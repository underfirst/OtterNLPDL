import math
from csv import QUOTE_NONE

import numpy as np
import pandas as pd
import seaborn as sns
# グラフを描画するライブラリ
from matplotlib import pyplot as plt

from config.BERT_GUG import RAW_RESOURCE_PATH

sns.set()

df = pd.read_csv(RAW_RESOURCE_PATH, sep="\t", quoting=QUOTE_NONE)
train = df[df["Dataset"] == "train"]
dev = df[df["Dataset"] == "dev"]
test = df[df["Dataset"] == "test"]
# スタージェスの公式で適切なbinsの値を求める
sturges = lambda n: math.ceil(math.log2(n * 2))

sns.distplot(
    train["Average"],
    bins=sturges(len(train["Average"])),
    color='red',
    kde=True,
    label='Train'
)

sns.distplot(
    dev["Average"],
    bins=sturges(len(dev["Average"])),
    color='blue',
    kde=True,
    label='Dev'
)

sns.distplot(
    test["Average"],
    bins=sturges(len(test["Average"])),
    color='green',
    kde=True,
    label='Test'
)

df = pd.concat([train, dev, test])
grid = sns.FacetGrid(df, col='Dataset', hue='Dataset', col_wrap=3, size=5)
grid.map(sns.distplot, 'Average', bins=7, kde=True)

plt.legend()
plt.show()
