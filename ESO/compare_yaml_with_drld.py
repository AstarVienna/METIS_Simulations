"""Compare the main yaml file against the DRLD.

First install the DRLD with
METIS_DRLD> pip install -e .
"""

import sys
import yaml
from pathlib import Path

from codes.drld_parser.data_reduction_library_design import METIS_DataReductionLibraryDesign

PATH_HERE = Path(__file__).parent

if len(sys.argv) == 1:
    filename_yaml = PATH_HERE / 'recipes.yaml'
else:
    filename_yaml = sys.argv[1]

with open(filename_yaml) as f:
    recipes = yaml.safe_load(f)

problems = []
for name, settings in recipes.items():
    do_catg = settings['prefix']
    # assert name.startswith(do_catg)
    if do_catg not in METIS_DataReductionLibraryDesign.dataitems:
        problems.append(f"Cannot find {do_catg} in METIS_DataReductionLibraryDesign!")
        continue
    di = METIS_DataReductionLibraryDesign.dataitems[do_catg]
    props = settings['properties']
    if props['catg'] != di.dpr_catg:
        problems.append(f"{do_catg} has DPR.CATG {props['catg']} in yaml but {di.dpr_catg} in DRLD")
    if props['tech'] != di.dpr_tech:
        problems.append(f"{do_catg} has DPR.TECH {props['tech']} in yaml but {di.dpr_tech} in DRLD")
    if props['type'] != di.dpr_type:
        problems.append(f"{do_catg} has DPR.TYPE {props['type']} in yaml but {di.dpr_type} in DRLD")

for problem in problems:
    print(problem)

assert not problems, "Found problems, see output above."