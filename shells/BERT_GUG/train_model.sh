pipenv run python src/controllers/BERT_GUG/train_model.py \
  --gpus=0 \
  --experiment_name="BERT_GUG" --server_name="hanuman"
# pipenvのshellのなかで python src/controllers/BERT_GUG/train_model.py ...でも良い
# wandbにlogin必須 (嫌ならcontroller/BERT_GUG/train_model.pyからwandb loggerを全部消して, リライトしてくれ.)