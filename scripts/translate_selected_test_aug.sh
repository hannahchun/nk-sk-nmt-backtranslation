#!/bin/bash
#SBATCH --job-name=nk_to_sk_aug
#SBATCH --output=../output/QualitativeAnalysis/logs/infer_%x_%j.out
#SBATCH --error=../output/QualitativeAnalysis/logs/infer_%x_%j.err
#SBATCH --time=04:00:00
#SBATCH --mem=16G
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1

MODEL_NAME=$1

echo "Model: $MODEL_NAME"

# Activate environment
eval "$(conda shell.bash hook)"
conda activate DSCC451Project

cd /scratch/hchun7/nk-sk-nmt-backtranslation/src

python translate_test.py \
  --input_file ../data/qualitative_analysis/selected_test.tsv \
  --output_file ../data/qualitative_analysis/${MODEL_NAME}_nk_to_sk_selected_test.tsv \
  --model_path ../output/NKtoSK/augmented_bilingual/${MODEL_NAME}/kobart_translation-model_final \
  --batch_size 16 \
  --max_length 128 \
  --num_beams 5