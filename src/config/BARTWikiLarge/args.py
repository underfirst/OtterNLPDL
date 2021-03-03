import argparse

from config.args import parser
from config.BARTWikiLarge.const import (BEST_MODEL_FOLDER_PREFIX, ES_EPOCH,
                                        ES_METRIC, EXPERIMENTAL_NAME,
                                        MODEL_TYPE)
from config.BARTWikiLarge.datapath import MODEL_PATH

parser = argparse.ArgumentParser(parents=[parser], add_help=False, conflict_handler="resolve")

parser.add_argument('--model_path', type=str, default=MODEL_PATH)
parser.add_argument('--model_type', type=str, default=MODEL_TYPE)
parser.add_argument('--es_metric', type=str, default=ES_METRIC)
parser.add_argument('--es_epoch', type=int, default=ES_EPOCH)
parser.add_argument('--best_model_folder_prefix', type=str, default=BEST_MODEL_FOLDER_PREFIX)
parser.add_argument('--experiment_name', type=str, default=EXPERIMENTAL_NAME)

if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
