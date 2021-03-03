from argparse import ArgumentParser

import torch
from pytorch_lightning import LightningModule
from transformers import (AdamW, AutoConfig,
                          AutoModelForSequenceClassification, AutoTokenizer,
                          get_linear_schedule_with_warmup)

from config.BERT_GUG import (BEST_MODEL_FOLDER_PREFIX, DEFAULT_LEARNING_RATE,
                             ES_METRIC, MODEL_PATH, MODEL_TYPE, NUM_LABELS,
                             WARMUP_STEP, WEIGHT_DECAY)
from utils.calc_pearsonr import calc_pearsonr


class LightningBERTClassificationModel(LightningModule):
    def __init__(self,
                 model_type=MODEL_TYPE,
                 tokenizer=None,
                 init_pretrained_path=None,
                 best_pretrained_path=MODEL_PATH,
                 best_model_folder_prefix=BEST_MODEL_FOLDER_PREFIX,
                 weight_decay=WEIGHT_DECAY,
                 default_learning_rate=DEFAULT_LEARNING_RATE,
                 apply_scheduler=True,
                 warmup_step=WARMUP_STEP,
                 num_training_step=None,
                 es_metric=ES_METRIC,
                 num_labels=NUM_LABELS,
                 **kwargs):
        super().__init__()
        self.warmup_step = warmup_step
        self.es_metric = es_metric
        self.num_training_step = num_training_step
        self.best_pretrained_path = best_pretrained_path
        self.best_model_folder_prefix = best_model_folder_prefix
        self.weight_decay = weight_decay
        self.default_learning_rate = default_learning_rate
        self.apply_scheduler = apply_scheduler
        self.save_hyperparameters()

        self.current_best_metrics = -float('inf')

        if tokenizer is not None:
            self.tokenizer = tokenizer
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_type)
        self.config = AutoConfig.from_pretrained(model_type)
        self.config.num_labels = num_labels
        self.model = AutoModelForSequenceClassification.from_pretrained(model_type, config=self.config)
        if init_pretrained_path is not None:
            self.load_architecture(init_pretrained_path, tokenizer=tokenizer)

    def forward(self, input_ids, labels=None):
        max_pad = (input_ids != self.tokenizer.pad_token_id).sum(dim=1).max().cpu().item()
        input_ids = input_ids[:, :max_pad]

        outputs = self.model(input_ids=input_ids, labels=labels, return_dict=True)
        if labels is not None:
            return outputs.loss, outputs.logits
        return outputs.logits

    def training_step(self, batch, batch_idx, optimizer_idx=None, ):
        input_ids = batch[0]
        labels = batch[-1]
        outputs = self.forward(input_ids=input_ids, labels=labels)
        loss = outputs[0]
        self.log("train_loss", loss)
        return loss

    def eval_step(self, batch):
        input_ids = batch[0]
        labels = batch[-1]
        outputs = self.forward(input_ids=input_ids, labels=labels)
        loss = outputs[0]
        pred = outputs[1].view(-1, 1)
        return loss, labels, pred

    def eval_epoch_end(self, eval_step_outputs):
        losses = list()
        labels = list()
        preds = list()
        for loss, label, pred in eval_step_outputs:
            losses.append(loss.reshape(1))
            labels.append(label)
            preds.append(pred)
        loss = torch.mean(torch.cat(losses))
        labels = torch.cat(labels)
        preds = torch.cat(preds)
        eval_pearsonr = torch.tensor(calc_pearsonr(preds.cpu(), labels.cpu()))
        return loss, eval_pearsonr

    def validation_step(self, batch, batch_idx, *args, **kwargs):
        return self.eval_step(batch)

    def validation_epoch_end(self, val_step_outputs):
        loss, pearsonr = self.eval_epoch_end(val_step_outputs)
        self.log('dev_pearsonr', pearsonr, on_step=False, on_epoch=True, prog_bar=True)
        self.log("dev_loss", loss, on_step=False, on_epoch=True, prog_bar=True)
        if self.current_best_metrics < pearsonr.item():
            self.current_best_metrics = pearsonr.item()
        return loss, pearsonr

    def test_step(self, batch, batch_idx, *args, **kwargs):
        return self.eval_step(batch)

    def test_epoch_end(self, test_step_outputs, *args, **kwargs):
        loss, pearsonr = self.eval_epoch_end(test_step_outputs)
        self.log('test_pearsonr', pearsonr)
        self.log('test_loss', loss)
        result = dict()
        result["test_loss"] = loss
        result["test_pearsonr"] = pearsonr
        return result

    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(),
                          weight_decay=self.weight_decay,
                          lr=self.default_learning_rate)
        result = []
        if self.apply_scheduler and self.num_training_step is not None:
            scheduler = get_linear_schedule_with_warmup(optimizer=optimizer, num_warmup_steps=self.warmup_step,
                                                        num_training_steps=self.num_training_step)
            result.append({
                "optimizer": optimizer,
                "lr_scheduler": {"scheduler": scheduler, 'interval': 'step'}, })
        else:
            result = [{"optimizer": optimizer}]
        return result

    def load_architecture(self, model_name_or_path, tokenizer=None):
        if tokenizer is not None:
            self.tokenizer = tokenizer
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.config = AutoConfig.from_pretrained(model_name_or_path)
        self.config.num_labels = self.num_labels
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name_or_path, config=self.config)

    @staticmethod
    def add_args(parent_parser):
        parser = ArgumentParser(parents=[parent_parser], add_help=False, conflict_handler="resolve")
        parser.add_argument('--model_type', default=MODEL_TYPE)
        parser.add_argument('--model_path', default=MODEL_PATH)
        parser.add_argument('--best_pretrained_path', default=MODEL_PATH)
        parser.add_argument('--weight_decay', type=float, default=WEIGHT_DECAY)
        parser.add_argument('--es_metric', type=str, default=ES_METRIC)
        parser.add_argument('--warmup_step', type=int, default=WARMUP_STEP)
        parser.add_argument('--apply_scheduler', action="store_true")
        parser.add_argument('--default_learning_rate', type=float, default=DEFAULT_LEARNING_RATE)
        return parser