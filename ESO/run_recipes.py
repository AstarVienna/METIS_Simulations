#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

from pathlib import Path
from itertools import product

import yaml

from astar_utils import NestedMapping

from raw_script import simulate


def run():
    """Run simulations using recipes.yaml."""
    rcps = _load_recipes()
    out_dir = Path("./output/")
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

            kwargs = NestedMapping({"OBS": props})

            simulate(fname, kwargs, source=recipe["source"])


def _load_recipes() -> dict:
    with Path("recipes.yaml").open(encoding="utf-8") as file:
        return yaml.safe_load(file)


if __name__ == "__main__":
    run()
