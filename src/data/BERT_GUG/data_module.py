from argparse import ArgumentParser
from csv import QUOTE_NONE
from math import ceil

import numpy as np
import pandas as pd
import torch
from pytorch_lightning import LightningDataModule
from torch.utils.data import DataLoader, TensorDataset

from config.BERT_GUG import BATCH_SIZE, LEVEL, RAW_RESOURCE_PATH, SENTENCE


class LightningGUGDataModule(LightningDataModule):
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
        df = pd.read_csv(self.raw_resource_path, sep="\t", quoting=QUOTE_NONE)
        if self.debug_mode:
            lines = self.batch_size * 10
        else:
            lines = df.shape[0]
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
        df = pd.read_csv(self.raw_resource_path, sep="\t", quoting=QUOTE_NONE)
        df = df[df["Dataset"] == mode]
        if self.debug_mode:
            df = df[0:self.batch_size * 10]
        sentences = df[self.sentence].tolist()
        labels = df[self.level].to_numpy(dtype=float)
        tensor_data = self.tokenizer(sentences, padding=True)
        input_ids = torch.tensor(tensor_data["input_ids"], dtype=torch.long)
        max_seq_len = (input_ids != self.tokenizer.pad_token_id).sum(dim=1).squeeze().cpu()
        self.get_stats(max_seq_len.numpy(), mode=mode)
        input_ids = torch.tensor(tensor_data["input_ids"], dtype=torch.long)
        labels = torch.tensor(labels, dtype=torch.float)
        dataset = TensorDataset(input_ids, labels)
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

    from config.BERT_GUG import MODEL_TYPE

    tokenizer = AutoTokenizer.from_pretrained(MODEL_TYPE)
    data_module = LightningGUGDataModule(tokenizer)
    dev_dataloader = data_module.load_file(mode="dev")
