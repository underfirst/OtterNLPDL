from argparse import ArgumentParser
from os import path
from math import ceil
import numpy as np
import torch
from pytorch_lightning import LightningDataModule
from torch.utils.data import TensorDataset, DataLoader
from config.BERT_STSB import BATCH_SIZE, RAW_RESOURCE_PATH, SENTENCE, LEVEL
from utils.readlines import readlines


class LightningSTSBDataModule(LightningDataModule):
    def __init__(self,
                 tokenizer,
                 batch_size=BATCH_SIZE,
                 raw_resource_path=RAW_RESOURCE_PATH,
                 sentence=SENTENCE,
                 level=LEVEL,
                 debug_mode=False,
                 ):
        super().__init__()
        self.tokenizer = tokenizer
        self.batch_size = batch_size
        self.raw_resource_path = raw_resource_path
        self.sentence = sentence
        self.level = level
        self.debug_mode = debug_mode

    def setup(self, stage=None):
        pass

    def get_train_len(self):
        if self.debug_mode:
            lines = self.batch_size * 10
        else:
            lines = readlines(path.join(self.raw_resource_path, "sts-train.tsv"))
            lines = len(lines)
        return ceil(lines / self.batch_size)

    def get_stats(self, seq_len, mode):
        print(mode)
        print("avg:", np.mean(seq_len))
        print("std:", np.std(seq_len))
        print("ub:", np.mean(seq_len) + 1.96 * np.std(seq_len))
        print("#", len(seq_len))
        print("#>ub:", (seq_len > np.mean(seq_len) + 1.96 * np.std(seq_len)).sum())
        print("#>100:", (seq_len > 100).sum())

    def load_file(self, mode="train"):
        df = readlines(path.join(self.raw_resource_path, f"sts-{mode}.tsv"), callbacks=[lambda x: x.split("\t")])
        sent1_idx = 5
        sent2_idx = 6
        label_idx = 4
        if self.debug_mode:
            df = df[0:self.batch_size * 10]
        sentence_pairs = [[i[5], i[6]] for i in df]
        labels = torch.tensor([float(i[label_idx]) for i in df], dtype=torch.float)
        tensor_data = self.tokenizer(sentence_pairs, padding=True, return_tensors="pt")
        input_ids = tensor_data["input_ids"]
        max_seq_len = (input_ids != self.tokenizer.pad_token_id).sum(dim=1).squeeze().cpu()
        self.get_stats(max_seq_len.numpy(), mode=mode)
        dataset = TensorDataset(input_ids,
                                tensor_data["token_type_ids"],
                                labels)
        data_loader = DataLoader(dataset, shuffle=mode == "train", batch_size=self.batch_size, num_workers=0)
        return data_loader

    def train_dataloader(self, *args, **kwargs):
        dataloader = self.load_file(mode="train")
        return dataloader

    def val_dataloader(self, *args, **kwargs):
        dataloader = self.load_file(mode="dev")
        return dataloader

    def test_dataloader(self):
        dataloader = self.load_file(mode="test")
        return dataloader

    @staticmethod
    def add_args(parent_parser):
        parser = ArgumentParser(parents=[parent_parser], add_help=False, conflict_handler="resolve")
        parser.add_argument('--batch_size', type=int, default=BATCH_SIZE)
        return parser


if __name__ == '__main__':
    from transformers import AutoTokenizer
    from config.BERT_STSB import MODEL_TYPE

    tokenizer = AutoTokenizer.from_pretrained(MODEL_TYPE)
    data_module = LightningSTSBDataModule(tokenizer)
    train_dataloader = data_module.train_dataloader()
    dev_dataloader = data_module.load_file(mode="dev")
