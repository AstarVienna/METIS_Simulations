#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""."""

from pathlib import Path
from itertools import product

import yaml
import argparse
from pathlib import Path
import os
from astar_utils import NestedMapping

from raw_script import simulate


def run(inputYAML,outputDir):
    """Run simulations using recipes.yaml."""

    rcps = _load_recipes(inputYAML)

    out_dir = Path(outputDir)
    
    out_dir.mkdir(parents=True, exist_ok=True)

    expandables = [
        "dit",
        "mjdobs",
    ]

    for name, recipe in rcps.items():
        expanded = [key for key in expandables
                    if isinstance(recipe["properties"][key], list)]
        combos = product(*[recipe["properties"][key] for key in expanded])

        for combo in combos:
            combodict = dict(zip(expanded, combo))
            props = recipe["properties"] | combodict
            
            # Create a filename that resembles that of the real data.
            # The filenames from the ICS software will probably look like
            #     METIS.2024-02-29T01:23:45.678.fits
            # However, this has two drawbacks:
            # - There are colons that cannot be used in Windows filenames.
            # - They don't contain any information about the type of file.
            # Therefor the colons are replaced and extra information is added.
            # The resulting filenames look like
            #     METIS.2024-01-02T03_45_00.DETLIN_LM_RAW-dit1.0.fits
            sdate = props["mjdobs"].isoformat()
            # Replace colon so the date can be in Windows filenames.
            sdate = sdate.replace(":", "_")
            expfname = "-".join(f"{k}{v}" if not isinstance(v, str)
                            else v.replace(",", ".")
                            for k, v in combodict.items()
                            if k not in {"mjdobs"})
            fname = '-'.join([name, expfname]) if expfname else name
            fname = f"METIS.{sdate}.{fname}"
            fname = out_dir / f"{fname}.fits"
            print("fname=",fname)
            kwargs = NestedMapping({"OBS": props})

            simulate(fname, kwargs, source=recipe["source"])


def _load_recipes(inputYAML) -> dict:
    
    with Path(inputYAML).open(encoding="utf-8") as file:
        return yaml.safe_load(file)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--inputYAML', type=str,
                    help='input YAML File')
    parser.add_argument('--outputDir', type=str, 
                    help='output directory')
    
    args = parser.parse_args()
    print(args)
    if(args.inputYAML):
        inputYAML = args.inputYAML
    else:
        inputYAML = Path(__file__).parent / "recipes.yaml"
    if(args.outputDir):
        outputDir = args.outputDir
    else:
        outputDir = Path(__file__).parent / "output/"
    
    print(inputYAML,outputDir)
    run(inputYAML,outputDir)

    
