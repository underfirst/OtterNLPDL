from os import path
from pathlib import Path

from torch.utils.data import DataLoader, TensorDataset
from transformers import BartTokenizer

from config.const import BATCH_SIZE
from config.datapath import RAW_ASSET_PATH
from utils.readlines import readlines


def load_asset_dataloader(tokenizer: BartTokenizer,
                          batch_size=BATCH_SIZE,
                          mode="valid",
                          raw_asset_path=RAW_ASSET_PATH, ):
    src_lines = readlines(path.join(raw_asset_path, f"asset.{mode}.orig"), verbose=True)
    trg_paths = sorted(list(Path(raw_asset_path).glob(f"asset.{mode}.simp*")))
    src_tensor_data = tokenizer(src_lines, padding=True, return_tensors="pt")["input_ids"]
    data = [src_tensor_data]
    for trg_path in trg_paths:
        trg_lines = readlines(trg_path, verbose=False)
        trg_tensor_data = tokenizer(trg_lines, padding=True, return_tensors="pt")["input_ids"]
        data.append(trg_tensor_data)
    dataset = TensorDataset(*data)
    data_loader = DataLoader(dataset, shuffle=False, batch_size=batch_size, num_workers=0)
    return data_loader
