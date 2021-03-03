# OtterTemplate

NLP班で, 特にhuggingfaceを用いたコーディング工数が
多めに発生するタイプの人たちむけのプロジェクトテンプレートです.

joey組やsockeye組のshell芸が主要な人は, スケートのものを参考にしてください.

--------------------

## フォルダ構造

[cookie-cutter][cookie-cutter]の[data science template][ds-template]がベースとなっています.
cookie-cutterはPython製のプロジェクトのフォルダ雛形の自動作成ツールです.
知らんけど, 最近だと小町研でも使われているらしい.

- `data/`: モデルの訓練や生成に使うデータのフォルダ.
  - `raw/`: 生データのフォルダ. **データはダウンロードしてzip解凍すること以外に原則編集しない.**
  - `processed/`: 処理済みデータのフォルダ.
- `docs/`: 手順書やメモなどの任意のドキュメント置き場.
- `external_tools/`: 他人が書いたソースコードやプログラムなど. git cloneしたものとかも全部ここにおく.
- `models/`: 自分が作成したモデルの訓練済みパラメータや, パラメータの評価結果など. あるいは他人が配布した訓練済みモデル一式など.
- `setup/`: 実験環境を作成するためのPipfile以外のファイル. (Dockerfileとか, shellとか, その他メモなど.)
- `src/`: 自分の書いたPython scripts一式.
  - `config/`: デフォルトの設定定数定義フォルダ.
    - `const.py`: 全体で共通の定数. (例: seed)
    - `datapath.py`: 全体で共通のファイルパス. (例: プロジェクトtopの絶対パスや`data/`への絶対パス.)
  - `models/`: モデルの定義ファイル.
  - `data/`: データ操作のファイル. (前処理, Dataloader, labelや文の単語数の分布などの可視化のコードなど.)
  - `controllers/`: 実行コード本体. (モデルの訓練や評価や生成のためのコード.)
  - `utils/`: 各種ユーティリティ自作関数ファイル.
  
### フォルダ上での注意

#### data/raw/フォルダの取扱い.

**データはダウンロードしてzip解凍すること以外に原則編集しない.**
説明のREADME.mdファイルの追加は許すが, ファイル名も含めてファイルに1byteでも追加, 編集, 削除を行うなら`processed/`にコピーして行う.
自分による編集を施したファイルを`raw/`フォルダに追加しない.
`raw/`フォルダには原則ダウンロードしてほやほやのファイル+説明がいればその説明ファイル以外を絶対におかないこと.
そうすると, 自分の編集がミスった時`raw/`フォルダから`processed/`へのコピペだけで実験をやり直せる.
途中で編集したファイルがごっちゃになると, 修正がめんどくさいので, ファイルごっちゃリスクを回避できる程度のファイルサイズのデータは`raw/`で新鮮なまま保持.

#### `src/`でのおすすめフォルダ構造.

実験毎に割と定数・モデル定義・データ処理・コントローラが異なることが多いと思うので, 自分は実験単位(以後自分はドメインと呼ぶ)でディレクトリを切ります.
`const/`, `models/`, `data/`, `controllers/`の下にドメイン毎のフォルダを作成しています.
例えば, BERTによる感情分析 (ドメイン名: BERT_STSB)の実験では, 
`src/config/BERT_STSB/`, `src/models/BERT_STSB/ `, `src/data/BERT_STSB/`, `src/controllers/BERT_STSB/`のようなフォルダを作り, その中にBERT_STSBの実験特有のコードを書いていきます.
人によっては, `src/BERT_STSB/config/`, `src/BERT_STSB/models/`, `src/BERT_STSB/controllers/`のようにする流派もありそうです. 
そこら辺は, お好みでどうぞ.

--------------------


[cookie-cutter]:https://cookiecutter.readthedocs.io/en/latest/installation.html
[ds-template]:https://github.com/drivendata/cookiecutter-data-science