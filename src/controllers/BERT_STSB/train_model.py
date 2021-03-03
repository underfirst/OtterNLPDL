from math import ceil
from os import path
from pathlib import Path

import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping, LearningRateMonitor, ModelCheckpoint
from pytorch_lightning.loggers import WandbLogger
from transformers import AutoTokenizer
from config.BERT_STSB import SEED, GRAD_CLIP_NORM
from config.BERT_STSB.args import parser
from data.BERT_STSB.data_module import LightningSTSBDataModule
from models.BERT_STSB.model import LightningBERTClassificationModel
from utils.slack_manager import SlackManager



pl.seed_everything(SEED)
parser = LightningSTSBDataModule.add_args(parser)
parser = LightningBERTClassificationModel.add_args(parser)
args = parser.parse_args()

if args.gpus is not None:
    args.device = "cuda:" + args.gpus
args.best_pretrained_path = args.model_path

tokenizer = AutoTokenizer.from_pretrained(args.model_type)

lightning_data_module = LightningSTSBDataModule(
    tokenizer,
    batch_size=args.batch_size, )
len_train = lightning_data_module.get_train_len()

lightning_model = LightningBERTClassificationModel(
    model_type=args.model_type,
    tokneizer=tokenizer,
    num_training_step=len_train * args.num_epoch,
    best_pretrained_path=args.best_pretrained_path,
    warmup_step=args.warmup_step)

callbacks = list()
callbacks.append(EarlyStopping(monitor="dev_pearsonr",
                               patience=int(ceil(args.es_epoch * len_train / args.val_check_interval)),
                               mode="max"))
callbacks.append(LearningRateMonitor(logging_interval="step"))
callbacks.append(ModelCheckpoint(monitor="dev_pearsonr", save_top_k=1, mode="max",
                                 dirpath=path.join(args.model_path, "checkpoint"),
                                 filename="es_pearsonr-{dev_loss:.2f}-{dev_pearsonr:.2f}"))

wandb_logger = WandbLogger(
    project="BERT_STSB", name=args.experiment_name,
    tags=["BERT", "STSB"])
trainer = pl.Trainer(
    logger=wandb_logger,
    default_root_dir=args.model_path,
    callbacks=callbacks,
    gradient_clip_val=GRAD_CLIP_NORM,
    max_epochs=args.num_epoch,
    val_check_interval=args.val_check_interval,
    gpus=args.gpus,
)

try:
    trainer.fit(lightning_model,
                train_dataloader=lightning_data_module.train_dataloader(),
                val_dataloaders=lightning_data_module.val_dataloader())
except:
    import traceback

    print(traceback.format_exc())

dev_best_check_point_path = list(Path(args.model_path, "checkpoint").glob("es_pearsonr*"))
dev_best_check_point_path = sorted(dev_best_check_point_path, key=lambda x: str(x).split("dev_pearsonr")[1])[-1]

lightning_model = LightningBERTClassificationModel.load_from_checkpoint(checkpoint_path=str(dev_best_check_point_path))
trainer.test(model=lightning_model, test_dataloaders=lightning_data_module.test_dataloader())
