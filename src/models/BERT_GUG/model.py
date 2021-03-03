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
from utils.method_output import MethodOutput


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
        self.num_labels = num_labels
        self.save_hyperparameters()

        self.test_pred_out = False

        self.current_best_metrics = -float('inf')

        if tokenizer is not None:
            self.tokenizer = tokenizer
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_type)
        init_model_info = model_type if init_pretrained_path is None else init_pretrained_path
        self.config = AutoConfig.from_pretrained(init_model_info)
        self.config.num_labels = self.num_labels
        self.model = AutoModelForSequenceClassification.from_pretrained(init_model_info, config=self.config)

    def forward(self, input_ids, labels=None):
        max_pad = (input_ids != self.tokenizer.pad_token_id).sum(dim=1).max().cpu().item()
        input_ids = input_ids[:, :max_pad]

        outputs = self.model(input_ids=input_ids, labels=labels, return_dict=True)
        result = MethodOutput()
        result.logits = outputs.logits
        if labels is not None:
            result.loss = outputs.loss
        return result

    def training_step(self, batch, batch_idx, optimizer_idx=None, ):
        input_ids = batch[0]
        labels = batch[-1]
        outputs = self.forward(input_ids=input_ids, labels=labels)
        loss = outputs.loss
        self.log("train_loss", loss)
        return loss

    def eval_step(self, batch):
        result = MethodOutput()
        input_ids = batch[0]
        labels = batch[-1]
        outputs = self.forward(input_ids=input_ids, labels=labels)
        result.loss = outputs.loss
        result.pred = outputs.logits.view(-1, 1)
        result.labels = labels
        return result

    def eval_epoch_end(self, eval_step_outputs):
        losses = list()
        labels = list()
        preds = list()
        for eval_step_result in eval_step_outputs:
            eval_step_result = MethodOutput(eval_step_result)
            losses.append(eval_step_result.loss.reshape(1))
            labels.append(eval_step_result.labels)
            preds.append(eval_step_result.pred)
        loss = torch.mean(torch.cat(losses))
        labels = torch.cat(labels)
        preds = torch.cat(preds)
        eval_pearsonr = torch.tensor(calc_pearsonr(preds.cpu(), labels.cpu()))
        result = MethodOutput()
        result.loss = loss
        result.pearsonr = eval_pearsonr
        result.preds = preds
        return result

    def validation_step(self, batch, batch_idx, *args, **kwargs):
        return self.eval_step(batch)

    def validation_epoch_end(self, val_step_outputs):
        result = self.eval_epoch_end(val_step_outputs)
        self.log('dev_pearsonr', result.pearsonr, on_step=False, on_epoch=True, prog_bar=True)
        self.log("dev_loss", result.loss, on_step=False, on_epoch=True, prog_bar=True)
        if self.current_best_metrics < result.pearsonr.item():
            self.current_best_metrics = result.pearsonr.item()
        return result

    def test_step(self, batch, batch_idx, *args, **kwargs):
        return self.eval_step(batch)

    def test_epoch_end(self, test_step_outputs, *args, **kwargs):
        result = self.eval_epoch_end(test_step_outputs)
        self.log('test_pearsonr', result.pearsonr)
        self.log('test_loss', result.loss)
        if self.test_pred_out:
            return result.preds

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
