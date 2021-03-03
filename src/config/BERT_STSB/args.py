from config.args import parser
from config.BERT_STSB.datapath import MODEL_PATH
from config.BERT_STSB.const import MODEL_TYPE, EXPERIMENTAL_NAME

parser.add_argument('--model_path', type=str, default=MODEL_PATH)
parser.add_argument('--model_type', type=str, default=MODEL_TYPE)
parser.add_argument('--experiment_name', type=str, default=EXPERIMENTAL_NAME)

if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
