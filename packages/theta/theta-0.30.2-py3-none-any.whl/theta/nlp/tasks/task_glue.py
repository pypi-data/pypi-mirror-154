#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from collections import OrderedDict
from typing import Type

import numpy as np
import torch
#  import torch.functional as F
import torch.nn.functional as F
import torch.nn as nn
from loguru import logger
from sklearn.metrics import f1_score
from torch.nn import CrossEntropyLoss, MSELoss
from tqdm import tqdm

from theta.nlp.arguments import (DataArguments, ModelArguments, TaskArguments,
                                 TrainingArguments)
from theta.nlp.data.samples import GlueSamples
from transformers import AutoModelForSequenceClassification

from .task import BaseDataset, BaseTask, TaskData, TaskRunner, TransformerModel


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def simple_accuracy(preds, labels):
    return (preds == labels).mean()


#  def acc_and_f1(preds, labels, average="micro"):
#      correct = np.sum((preds == labels).astype(int))
#      acc = correct / preds.shape[0]
#      f1 = f1_score(y_true=labels,
#                    y_pred=preds,
#                    average=average,
#                    zero_division=1)
#      acc_and_f1 = (acc + f1) / 2
#      return {"acc": acc, "f1": f1, "acc_and_f1": acc_and_f1}


def p_r_f1(preds, labels):
    if len(preds.shape) > 1 and len(labels.shape) > 1:
        tp = np.sum(((preds + labels) == 2).astype(int))
        fp = np.sum(((preds - labels) == 1).astype(int))
        fn = np.sum(((labels - preds) == 1).astype(int))
    else:
        tp = np.sum((preds == labels).astype(int))
        num_true = labels.shape[0]
        fn = num_true - tp
        num_pred = preds.shape[0]
        fp = num_pred - tp

    p = tp / (tp + fp) if tp + fp != 0 else 0.0
    r = tp / (tp + fn) if tp + fn != 0 else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) != 0 else 0.0

    #  return {"acc": acc, "f1": f1, "acc_and_f1": acc_and_f1}
    return (p, r, f1)


# ------------------------------ Dataset ------------------------------
class GlueDataset(BaseDataset):
    """
    完成模型输入数据的编码工作
    """

    def __init__(self, *args, **kwargs):
        super(GlueDataset, self).__init__(*args, **kwargs)

    def _encode_item(self, x):
        guid, text_a, text_b, labels = x

        # -------- input_ids, attention_mask, token_type_ids --------
        text_pair = [(text_a, text_b)] if text_b is not None else [text_a]
        encodings = self.tokenizer.batch_encode_plus(
            text_pair,
            padding=self.data_args.padding,
            max_length=self.data_args.max_length,
            add_special_tokens=True,
            truncation=True,
            return_offsets_mapping=True)
        input_ids = torch.from_numpy(
            np.array(encodings.input_ids, dtype=np.int64))[0]
        attention_mask = torch.from_numpy(
            np.array(encodings.attention_mask, dtype=np.int64))[0]
        token_type_ids = torch.from_numpy(
            np.array(encodings.token_type_ids, dtype=np.int64))[0]

        # -------- labels --------
        if labels is not None:
            if isinstance(labels, list):
                encoded_labels = [0] * len(self.label2id)
                for x in labels:
                    encoded_labels[self.label2id[x]] = 1
                labels = torch.from_numpy(
                    np.array(encoded_labels, dtype=np.float32))
            else:
                if labels:
                    encoded_labels = self.label2id[labels]
                else:
                    encoded_labels = 0
                labels = torch.from_numpy(
                    np.array(encoded_labels, dtype=np.int64))

        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'token_type_ids': token_type_ids,
            'labels': labels
        }

    @classmethod
    def collate_fn(cls, batch):
        stacked_batch = {}
        #  for key in ['input_ids', 'attention_mask', 'token_type_ids', 'labels']:
        #      key_batch = [e[key] for e in batch if e[key] is not None]
        #      if key_batch:
        #          batch_values = torch.stack(key_batch)
        #          stacked_batch[key] = batch_values
        #      else:
        #          stacked_batch[key] = None
        #  return stacked_batch

        not_none_tensor_keys = [
            'input_ids', 'attention_mask', 'token_type_ids'
        ]
        maybe_none_tensor_keys = ['labels']
        not_tensor_keys = []

        # not None tensors
        for key in not_none_tensor_keys:
            key_batch = [e[key] for e in batch if e[key] is not None]
            #  logger.info(f"key: {key} key_batch: {key_batch}")
            batch_values = torch.stack(key_batch)
            stacked_batch[key] = batch_values
        # maybe None tensors
        for key in maybe_none_tensor_keys:
            key_batch = [e[key] for e in batch if e[key] is not None]
            if key_batch:
                batch_values = torch.stack(key_batch)
                stacked_batch[key] = batch_values
            else:
                stacked_batch[key] = None
        # not tensors
        for key in not_tensor_keys:
            key_batch = [e[key] for e in batch if e[key] is not None]
            stacked_batch[key] = key_batch

        return stacked_batch


