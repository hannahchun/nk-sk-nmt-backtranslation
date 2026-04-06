#!/bin/bash
#SBATCH --job-name=nk_sk_nmt_baseline
#SBATCH --output=../output/NKtoSK/logs/train_%j.out
#SBATCH --error=../output/NKtoSK/logs/train_%j.err
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

# Run code
cd /scratch/hchun7/nk-sk-nmt-backtranslation/src

python train.py \
  --train_file ../data/bilingual/train.tsv \
  --validation_file ../data/bilingual/val.tsv \
  --default_root_dir ../output/NKtoSK \
  --gradient_clip_val 1.0 \
  --max_epochs 5 \
  --gpus 1 \
  --batch_size 4 \
  --num_workers 3

echo "End time: $(date)"