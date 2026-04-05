import argparse
from train import KoBARTConditionalGeneration
from transformers.models.bart import BartForConditionalGeneration
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("--hparams", default=None, type=str)
parser.add_argument("--model_binary", default=None, type=str)
parser.add_argument("--output_dir", default='../output/kobart_translation_NKtoSK', type=str)
# might need to use different directory names to store the pytorch_model.bin files for the translation model

args = parser.parse_args()

with open(args.hparams) as f:
    # hparams = yaml.load(f)
    hparams = yaml.load(f, Loader = yaml.FullLoader)
    
inf = KoBARTConditionalGeneration.load_from_checkpoint(args.model_binary, hparams=hparams)

inf.model.save_pretrained(args.output_dir)
