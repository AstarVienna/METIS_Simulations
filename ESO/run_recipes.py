#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""."""

from pathlib import Path
from itertools import product
import argparse

import yaml

from astar_utils import NestedMapping

def run(inputYAML, outputDir, small=False, catglist=None):
    """Run simulations using recipes.yaml."""

    allrcps = _load_recipes(inputYAML)

    if catglist is None:
        dorcps = allrcps
    else:
        dorcps = {}
        for catg in catglist:
            if catg in allrcps.keys():
                dorcps[catg] = allrcps[catg]
            else:
                raise ValueError(f"ERROR: {catg} is not a supported product category")

    # This import is executed here to defer downloading irdb packages
    # until we know they're needed
    from raw_script import simulate

    out_dir = Path(outputDir)
    out_dir.mkdir(parents=True, exist_ok=True)

    expandables = [
        "dit",
        "mjdobs",
    ]

    for name, recipe in dorcps.items():
        expanded = [key for key in expandables
                    if isinstance(recipe["properties"][key], list)]
        combos = product(*[recipe["properties"][key] for key in expanded])
        mode = recipe["mode"]
        prefix = recipe["prefix"]
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
            fname = '-'.join([prefix, expfname]) if expfname else prefix
            fname = f"METIS.{sdate}.{fname}"
            fname = out_dir / f"{fname}.fits"
            print("fname=",fname)
            kwargs = NestedMapping({"OBS": props})

            simulate(fname, mode, kwargs, source=recipe["source"], small=small)


def _load_recipes(inputYAML) -> dict:

    with Path(inputYAML).open(encoding="utf-8") as file:
        return yaml.safe_load(file)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--inputYAML', type=str,
                        help='input YAML File')
    parser.add_argument('-o', '--outputDir', type=str,
                        help='output directory')
    parser.add_argument('-s', '--small', type=bool,
                        default=False,
                        help=('use detectors of 32x32 pixels; ' +
                              'for running in the continuous integration'))
    parser.add_argument('-c', '--catg', type=str,
                        help='comma-separated list of selected output file categories')

    args = parser.parse_args()
    print(args)

    if args.inputYAML:
        inputYAML = args.inputYAML
    else:
        inputYAML = Path(__file__).parent / "recipes.yaml"

    if args.outputDir:
        outputDir = args.outputDir
    else:
        outputDir = Path(__file__).parent / "output/"

    small = args.small

    if args.procatg:
        catglist = args.procatg.split(',')
    else:
        catglist = None

    print(inputYAML, outputDir, small, catglist)
    run(inputYAML, outputDir, small, catglist)
