#!/bin/bash
#SBATCH --job-name=nk_sk_augmented
#SBATCH --output=../output/NKtoSK/augmented_bilingual/logs/train_%x_%j.out
#SBATCH --error=../output/NKtoSK/augmented_bilingual/logs/train_%x_%j.err
#SBATCH --time=60:00:00
#SBATCH --mem=16G
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1

SCALE=$1

echo "Scale: $SCALE"

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

# Run code
cd /scratch/hchun7/nk-sk-nmt-backtranslation/src

python train.py \
  --train_file ../data/bilingual/augmented/train_augmented_${SCALE}.tsv \
  --validation_file ../data/bilingual/filtered/val_filtered.tsv \
  --default_root_dir ../output/NKtoSK/augmented_bilingual/aug_${SCALE} \
  --gradient_clip_val 1.0 \
  --max_epochs 5 \
  --gpus 1 \
  --batch_size 4 \
  --num_workers 3

echo "End time: $(date)"
