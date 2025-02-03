"""Compare the main yaml file against the DRLD.

First install the DRLD with
METIS_DRLD> pip install -e .
"""

import sys
import yaml
from pathlib import Path

from codes.drld_parser.data_reduction_library_design import METIS_DataReductionLibraryDesign

import simulationDefinitions

HACK_RAWS_THAT_SHOULD_BE_ADDED_TO_THE_DRLD = {
    'N_IMAGE_SKY_RAW',
    'LM_IMAGE_SKY_RAW',
    'N_LSS_SKY_RAW',
    'LM_LSS_SKY_RAW',
    'IFU_RSRF_PINH_RAW',
}

HACK_RAW_TEMPLATE_COMBINATIONS_THAT_SHOULD_BE_ADDED_TO_THE_DRLD = {
    ("IFU_SKY_RAW", "metis_ifu_cal_standard"),
}

def compareYAML(argv):
    
    PATH_HERE = Path(__file__).parent
    
    if len(sys.argv) == 1:
        filename_yaml = PATH_HERE / 'YAML/recipes.yaml'
    else:
        filename_yaml = argv[1]
    
    with open(filename_yaml) as f:
        recipes = yaml.safe_load(f)
    
    dicts_from_sim_defs = {
        k: v
        for k, v in simulationDefinitions.__dict__.items()
        if k.upper() == k and isinstance(v, dict) and "do.catg" in v
    }
    
    problems = []
    for name, settings in recipes.items():
        do_catg = settings['do.catg']
        # assert name.startswith(do_catg)
        if do_catg not in METIS_DataReductionLibraryDesign.dataitems:
            if do_catg not in HACK_RAWS_THAT_SHOULD_BE_ADDED_TO_THE_DRLD:
                problems.append(f"Cannot find {do_catg} in METIS_DataReductionLibraryDesign!")
            continue
        di = METIS_DataReductionLibraryDesign.dataitems[do_catg]
        props = settings['properties']
        if props['catg'] != di.dpr_catg:
            problems.append(f"{do_catg} has DPR.CATG {props['catg']} in yaml but {di.dpr_catg} in DRLD")
        # Workaround for special yaml_tech values that
        # are fixed through updateHeaders() in runRecipes.py
        yaml_tech = props['tech']
        if yaml_tech in ["RAVC,LM", "APP,LM"]:
            yaml_tech = "IMAGE,LM"
        if yaml_tech in ["RAVC,IFU", "LMS"]:
            yaml_tech = "IFU"
        if yaml_tech != di.dpr_tech:
            problems.append(f"{do_catg} has DPR.TECH {props['tech']} in yaml but {di.dpr_tech} in DRLD")
        if props['type'] != di.dpr_type:
            problems.append(f"{do_catg} has DPR.TYPE {props['type']} in yaml but {di.dpr_type} in DRLD")
    
        tplname = props["tplname"].lower()
        if tplname not in di.templates:
            if (do_catg, tplname) not in HACK_RAW_TEMPLATE_COMBINATIONS_THAT_SHOULD_BE_ADDED_TO_THE_DRLD:
                problems.append(f"{do_catg} has tplname {tplname} but only {di.templates} create it")
    
    do_catg_used_in_yaml = {
        settings['do.catg']
        for settings in list(recipes.values()) + list(dicts_from_sim_defs.values())
    }
    do_catg_used_in_drld = {a for a in METIS_DataReductionLibraryDesign.dataitems if a.endswith("_RAW")}
    do_catg_only_in_yaml = do_catg_used_in_yaml - do_catg_used_in_drld - HACK_RAWS_THAT_SHOULD_BE_ADDED_TO_THE_DRLD
    do_catg_only_in_drld = do_catg_used_in_drld - do_catg_used_in_yaml
    if do_catg_only_in_yaml:
        problems.append(f"DO.CATG values only used in yaml file but not in the DRLD: {do_catg_only_in_yaml}")
    if do_catg_only_in_drld:
        problems.append(f"DO.CATG values only used in drld but not in the yaml file: {do_catg_only_in_drld}")
    
    for problem in problems:
        print(problem)
    
    assert not problems, "Found problems, see output above."

if __name__ == "__main__":
    
    compareYAML(sys.argv)
