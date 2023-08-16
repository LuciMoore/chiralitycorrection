import os
import numpy as np
from glob import glob
import argparse
import re



def get_template_age_closest_to(age, templates_dir):
    """
    :param age: Int, participant age in months
    :param templates_dir: String, valid path to existing directory which
                          contains template image files
    :return: String, the age (or range of ages) in months closest to the
             participant's with a template image file in templates_dir
    """
    template_ages = list()
    template_ranges = dict()

    # Get list of all int ages (in months) that have template files
    for tmpl_path in glob(os.path.join(templates_dir,
                                        "*mo_template_LRmask.nii.gz")):
        tmpl_age = os.path.basename(tmpl_path).split("mo", 1)[0]
        if "-" in tmpl_age: # len(tmpl_age) <3:
            for each_age in tmpl_age.split("-"):
                template_ages.append(int(each_age))
                template_ranges[template_ages[-1]] = tmpl_age
        else:
            template_ages.append(int(tmpl_age))
    
    # Get template age closest to subject age, then return template age
    closest_age = get_age_closest_to(age, template_ages)
    return (template_ranges[closest_age] if closest_age
            in template_ranges else str(closest_age))


def get_age_closest_to(subject_age, all_ages):
    """
    :param subject_age: Int, participant's actual age in months
    :param all_ages: List of ints, each a potential participant age in months
    :return: Int, the age in all_ages which is closest to subject_age
    """
    return all_ages[np.argmin(np.abs(np.array(all_ages)-int(subject_age)))]

def choose_template(age_months):
    # Get template closest to age
    templates_dir = os.path.join('util', 'chirality_correction_templates')
    tmpl_age = get_template_age_closest_to(age_months, templates_dir)

    # for T1-and-T2 combined use T2 for <22 months otherwise T1 (img quality)
    t1or2 = 2 if int(age_months) < 22 else 1  # NOTE 22 cutoff might change


    # Paths for left & right registration
    template_anat = os.path.join(templates_dir, f"{tmpl_age}mo_T{t1or2}w_acpc_dc_restore.nii.gz")
    template_LR_mask = os.path.join(templates_dir, f"{tmpl_age}mo_template_LRmask.nii.gz")

    return t1or2, template_anat, template_LR_mask

def choose_subject_file(input_file, t1or2):
    suffix = "0000" if t1or2 == 1 else "0001"
    path_pieces = input_file.split("/")[:-1]
    matches = re.search("(sub-.*_ses-.*)\.nii\.gz", input_file).groups()
    subses = matches[0]
    subject_file = f"{subses}_{suffix}.nii.gz"
    filepath = os.path.join(*path_pieces, subject_file)
    return filepath

def parse_args():
    parser = argparse.ArgumentParser("ChooseTemplates")

    parser.add_argument(
        "input_file"
    )

    parser.add_argument(
        "age_months"
    )
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    t1or2, template_anat, template_LR_mask = choose_template(args.age_months)
    subject_file = choose_subject_file(args.input_file, t1or2)
    print(subject_file, template_anat, template_LR_mask)
