#!/bin/bash -l

#SBATCH -t 1:00:00
#SBATCH -N 1
#SBATCH --ntasks 4
#SBATCH --mem=60gb
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lmoore@umn.edu
#SBATCH -o /home/feczk001/shared/projects/nnUNet_s3_wrapper/chiralitycorrection/logs/%A_chir_corr.out
#SBATCH -e /home/feczk001/shared/projects/nnUNet_s3_wrapper/chiralitycorrection/logs/%A_chir_corr.err
#SBATCH -J chirality-correction
#SBATCH -A feczk001

SubjectHead=$1;shift
TemplateHead=$1;shift
TemplateMask=$1;shift

module load ants

bn=$(basename "$SubjectHead")
sub=`echo $bn | awk -F '_' '{print $1}'`
ses=`echo $bn | awk -F '_' '{print $2}'`
echo ${sub}_${ses}

WD="./wd_${sub}_${ses}"
mkdir "$WD"

# Register the template head to the subject head
ANTS 3 -m CC["$SubjectHead","$TemplateHead",1,5] -t SyN[0.25] -r Gauss[3,0] -o "$WD"/antsreg -i 60x50x20 --use-Histogram-Matching  --number-of-affine-iterations 10000x10000x10000x10000x10000 --MI-option 32x16000

# Apply resulting transformation to template L/R mask to generate subject L/R mask
antsApplyTransforms -d 3 \
        --output ${sub}_${ses}_LRmask.nii.gz \
        --reference-image "$SubjectHead" \
        --transform "$WD"/antsregWarp.nii.gz "$WD"/antsregAffine.txt \
        --input "$TemplateMask" \
	--interpolation NearestNeighbor

#delete wd
rm -r "$WD"
