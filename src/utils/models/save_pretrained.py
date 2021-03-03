from copy import deepcopy
from os import makedirs, path

import torch


def _save_pretrained(model_class, saved_param_name_list, savepath):
    print("save model:", savepath)
    model_to_save = deepcopy(model_class)
    model_to_save.to("cpu")
    makedirs(savepath, exist_ok=True)
    torch.save(model_to_save.state_dict(),
               path.join(savepath, "state_dict.bin"))

    params = {}
    for key in model_to_save.__dict__.keys():
        if key in saved_param_name_list:
            params[key] = model_to_save.__dict__[key]
    torch.save(params, path.join(savepath, "params.bin"))
