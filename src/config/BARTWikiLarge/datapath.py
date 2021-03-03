from os import path

from config.datapath import *

MODEL_PATH = path.join(PROJECT_TOP, "models", "BARTWikiLarge")
REINFORCEMENT_MODEL_PATH = path.join(PROJECT_TOP, "models", "BARTWikiLarge", "reinforcement")

RAW_RESOURCE_PATH = path.join(DATAPATH, "raw", "wikilarge")
RAW_WIKIAUTO_TRAIN_PATH = path.join(DATAPATH, "raw", "wikiauto")
PROCESSED_WIKIMEDIUM_RESOURCE_PATH = path.join(DATAPATH, "processed", "wikimedium")

if __name__ == '__main__':
    print(MODEL_PATH)