# ------------------------------ TaskData ------------------------------
class GlueData(TaskData):
    """
    指定任务专属的Dataset类型，并提供训练、验证、测试集实例。
    """

    def __init__(self, *args, **kwargs):
        super(GlueData, self).__init__(*args, **kwargs)

    def build_train_dataset(self):
        return GlueDataset(self.data_args, self._splitted_train_samples.rows,
                           self.label2id, self.tokenizer)

    def build_val_dataset(self):
        return GlueDataset(self.data_args, self._splitted_val_samples.rows,
                           self.label2id, self.tokenizer)

    def build_test_dataset(self):
        return GlueDataset(self.data_args, self.test_samples.rows,
                           self.label2id, self.tokenizer)


# https://github.com/wangz10/contrastive_loss


def compute_kl_loss(p, q, pad_mask=None):

    p_loss = F.kl_div(F.log_softmax(p, dim=-1),
                      F.softmax(q, dim=-1),
                      reduction='none')
    q_loss = F.kl_div(F.log_softmax(q, dim=-1),
                      F.softmax(p, dim=-1),
                      reduction='none')

    # pad_mask is for seq-level tasks
    if pad_mask is not None:
        p_loss.masked_fill_(pad_mask, 0.)
        q_loss.masked_fill_(pad_mask, 0.)

    # You can choose whether to use function "sum" and "mean" depending on your task
    p_loss = p_loss.sum()
    q_loss = q_loss.sum()

    loss = (p_loss + q_loss) / 2
    return loss


#  def contrastive_learning_loss_official(alpha, loss_fct, labels, num_labels,
#                                         logits_list):
def contrastive_learning_loss_official(alpha, loss_fct, labels, num_labels,
                                       logits_list):
    #  print(f"In contrastive_learning_loss")

    logits1 = logits_list[0]
    logits2 = logits_list[-1]
    #  print(f"logits1: {logits1}, logits2: {logits2}")

    #  loss1 = losses_list[0]
    #  loss2 = losses_list[-1]
    # cross entropy loss for classifier
    #  loss1 = loss_fct(logits1.view(-1, num_labels), labels.view(-1))
    #  loss2 = loss_fct(logits2.view(-1, num_labels), labels.view(-1))
    loss1 = loss_fct(logits1, labels)
    loss2 = loss_fct(logits2, labels)
    #  print(f"loss1: {loss1}, loss2: {loss2}")

    ce_loss = 0.5 * (loss1 + loss2)
    #  print(f"ce_loss: {ce_loss}")

    kl_loss = compute_kl_loss(logits1, logits2)
    #  print(f"cel_loss: {ce_loss.item():.6f}, kl_loss: {kl_loss.item():.6f}")

    # carefully choose hyper-parameters
    # 0.849145
    #  alpha = 10.0

    # 0.824338
    #  alpha = 0.1

    # submissions/prediction_glue_20220603001227_20220603.170045.json
    # 0.843111
    #  alpha = 1.0

    # submissions/prediction_glue_20220603170256_20220604.000032.json
    # 0.84311
    #  alpha = 20.0

    loss = ce_loss + alpha * kl_loss
    #  print(f"contrastive_loss: {loss}")

    return loss, logits_list[0]


