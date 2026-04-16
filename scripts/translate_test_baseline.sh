#!/bin/bash
#SBATCH --job-name=nk_to_sk_translate_test_baseline
#SBATCH --output=../output/TranslationTest/logs/infer_%j.out
#SBATCH --error=../output/TranslationTest/logs/infer_%j.err
#SBATCH --time=10:00:00
#SBATCH --mem=16G
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1

# Print job info
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $(hostname)"
echo "Start time: $(date)"

# Activate conda
eval "$(conda shell.bash hook)"
echo "conda initialized"
conda activate DSCC451Project
echo "environment activated"

# Verify environment
echo "Python: $(which python)"
echo "Conda env: $CONDA_DEFAULT_ENV"

# Move to src directory
cd /scratch/hchun7/nk-sk-nmt-backtranslation/src

# Run translation script
python translate_test.py \
  --input_file ../data/bilingual/filtered/test_filtered.tsv \
  --output_file ../data/translation_results/baseline_nk_to_sk_test.tsv \
  --model_path ../output/NKtoSK/filtered_bilingual/kobart_translation-model_final \
  --batch_size 16 \
  --max_length 128 \
  --num_beams 5

echo "End time: $(date)"