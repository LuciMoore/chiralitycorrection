#!/usr/bin/env python

"""
This script generates a L/R mask for the nnuNet segmentation that will be used for chirality correction.
The LR masks generated will output to: LR_masks/<SUB>_<SES>

Arguments:
    input_dir: folder path to collection of asegs that require chirality correction
    prefree_anats_dir: folder that contains required prefree anat files
    t_mod: specify either T1 or T2 to LR mask registration

Usage:
  LR_mask_reg <input_dir> <prefree_anats_dir> <t_mod>
  LR_mask_reg -h | --help
Options:
  -h --help     Show this screen.
"""

import subprocess
import os
import glob
from docopt import docopt


def LR_mask_reg(input_dir, prefree_anats_dir, t_mod):
    templates_root_dir = 'util/chirality_correction_templates'

    if t_mod == 'T2': #USE T2
        templatehead = '{}/1mo_T2w_acpc_dc_restore.nii.gz'.format(templates_root_dir)
        templatemask = '{}/1mo_template_LRmask.nii.gz'.format(templates_root_dir)

    elif t_mod == 'T1': #USE T1
        templatehead = '{}/1mo_T1w_acpc_dc_restore.nii.gz'.format(templates_root_dir)
        templatemask = '{}/1mo_template_LRmask.nii.gz'.format(templates_root_dir)

    # grab list of subjects needed from aseg pre cc folder:
    os.chdir(input_dir)
    sublist = glob.glob('sub-*nii.gz')
    sublist.sort()

    # create nested LR_masks dir if it doesn't already exist
    if not os.path.exists('{}/LR_masks'.format(input_dir)):
        os.mkdir('{}/LR_masks'.format(input_dir))

    LR_mask_out_dir = '{}/LR_masks'.format(input_dir)

    for i in sublist:
        i = i.strip('.nii.gz')
        split_name = i.split("_", 2)
        sub = split_name[0]
        ses = split_name[1]
        subses = split_name[0] + '_' + split_name[1]

        if not os.path.exists('{}/{}'.format(prefree_anats_dir, subses)):
            print('Prefree anats for {} are missing'.format(subses))

        else:
            sub_LR_mask_dir = '{}/{}'.format(LR_mask_out_dir, subses)
            if os.path.exists('{}/{}/LRmask.nii.gz'.format(LR_mask_out_dir, subses)):
                print('LR mask for {} already exists - skipping'.format(subses))

            else:
                if not os.path.exists('{}'.format(sub_LR_mask_dir)):
                    os.mkdir('{}'.format(sub_LR_mask_dir))

                #define subject anatomical file to use for registration
                if t_mod == 'T2': #USE T2
                    sub_anat = '{}/{}/T2w_acpc_dc_restore.nii.gz'.format(prefree_anats_dir, subses)

                elif t_mod == 'T1':  # USE T1
                    sub_anat = '{}/{}/T1w_acpc_dc_restore.nii.gz'.format(prefree_anats_dir, subses)

                os.chdir('{}'.format(sub_LR_mask_dir))

                sbatch = 'sbatch --job-name {} --cpus-per-task 4 --mem-per-cpu 60GB --time 36:00:00 ' \
                         '--output {}/ANTS.out --error {}/ANTS.err ' \
                         'util/LR_mask_registration.sh ' \
                         '{} {} {}'.format(subses,
                                           sub_LR_mask_dir, sub_LR_mask_dir,
                                           sub_anat, templatehead, templatemask)
                print(sbatch)
                subprocess.run(sbatch, shell=True)

if __name__ == '__main__':
    args = docopt(__doc__)
    LR_mask_reg(args['<input_dir>'], args['<prefree_anats_dir>'], args['<t_mod>'])