def contrastive_learning_loss_old(alpha, loss_fct, labels, num_labels,
                                  logits_list):
    loss = None
    for logits in logits_list:
        if num_labels == 1:
            #  We are doing regression
            loss_fct = MSELoss()
            if loss:
                loss += alpha * loss_fct(logits.view(-1), labels.view(-1))
            else:
                loss = alpha * loss_fct(logits.view(-1), labels.view(-1))
        else:
            loss_fct = CrossEntropyLoss()
            if loss:
                loss += alpha * loss_fct(logits.view(-1, num_labels),
                                         labels.view(-1))
            else:
                loss = alpha * loss_fct(logits.view(-1, num_labels),
                                        labels.view(-1))

    if loss is not None:
        if num_labels == 1:
            loss_fct = MSELoss()
            loss += 1.0 * loss_fct(logits_list[0].view(-1),
                                   logits_list[-1].view(-1))
        else:
            p = torch.log_softmax(logits_list[0].view(-1, num_labels), dim=-1)
            p_tec = torch.softmax(logits_list[0].view(-1, num_labels), dim=-1)
            q = torch.log_softmax(logits_list[-1].view(-1, num_labels), dim=-1)
            q_tec = torch.softmax(logits_list[-1].view(-1, num_labels), dim=-1)

            kl_loss = torch.nn.functional.kl_div(p, q_tec,
                                                 reduction='none').sum()
            reverse_kl_loss = torch.nn.functional.kl_div(
                q, p_tec, reduction='none').sum()
            loss += 0.5 * (kl_loss + reverse_kl_loss) / 2.

#
    return loss, logits_list[0]


#  contrastive_learning_loss = contrastive_learning_loss_old
contrastive_learning_loss = contrastive_learning_loss_official


