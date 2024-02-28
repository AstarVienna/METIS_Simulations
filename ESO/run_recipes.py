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
    ]

    for name, recipe in rcps.items():
        expanded = [key for key in expandables
                    if isinstance(recipe["properties"][key], list)]
        combos = product(*[recipe["properties"][key] for key in expanded])

        for combo in combos:
            combodict = dict(zip(expanded, combo))
            expfname = "-".join(f"{k}{v}" if not isinstance(v, str)
                                else v.replace(",", ".")
                                for k, v in combodict.items())
            fname = '-'.join([name, expfname]) if expfname else name
            fname = out_dir / f"{fname}.fits"

            kwargs = NestedMapping({"OBS": recipe["properties"] | combodict})

            simulate(fname, kwargs, source=recipe["source"])


def _load_recipes() -> dict:
    with Path("recipes.yaml").open(encoding="utf-8") as file:
        return yaml.full_load(file)


if __name__ == "__main__":
    run()
