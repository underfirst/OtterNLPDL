from utils.set_local_const import set_local_const

MODEL_TYPE = "bert-base-uncased"

DO_LOWER_CASE = False
WEIGHT_DECAY = 0.01  # 1.0e-06  # 0.5
MAX_GRAD_NORM = 5.0  # 5.0
GRAD_CLIP_NORM = MAX_GRAD_NORM
DROPOUT_RATIO = 0.1  # 0.5

BATCH_SIZE = 32
NUM_EPOCH = 100
ES_EPOCH = 5

EVAL_AT = set_local_const(100, 2)
LIMIT_TRAIN_BATCHES = set_local_const(1.0, 4)
LIMIT_VAL_BATCHES = set_local_const(1.0, 4)

DEVICE = set_local_const("cuda:1", "cpu")
DEVICE_NUMBER = None if DEVICE == "cpu" else DEVICE.replace("cuda:", "")

ES_METRIC = "dev_bleu"
BEST_MODEL_FOLDER_PREFIX = "es_eval_pearsonr"  # 2版がクソゴミ

DEFAULT_LEARNING_RATE = 2e-5  # 5e-5, 3e-5, 2e-5
ADAM_EPSILON = 1e-8
WARMUP_STEP = 1000

CACHE_EXT = ".cache"
META_DEFAULT_INT = 202005041749
META_DEFAULT_STR = "META_DEFAULT_STR"
SEED = 0

DEBUG_FLG = False
DEFAULT_BEAM_SIZE = 1
