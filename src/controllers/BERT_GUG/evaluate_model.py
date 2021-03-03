from pathlib import Path

import pytorch_lightning as pl
from transformers import AutoTokenizer

from config.BERT_GUG import SEED
from config.BERT_GUG.args import parser
from data.BERT_GUG.data_module import LightningGUGDataModule
from models.BERT_GUG.model import LightningBERTClassificationModel

pl.seed_everything(SEED)
parser = LightningGUGDataModule.add_args(parser)
parser = LightningBERTClassificationModel.add_args(parser)
args = parser.parse_args()

if args.gpus is not None:
    args.device = "cuda:" + args.gpus
args.best_pretrained_path = args.model_path

tokenizer = AutoTokenizer.from_pretrained(args.model_type)

lightning_data_module = LightningGUGDataModule(tokenizer, batch_size=args.batch_size, )
len_train = lightning_data_module.get_train_len()

trainer = pl.Trainer(
    default_root_dir=args.model_path,
    gpus=args.gpus,
)

dev_best_check_point_path = list(Path(args.model_path, "checkpoint").glob("es_pearsonr*"))
dev_best_check_point_path = sorted(dev_best_check_point_path, key=lambda x: str(x).split("dev_pearsonr")[1])[-1]

lightning_model = LightningBERTClassificationModel.load_from_checkpoint(checkpoint_path=str(dev_best_check_point_path))
lightning_model.tokenizer = tokenizer
lightning_model.test_pred_out = True
preds = trainer.test(model=lightning_model, test_dataloaders=lightning_data_module.test_dataloader())
print("test predicted:", preds)