class MyGlueBaseModel(TransformerModel):

    def __init__(
        self,
        model_name_or_path,
        num_labels,
        tokenizer=None,
        dropout_prob=0.1,
        attention_probs_dropout_prob=0.1,
        #  loss_type='CrossEntropyLoss',
        loss_type='FocalLoss',
        #  loss_type='LabelSmoothingCrossEntropy',
        #  loss_type='DiceLoss',
        **kwargs):

        # for TransformerModel.load_from_config()
        self.num_labels = num_labels
        super(MyGlueBaseModel, self).__init__(
            model_name_or_path,
            tokenizer=tokenizer,
            automodel_cls=AutoModelForSequenceClassification,
            dropout_prob=dropout_prob,
            attention_probs_dropout_prob=attention_probs_dropout_prob)
        #  config = self.config
        #  if self._is_xlnet():
        #      from transformers.modeling_utils import SequenceSummary
        #      self.sequence_summary = SequenceSummary(config)
        #      self.logits_proj = nn.Linear(config.d_model, self.num_labels)
        #  else:
        #      self.dropout = nn.Dropout(config.hidden_dropout_prob)
        #      self.classifier = nn.Linear(config.hidden_size, self.num_labels)

        self.init_weights()

    def _adjust_config(self):
        setattr(self.config, 'num_labels', self.num_labels)
        # default: 0.1
        setattr(self.config, 'attention_probs_dropout_prob',
                self.attention_probs_dropout_prob)
        # default: null
        setattr(self.config, 'classifier_dropout', self.dropout_prob)

    def load_from_pretrained(self, model_path):
        #  automodel_cls = AutoModelForSequenceClassification
        #  super(MyGlueModel,
        #        self)._load_from_pretrained(model_path,
        #                                    automodel_cls=automodel_cls,
        #                                    num_labels=self.num_labels)

        self._adjust_config()
        self.transformer = AutoModelForSequenceClassification.from_pretrained(
            model_path, config=self.config)

        #  self.transformer = AutoModelForSequenceClassification.from_pretrained(
        #      model_path, num_labels=self.num_labels)

    def load_from_config(self):
        self._adjust_config()
        self.transformer = AutoModelForSequenceClassification.from_config(
            self.config)
        logger.warning(f"After load_from_config() : {self.config}")

    def forward(self,
                input_ids=None,
                attention_mask=None,
                token_type_ids=None,
                labels=None):

        outputs = self.transformer(input_ids,
                                   attention_mask=attention_mask,
                                   token_type_ids=token_type_ids,
                                   labels=labels,
                                   return_dict=True)
        #  logger.warning(f"outputs[0].shape: {outputs[0].shape}")
        #  logger.warning(f"outputs: {outputs}")
        # logger.warning(f"outputs[1]: {outputs[1]}")

        #  if labels is not None:
        #      loss = outputs.loss
        #      logits = outputs.logits
        #      return (loss, logits)
        #  else:
        #      logits = outputs.logits
        #      return logits

        #          if self._is_xlnet():
        #              output = outputs[0]
        #              output = self.sequence_summary(output)
        #              logits = self.logits_proj(output)
        #          #  elif self._is_electra():
        #          #      # ElectraConfig last_hidden_state
        #          #      pooled_output = outputs[0]
        #          #
        #          #      pooled_output = self.dropout(pooled_output)
        #          #      logits = self.classifier(pooled_output)
        #          else:
        #              # BERT
        #              pooled_output = outputs.pooler_output
        #
        #              pooled_output = self.dropout(pooled_output)
        #              logits = self.classifier(pooled_output)
        #  #
        #          if labels is not None:
        #              loss_fct = CrossEntropyLoss()
        #              loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
        #              return (loss, logits)
        #          else:
        #              return logits

        loss = outputs.loss
        logits = outputs.logits
        if labels is not None:
            return (loss, logits)
        else:
            return logits


class MyGlueModel(MyGlueBaseModel):

    def __init__(
        self,
        model_name_or_path,
        num_labels,
        tokenizer=None,
        dropout_prob=0.1,
        attention_probs_dropout_prob=0.1,
        #  loss_type='CrossEntropyLoss',
        loss_type='FocalLoss',
        #  loss_type='LabelSmoothingCrossEntropy',
        #  loss_type='DiceLoss',
        **kwargs):

        # for TransformerModel.load_from_config()
        self.num_labels = num_labels
        super(MyGlueModel, self).__init__(
            model_name_or_path,
            num_labels,
            tokenizer=tokenizer,
            dropout_prob=dropout_prob,
            attention_probs_dropout_prob=attention_probs_dropout_prob,
            loss_type=loss_type,
            **kwargs)

    def forward(self,
                input_ids=None,
                attention_mask=None,
                token_type_ids=None,
                labels=None):

        outputs = self.transformer(input_ids,
                                   attention_mask=attention_mask,
                                   token_type_ids=token_type_ids,
                                   labels=labels,
                                   return_dict=True)
        loss = outputs.loss
        logits = outputs.logits
        if labels is not None:
            return (loss, logits)
        else:
            return logits


