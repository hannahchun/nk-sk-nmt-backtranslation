#!/bin/bash
#SBATCH --job-name=nk_to_sk_aug
#SBATCH --output=../output/TranslationTest/logs/infer_%x_%j.out
#SBATCH --error=../output/TranslationTest/logs/infer_%x_%j.err
#SBATCH --time=10:00:00
#SBATCH --mem=16G
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1

MODEL_SCALE=$1 

# Print job info
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $(hostname)"
echo "Start time: $(date)"
echo "Model scale: $MODEL_SCALE"

# Activate conda
eval "$(conda shell.bash hook)"
conda activate DSCC451Project

echo "Python: $(which python)"
echo "Conda env: $CONDA_DEFAULT_ENV"

# Move to src
cd /scratch/hchun7/nk-sk-nmt-backtranslation/src

# Run translation (NK -> SK)
python translate_test.py \
  --input_file ../data/bilingual/filtered/test_filtered.tsv \
  --output_file ../data/translation_results/aug_${MODEL_SCALE}x_nk_to_sk_test.tsv \
  --model_path ../output/NKtoSK/augmented_bilingual/aug_${MODEL_SCALE}x/kobart_translation-model_final \
  --batch_size 16 \
  --max_length 128 \
  --num_beams 5

echo "End time: $(date)"
