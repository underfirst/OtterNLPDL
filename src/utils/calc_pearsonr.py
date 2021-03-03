import numpy as np
import torch
from scipy.stats import pearsonr


def calc_pearsonr(preds, labels):
    preds = np.array(preds)
    labels = np.array(labels)
    return pearsonr(preds.reshape(-1), labels.reshape(-1))[0]



if __name__ == '__main__':
    import torch
    outputs_preds = torch.randn((32, 1))
    labels = torch.randn((32))
    print(calc_pearsonr(outputs_preds, labels))