class ContrastiveLearningGlueModel(MyGlueBaseModel):

    def __init__(
            self,
            model_name_or_path,
            num_labels,
            tokenizer=None,
            dropout_prob=0.1,
            attention_probs_dropout_prob=0.1,
            #  loss_type='CrossEntropyLoss',
            loss_type='FocalLoss',
            #  loss_type='LabelSmoothingCrossEntropy',
            #  loss_type='DiceLoss',
            cl_alpha=4.0,
            **kwargs):

        # for TransformerModel.load_from_config()
        self.num_labels = num_labels
        self.cl_alpha = cl_alpha
        super(ContrastiveLearningGlueModel, self).__init__(
            model_name_or_path,
            num_labels,
            tokenizer=tokenizer,
            dropout_prob=dropout_prob,
            attention_probs_dropout_prob=attention_probs_dropout_prob,
            loss_type=loss_type,
            **kwargs)

    def forward(self,
                input_ids=None,
                attention_mask=None,
                token_type_ids=None,
                labels=None):

        if labels is not None:
            logits_list = []
            for i in range(2):
                outputs = self.transformer(input_ids,
                                           attention_mask=attention_mask,
                                           token_type_ids=token_type_ids,
                                           labels=labels,
                                           return_dict=True)
                loss = outputs.loss
                logits = outputs.logits
                logits_list.append(logits)

            alpha = self.cl_alpha
            loss_fct = CrossEntropyLoss()
            num_labels = self.num_labels
            #  print(f"call contrastive_learning_loss")
            loss, logits = contrastive_learning_loss(alpha, loss_fct, labels,
                                                     num_labels, logits_list)
            #  print(f"After contrastive_learning_loss: {loss: {loss}}")
            return (loss, logits)
        else:
            outputs = self.transformer(input_ids,
                                       attention_mask=attention_mask,
                                       token_type_ids=token_type_ids,
                                       labels=labels,
                                       return_dict=True)
            logits = outputs.logits
            return logits


# ------------------------------ TaskRunner ------------------------------


class GlueRunner(TaskRunner):
    """
    任务专属模型定义
    """

    def __init__(self, task_args, glue_labels):
        super(GlueRunner, self).__init__(**task_args.to_dict())
        logger.warning(f"glue_labels: {glue_labels}")
        self.glue_labels = glue_labels
        self.num_labels = len(self.glue_labels)
        self.label2id = {x: i for i, x in enumerate(glue_labels)}
        self.id2label = {i: x for i, x in enumerate(glue_labels)}
        self.type_weights = np.ones(self.num_labels)

        model_args = task_args.model_args
        attention_probs_dropout_prob = model_args.attention_probs_dropout_prob

        logger.warning(f"num_labels: {self.num_labels}")
        if model_args.cl_alpha:
            self.model = ContrastiveLearningGlueModel(
                model_name_or_path=model_args.model_name_or_path
                if model_args.model_name_or_path else os.path.join(
                    model_args.checkpoint_path, "checkpoint"),
                dropout_prob=model_args.dropout_prob,
                attention_probs_dropout_prob=attention_probs_dropout_prob,
                num_labels=self.num_labels,
                cl_alpha=model_args.cl_alpha)
        else:
            self.model = MyGlueModel(
                model_name_or_path=model_args.model_name_or_path
                if model_args.model_name_or_path else os.path.join(
                    model_args.checkpoint_path, "checkpoint"),
                dropout_prob=model_args.dropout_prob,
                attention_probs_dropout_prob=attention_probs_dropout_prob,
                num_labels=self.num_labels)
        #  config = self.transformer.config
        #  if self._is_xlnet():
        #      from transformers.modeling_utils import SequenceSummary
        #      self.sequence_summary = SequenceSummary(config)
        #      self.logits_proj = nn.Linear(config.d_model, num_labels)
        #  else:
        #      self.dropout = nn.Dropout(config.hidden_dropout_prob)
        #      self.classifier = nn.Linear(config.hidden_size, num_labels)

    def forward(self, *args, **kwargs):
        return self.model(*args, **kwargs)

    #  def forward(self, batch, batch_idx):
    #  def forward(self,
    #              input_ids=None,
    #              attention_mask=None,
    #              token_type_ids=None,
    #              labels=None):
    #
    #      return self.model(*args, **kwargs)
