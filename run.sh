#!/bin/bash -l

#SBATCH -t 1:00:00
#SBATCH -N 1
#SBATCH --ntasks 20
#SBATCH --cpus-per-task 4
#SBATCH --mem-per-cpu 32gb
#SBATCH --mail-type=ALL
#SBATCH --mail-user=<YOUR@EMAIL.edu>
#SBATCH -o /path/to/out/%A_chir_corr.out
#SBATCH -e /path/to/out/%A_chir_corr.err
#SBATCH -J chirality-correction
#SBATCH -A feczk001

module load python

file=$1
age=$2

files=$(python step0_choose_templates.py $file $age)

./util/LR_mask_registration.sh $files
