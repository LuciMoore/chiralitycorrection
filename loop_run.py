
import step0_choose_templates
import os

aseg_dir='/home/feczk001/shared/projects/chir_corr/subject_data'
age_months=12
input_file='/home/feczk001/shared/projects/chir_corr/subject_data/sub-011228_ses-12mo.nii.gz'
code_dir='/home/feczk001/shared/projects/nnUNet_s3_wrapper/chiralitycorrection/util'

t1or2, template_anat, template_LR_mask = step0_choose_templates.choose_template(age_months)
subject_file = step0_choose_templates.choose_subject_file(input_file, t1or2)
print(subject_file, template_anat, template_LR_mask)
subject_file=os.path.join('/', subject_file)

os.system('sbatch {}/LR_mask_reg_sbatch.sh {} {} {}'.format(code_dir, subject_file, template_anat, template_LR_mask))