#          outputs = self.transformer(input_ids,
#                                           attention_mask=attention_mask,
#                                           token_type_ids=token_type_ids,
#                                           return_dict=True)
#          #  logger.warning(f"outputs[0].shape: {outputs[0].shape}")
#          #  logger.warning(f"outputs: {outputs}")
#          # logger.warning(f"outputs[1]: {outputs[1]}")
#
#          #  if labels is not None:
#          #      loss = outputs.loss
#          #      logits = outputs.logits
#          #      return (loss, logits)
#          #  else:
#          #      logits = outputs.logits
#          #      return logits
#
#          if self._is_xlnet():
#              output = outputs[0]
#              output = self.sequence_summary(output)
#              logits = self.logits_proj(output)
#          elif self._is_electra():
#              # ElectraConfig last_hidden_state
#              pooled_output = outputs[0]
#
#              pooled_output = self.dropout(pooled_output)
#              logits = self.classifier(pooled_output)
#          else:
#              # BERT
#              pooled_output = outputs.pooler_output
#
#              pooled_output = self.dropout(pooled_output)
#              logits = self.classifier(pooled_output)
#  #
#          if labels is not None:
#              loss_fct = CrossEntropyLoss()
#              loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
#              return (loss, logits)
#          else:
#              return logits

    def training_step(self, batch, batch_idx):
        outputs = self.forward(**batch)
        loss = outputs[0]

        self.log('train_loss', loss, on_step=True)
        #  self.log('lr', self.hparams.lr, on_step=True)

        return OrderedDict({
            "loss": loss,
        })

    def validation_step(self, batch, batch_idx):
        #  logger.warning(f"batch: {batch}")
        #  logger.info(f"batch['input_ids'].shape: {batch['input_ids'].shape}")
        #  logger.info(
        #      f"batch['attention_mask'].shape: {batch['attention_mask'].shape}")
        #  logger.info(
        #      f"batch['token_type_ids'].shape: {batch['token_type_ids'].shape}")
        #  logger.info(f"batch['labels'].shape: {batch['labels'].shape}")
        val_loss, logits = self.forward(**batch)

        #  preds = np.argmax(logits, axis=1)

        batch_labels = batch['labels']
        batch_labels = batch_labels.cpu().numpy().astype(int)

        is_multi_label_classification = False
        if len(batch_labels.shape) == 1:
            is_multi_label_classification = False
        else:
            is_multi_label_classification = True
        #  logger.info(
        #      f"is_multi_label_classification: {is_multi_label_classification}")

        if is_multi_label_classification:
            confidence = 0.5
            batch_probs = torch.sigmoid(logits).cpu().numpy()
            batch_preds = (batch_probs > confidence).astype(int)
            val_acc, val_recall, val_f1 = p_r_f1(batch_preds, batch_labels)

        else:
            #  correct_count = torch.sum(batch_labels == batch_preds).float()
            #  if self.on_gpu:
            #      correct_cout = correct_count.cuda(val_loss.device.index)
            batch_probs = torch.softmax(logits, -1)
            batch_preds = torch.argmax(logits, dim=1).cpu().numpy()
            val_acc, val_recall, val_f1 = p_r_f1(batch_preds, batch_labels)

        self.log('val_loss', val_loss, on_step=True)
        self.log('val_acc', val_acc, on_step=True)
        self.log('val_recall', val_recall, on_step=True)
        self.log('val_f1', val_f1, on_step=True)

        #  logger.info(f"val_loss: {val_loss:.4f}")

        return OrderedDict({
            'val_loss': val_loss,
            'val_acc': val_acc,
            'val_recall': val_recall,
            'val_f1': val_f1,
            'batch_probs': batch_probs,
            #  'correct_count': correct_count,
            'batch_idx': batch_idx,
            'batch_size': batch_labels.shape[0]
        })

    def validation_epoch_end(self, outputs):
        #  val_acc = sum([out["correct_count"]
        #                 for out in outputs]).float() / sum(out["batch_size"]
        #                                                    for out in outputs)
        #  val_acc = sum([out["correct_count"]
        #                 for out in outputs]) / sum(out["batch_size"]
        #                                            for out in outputs)
        val_loss = sum([out["val_loss"] for out in outputs]) / len(outputs)
        val_acc = sum([out["val_acc"] for out in outputs]) / len(outputs)
        val_recall = sum([out["val_recall"] for out in outputs]) / len(outputs)
        val_f1 = sum([out["val_f1"] for out in outputs]) / len(outputs)
        logger.info(
            f"val_loss: {val_loss:.4f}, val_acc: {val_acc:.4f}, val_recall: {val_recall:.4f}, val_f1: {val_f1:.4f}"
        )
        min_batch_idx = min([out["batch_idx"] for out in outputs])
        max_batch_idx = max([out["batch_idx"] for out in outputs])
        #  batch_size = int(
        #      sum([out["batch_size"] for out in outputs]) / len(outputs))

        self.log('val_loss', val_loss, on_epoch=True)
        self.log('val_acc', val_acc, on_epoch=True)
        self.log('val_recall', val_acc, on_epoch=True)
        self.log('val_f1', val_f1, on_epoch=True)

        eval_outputs = {
            'min_batch_idx': min_batch_idx,
            'max_batch_idx': max_batch_idx,
            #  'batch_size': batch_size,
            'val_loss': val_loss,
            'val_acc': val_acc,
            'val_recall': val_recall,
            'val_f1': val_f1
        }
        self.save_best_model(eval_outputs)

    def test_step(self, batch, batch_idx):
        logits = self.forward(**batch)

        preds = torch.argmax(logits, dim=1)

        return OrderedDict({'preds': preds, 'logits': logits})

    def test_epoch_end(self, outputs):

        final_preds = torch.cat([out['preds'] for out in outputs])
        logger.info(f"preds: {final_preds.shape}")
        final_preds = final_preds.detach().cpu().numpy().tolist()

        final_logits = torch.cat([out['logits'] for out in outputs])
        logger.info(f"logits: {final_logits.shape}")
        final_logits = final_logits.detach().cpu().numpy().tolist()

        self.test_results = {'preds': final_preds, 'logits': final_logits}


