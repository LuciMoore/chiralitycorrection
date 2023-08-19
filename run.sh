#!/bin/bash -l

#SBATCH -t 1:00:00
#SBATCH -N 1
#SBATCH --ntasks 20
#SBATCH --mem=80gb
#SBATCH -p v100
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lmoore@umn.edu
#SBATCH -o /home/feczk001/shared/projects/chir_corr/logs/%A_chir_corr.out
#SBATCH -e /home/feczk001/shared/projects/chir_corr/logs/%A_chir_corr.err
#SBATCH -J chirality-correction
#SBATCH -A feczk001

module load python

file=$1
age=$2

files=$(python step0_choose_templates.py $file $age)

./util/LR_mask_registration.sh $files
