from os import path

from utils.search_project_top import search_project_top

PROJECT_TOP = search_project_top(__file__)  # .project_topファイルがある場所を探して, そこをproject topにしてくれる.
DATA_PATH = path.join(PROJECT_TOP, "data")
MODEL_PATH = path.join(PROJECT_TOP, "models")
RAW_ASSET_PATH = path.join(DATA_PATH, "raw", "asset", "dataset")  # TODO: 例としてasset
BLEU_SH_PATH = path.join(PROJECT_TOP, "external_tools", "bleu.sh")