# ------------------------------ Task ------------------------------
class GlueTask(BaseTask):
    #  def __init__(self, *args, **kwargs):
    #      super(GlueTask, self).__init__(*args, **kwargs)
    def __init__(self, args: Type[TaskArguments], data: Type[TaskData],
                 glue_labels: list):
        runner = GlueRunner(args, glue_labels)
        super(GlueTask, self).__init__(args, data, runner)

    @classmethod
    def get_data_class(cls):
        return GlueData

    @classmethod
    def get_samples_class(cls):
        from ..data.samples import GlueSamples
        return GlueSamples

    def execute(self, *args, **kwargs):
        model_args = self.model_args
        data_args = self.data_args
        training_args = self.training_args
        remaining_args = self.remaining_args

        return super(GlueTask, self).execute(*args, **kwargs)

    def generate_submission(self):
        logger.warning(f"GlueTask.generate_submission().")

    @classmethod
    def run_task_from_checkpoint(task_cls,
                                 task_args,
                                 checkpoint_path,
                                 labels_list,
                                 do_train=False,
                                 do_eval=False,
                                 do_predict=False,
                                 do_submit=False,
                                 train_data_generator=None,
                                 test_data_generator=None):
        from .task import run_task_from_checkpoint as _run_task_from_checkpoint
        return _run_task_from_checkpoint(
            task_cls,
            task_args,
            checkpoint_path,
            labels_list,
            do_train=do_train,
            do_eval=do_eval,
            do_predict=do_predict,
            do_submit=do_submit,
            train_data_generator=train_data_generator,
            test_data_generator=test_data_generator)
