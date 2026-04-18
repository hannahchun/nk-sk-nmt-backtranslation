#!/bin/bash
#SBATCH --job-name=bertscore_%x
#SBATCH --output=../output/Evaluation/logs/bertscore_%x_%j.out
#SBATCH --error=../output/Evaluation/logs/bertscore_%x_%j.err
#SBATCH --time=10:00:00
#SBATCH --mem=16G
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1

SCALE=$1

echo "Scale: $SCALE"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $(hostname)"
echo "Start time: $(date)"

# Activate environment
eval "$(conda shell.bash hook)"
conda activate DSCC451Project

echo "Python: $(which python)"
echo "Conda env: $CONDA_DEFAULT_ENV"

# Move to working dir
cd /scratch/hchun7/nk-sk-nmt-backtranslation

# Run BERTScore
bert-score \
  -r ../data/translation_results_text/aug_${SCALE}x_ref_nk_to_sk_test.txt \
  -c ../data/translation_results_text/aug_${SCALE}x_cand_nk_to_sk_test.txt \
  --lang ko \

echo "End time: $(date)"