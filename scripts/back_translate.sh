#!/bin/bash
#SBATCH --job-name=sk_to_nk_backtranslate
#SBATCH --output=../output/BackTranslation/synthetic_data/logs/infer_%j.out
#SBATCH --error=../output/BackTranslation/synthetic_data/logs/infer_%j.err
#SBATCH --time=20:00:00
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

# Run back-translation script
python back_translate.py \
  --input_file ../data/monolingual/SK/original/original_monolingual_sk_shuffled.tsv \
  --output_file ../data/synthetic/synthetic_sk_to_nk.tsv \
  --model_path ../output/SKtoNK/filtered_bilingual/kobart_translation-model_final \
  --batch_size 16 \
  --max_length 128 \
  --num_beams 5

echo "End time: $(date)"