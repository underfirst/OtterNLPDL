# GUGの説明

```shell
cd data/raw/;
git clone https://github.com/EducationalTestingService/gug-data.git
# 絶対にraw/以下のgug_annotations.tsvとか, オリジナルのREADME.mdをいじるなよ? 絶対にいじるなよ? おじさんとの約束だ!
```

(英文, 英文の文法的人手による正しさ評価)のデータセットです.
  
## gug_annotations.tsvの説明

- Id: ID
- Sentence: 英文
- Expert Judgement: 著者1人(英語添削のプロ)が, 1-4段階でつけた評価.
- Crowd Flower Judgements: クラウドワーカー(英語添削マンとかではないただの真面目なネイティブスピーカー)5人による評価.
- Average: Crowd Flower Judgementsの平均値. (これを予測するZ!)
- Dataset: 著者らによる `train`, `dev`, `test`の分割指示.

## 実行結果目安:

train_loss 0.01046
test_pearsonr 0.74255
test_loss 0.12959
