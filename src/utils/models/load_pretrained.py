from os import path

import torch


def _load_pretrained(model_class, loadpath):
    print("load model from", loadpath)
    params = torch.load(path.join(loadpath, "params.bin"))
    model = model_class(**params)
    model.load_state_dict(torch.load(path.join(loadpath, "state_dict.bin")))
    return model
