import math
import numpy as np
import pandas as pd
from csv import QUOTE_NONE
# グラフを描画するライブラリ
from os import path
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()
from config.BERT_STSB import RAW_RESOURCE_PATH
from utils.readlines import readlines

def load_labels(mode="train"):
    tsv_path = path.join(RAW_RESOURCE_PATH, f"sts-{mode}.tsv")
    scores = readlines(tsv_path, callbacks=[lambda x: float(x.split("\t")[4])])
    data = [{"Dataset":mode,"score": s} for s in scores]
    return pd.DataFrame(data)

train = load_labels("train")
dev = load_labels("dev")
test = load_labels("test")
# スタージェスの公式で適切なbinsの値を求める
sturges = lambda n: math.ceil(math.log2(n*2))

# sns.distplot(
#     train["Average"],
#     bins=sturges(len(train["Average"])),
#     color='red',
#     kde=True,
#     label='Train'
# )
#
# sns.distplot(
#     dev["Average"],
#     bins=sturges(len(dev["Average"])),
#     color='blue',
#     kde=True,
#     label='Dev'
# )
#
# sns.distplot(
#     test["Average"],
#     bins=sturges(len(test["Average"])),
#     color='green',
#     kde=True,
#     label='Test'
# )
df =pd.concat([train, dev, test])
grid = sns.FacetGrid(df, col='Dataset', hue='Dataset', col_wrap=3, size=5)
grid.map(sns.distplot, 'score', bins=7, kde=True)

plt.legend()
plt.show()