import argparse

from config.const import (BEST_MODEL_FOLDER_PREFIX, DEVICE, DEVICE_NUMBER,
                          ES_EPOCH, ES_METRIC, EVAL_AT, LIMIT_TRAIN_BATCHES,
                          LIMIT_VAL_BATCHES, META_DEFAULT_STR, NUM_EPOCH)

parser = argparse.ArgumentParser(conflict_handler="resolve")

# default definition
parser.add_argument('--num_epoch', type=int, default=NUM_EPOCH)
parser.add_argument('--es_epoch', type=int, default=ES_EPOCH)
parser.add_argument('--device',  type=str, default=DEVICE)
parser.add_argument('--best_model_folder_prefix', type=str, default=BEST_MODEL_FOLDER_PREFIX)
parser.add_argument('--es_metric', type=str, default=ES_METRIC)

parser.add_argument('--experiment_name', type=str, default="")
parser.add_argument('--server_name', type=str, default="laptop")

# defaultがコードによって異なる項目
parser.add_argument('--model_path', type=str, default=META_DEFAULT_STR)
parser.add_argument('--tensorboard_path', type=str, default=META_DEFAULT_STR)
parser.add_argument('--eval_temp_folder', type=str, default=META_DEFAULT_STR)


# lightning model parameter
parser.add_argument('--val_check_interval', default=EVAL_AT, type=int)
parser.add_argument('--limit_train_batches', default=LIMIT_TRAIN_BATCHES, type=int)
parser.add_argument('--limit_val_batches', default=LIMIT_VAL_BATCHES, type=int)
parser.add_argument('--gpus', default=DEVICE_NUMBER)
