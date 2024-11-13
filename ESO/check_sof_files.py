#!/usr/bin/env python
"""Check SOF files.

First install the DRLD with
METIS_DRLD> pip install -e .

But that does not always work (TODO: fix), so you can also specify the
Python path:
export PYTHONPATH=/path/to/METIS_DRLD/codes
"""
from pathlib import Path
from codes.drld_parser.data_reduction_library_design import METIS_DataReductionLibraryDesign


PATH_HERE = Path(__file__).parent
PATH_FITS = PATH_HERE / "output"


def check_sof_file(filename, problems_raws, problems_tags, problems_names, problems_input):
    # E.g. "metis_lm_img_flat.twilight.sof" -> "metis_lm_img_flat"
    recipe_name = filename.stem.split(".")[0]
    assert recipe_name in METIS_DataReductionLibraryDesign.recipes, (f"{recipe_name} not found in "
                                                                     f"METIS_DataReductionLibraryDesign")
    recipe = METIS_DataReductionLibraryDesign.recipes[recipe_name]

    lines1 = open(filename, mode="r", encoding="utf-8").readlines()
    lines = [
        [a.split("/")[-1] for a in line.split()]
        for line in lines1
    ]

    # Check whether tags are in the DRLD.
    tags = [tag for _, tag in lines]
    tags_missing = [
        tag for tag in tags
        if tag not in METIS_DataReductionLibraryDesign.dataitems
    ]
    if tags_missing:
        problems_tags.append((filename.name, tags_missing))

    # Check whether the tag is in the filename.
    filenames_without_tags = [
        fn
        for fn, tag in lines
        if tag not in fn
    ]
    if filenames_without_tags:
        problems_names.append((filename.name, filenames_without_tags))

    # Check whether raws exist.
    fns_raw = [
        fn
        for fn, tag in lines
        if "RAW" in tag
    ]
    fns_raw_missing = [
        fn
        for fn in fns_raw
        if not (PATH_FITS / fn).exists()
    ]
    if fns_raw_missing:
        problems_raws.append((filename.name, fns_raw_missing))

    # Check whether files mentioned in SOF files are actually input to the recipes.
    tags_input_to_recipe = [di.name for di in recipe.input_data]
    tags_not_input_to_recipe_according_to_drld = [
        tag for tag in tags
        if tag not in tags_input_to_recipe
    ]
    if tags_not_input_to_recipe_according_to_drld:
        problems_input.append((filename.name, tags_not_input_to_recipe_according_to_drld))


def check_sof_directory(directory, check_files_existing=True):
    problems_raws = []
    problems_tags = []
    problems_names = []
    problems_input = []

    for filename in directory.glob("*.sof"):
        if "persistence" in filename.name:
            continue
        check_sof_file(filename, problems_raws, problems_tags, problems_names, problems_input)

    if problems_raws and check_files_existing:
        print("Some RAW files are missing:")
        for fn_sof, fns_missing in problems_raws:
            print("-", fn_sof)
            for fn in fns_missing:
                print("  -", fn)

    print()
    if problems_tags:
        print("Some tags are not in the DRLD:")
        for fn_sof, fns_missing in problems_tags:
            print("-", fn_sof)
            for fn in fns_missing:
                print("  -", fn)

    print()
    if problems_names:
        print("Some filenames do not contain the tag:")
        for fn_sof, fns_missing in problems_names:
            print("-", fn_sof)
            for fn in fns_missing:
                print("  -", fn)

    print()
    if problems_input:
        print("Some tags in SOF files are not actually input to the recipe:")
        for fn_sof, tags_not_input in problems_input:
            print("-", fn_sof)
            for fn in tags_not_input:
                print("  -", fn)

    if problems_raws or problems_tags:
        return False
    return True


def main():
    PATH_SOFS = PATH_HERE / "sofFiles"
    PATH_TEMPLATES = PATH_HERE / "sofTemplates"

    print("Doing the SOF files.")
    sofs_ok = check_sof_directory(PATH_SOFS)

    print()
    print("Doing the Templates.")
    templates_ok = check_sof_directory(PATH_TEMPLATES, check_files_existing=False)

    return sofs_ok and templates_ok

if __name__ == "__main__":
    all_ok = main()
    if not all_ok:
        exit(1)
