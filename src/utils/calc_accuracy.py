import numpy as np
from sklearn.metrics import accuracy_score


def calc_accuracy(preds, labels):
    preds = np.array(preds)
    labels = np.array(labels)
    return accuracy_score(preds.reshape(-1), labels.reshape(-1))


if __name__ == '__main__':
    import torch

    outputs_preds = torch.randint(3, (32, 1))
    labels = torch.randint(3,(32,))
    print(accuracy_score(outputs_preds, labels))
