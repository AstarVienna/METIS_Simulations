#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Blank template for simulation scripts."""

import re
import logging
import argparse
import datetime
from pathlib import Path
from itertools import product, cycle, chain
from collections.abc import Mapping


import numpy as np
from more_itertools import value_chain

from astar_utils.loggers import get_logger, ColoredFormatter
import scopesim as sim
import scopesim_templates as sim_tp
import astropy.units as u

from simulationDefinitions import *
from sources import *

logger = get_logger(__file__)

# lookup table for scopesim modes based on !OBS.type, which seems to be a
# direct relation (if it's not, change ... something)

# spoiler alert: LSS,LM maps to both lss_l and lss_m, which causes problems
# the code will run with an open filter, but defaults to lss_m; using a filter
# throws an error due to no wavelength coverate
# Current Solution: use the mode field in the YAML file directly.
# may want to error trap for invalid combinations in the future

def simulate(fname, mode, kwargs, source=None, small=False):
    """Run main function for this script."""
    logger.info("*****************************************")
    logger.info("Observation type: %s", kwargs["!OBS.type"])
    logger.debug("kwargs dict:\n%s",
                 "\n".join(f"  {k}: {v}" for k, v in kwargs.items()))
    if fname is not None:
        logger.debug("output filename: %s", fname)
    else:
        logger.warning("Output filename not set, result will not be saved.")

    if isinstance(source, Mapping):
        src_name = source["name"]
    else:
        src_name = source or SOURCEMODEDICT[kwargs["!OBS.type"]]
    src_fct, src_kwargs = SOURCEDICT[src_name]
    if isinstance(source, Mapping):
        src_kwargs |= source["kwargs"]

    # Fix units
    if "temperature" in src_kwargs and not isinstance(src_kwargs["temperature"], u.Quantity):
        src_kwargs["temperature"] <<= u.K
    if "amplitude" in src_kwargs and not isinstance(src_kwargs["amplitude"], u.Quantity):
        src_kwargs["amplitude"] <<= u.ABmag

    src = src_fct(**src_kwargs)
    logger.info("Source function: %s", src_fct.__name__)
    logger.debug("Source kwargs: %s", src_kwargs)

    # HACK: closed filter is not yet implemented
    if kwargs["!OBS.filter_name"] == "closed":
        shutter = True
        kwargs["!OBS.filter_name"] = "open"
    else:
        shutter = False

    # Fix the random number generator for now. This should ensure our data
    # is reproducible, so we can create the exact same dataset again at a
    # later date.
    kwargs["!SIM.random.seed"] = 9001

    #mode = MODESDICT[kwargs["!OBS.tech"]]
    logger.info("ScopeSim mode: %s", mode)
    # return None
    cmd = sim.UserCommands(
        use_instrument="METIS",
        set_modes=[mode],
        properties=kwargs
    )

    metis = sim.OpticalTrain(cmd)

    if small:
        # Hack to make the detectors smaller, so we can run the simulations
        # quickly in the continuous integration. For example, we want
        # ScopeSim_Data to download all the required external data, but we
        # don't care about the output.
        for key in ['detector_array', 'detector_array_list']:
            if key in metis.effects['name']:
                metis[key].table['x_size'] = 32
                metis[key].table['y_size'] = 32

    if "common_fits_keywords" not in metis.effects["name"]:
        logger.error(
            "The 'common_fits_keywords' effect was not found in the optical "
            "train, FITS header will be incomplete. Make sure you are using "
            "an up-to-date version of the METIS IRDB package!")

    metis["auto_exposure"].include = False
    if shutter:
        metis.optics_manager["METIS"].add_effect(sim.effects.Shutter())

    metis.observe(src)
    hdus = metis.readout(str(fname))
    return hdus[0]


def _expand_fnames(fnames, nreq):
    if fnames is None:
        return nreq * [None]

    fnames = [p.absolute() for p in fnames]

    if len(fnames) == 1 and not fnames[0].suffix:
        fnames[0].mkdir(parents=True, exist_ok=True)
        return nreq * [fnames[0]]

    if len(fnames) != nreq:
        raise ValueError(
            "Provide either as many output file paths or names as expanded "
            "combinations, or a single output directory.")

    is_dirs = [not p.suffix for p in fnames]
    if any(is_dirs) and not all(is_dirs):
        raise ValueError("Found some dirs and some files in output paths.")

    for path in fnames:
        if not path.suffix:
            path.mkdir(parents=True, exist_ok=True)

    return fnames


def _parse_dit(string: str):
    """Convert to float by default, but also allow simple np constructors."""
    try:
        return float(string)
    except ValueError:
        match = re.fullmatch(r"(?P<fct>\w+)\((?P<args>.+)\)", string)
        args = [int(arg) if arg.isdigit() else float(arg)
                for arg in re.findall(r"(?P<x>\w+)", match["args"])]
        func = getattr(np, match["fct"])
        # Need [] here so the iterable chaining won't eat it for breakfast
        return [func(*args)]


def _logger_setup(verbosity: int) -> None:
    loglevel = max(-10 * verbosity + logging.WARNING, logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(loglevel)
    handler.setFormatter(ColoredFormatter(False))
    logger.addHandler(handler)
    logger.setLevel(loglevel)
    logger.propagate = False


def main():
    """Call the CLI."""
    parser = argparse.ArgumentParser(
        prog="rawdata",
        description=(
            "Run METIS raw data simulations.\n\n This script allows for "
            "multiple simulations to be specified at once using the '--expand'"
            " argument. To e.g. run simulations with different integration "
            "times (but otherwise the same parameters), use '--dit 5 10 20 "
            "--expand dit'. It is also possible to expand on more than one "
            "argument, in which case all possible combinations are applied."
            " If multiple values are given for an argument, but no expand flag"
            " is set for that argument, it will be zipped instead. It is also "
            "possible to combine expanded and zipped arguments, but care must "
            "be taken regarding the order of values. It is recommended to use "
            "the maximum verbosity level ('-vv') to inspect such cases for "
            "correct argument matching."
        ),
    )

    parser.add_argument(
        "-e", "--expand",
        action="append",
        help=("Select which arguments to expand into combinations. Any other "
              "arguments with multiple values will be zipped."),
    )

    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase output verbosity.",
    )

    parser.add_argument(
        "-o", "--outpath",
        nargs="*",
        type=Path,
        help=(
            "The file name or path where the resulting fits file will be saved"
            " to. If omitted, the output will not be saved to disk. If multi"
            "ple runs are performed based on expansion of other arguments, "
            "this may be a sequence of file names, or just the output direc"
            "tory, in which case the file names will be chosen automatically. "
            "If other arguments are expanded, but only a single file name (or "
            "an unmatching number) is given here, an error will be raised."),
    )

    parser.add_argument(
        "-m", "--mode",
        nargs="*",
        type=Path,
        help=(
            "mode for instrument"),
    )

    parser.add_argument(
        "--source",
        choices=[
            "empty",
            "flat",
        ],
        help=(
            "Overrides the default sources. Currently does not allow for "
            "expansion, meaning if specified, this source will be used for all"
            " simulations of this call."),
    )

    parser.add_argument(
        "--irdb",
        default=DEFAULT_IRDB_LOCATION,
        type=Path,
        help=(
            "Location of the IRDB. By default, the script will look for it in "
            "'../IRDB/'. It is recommended to use a local clone of the IRDB "
            "repo and keep it up-to-date."),
    )

    expandables = parser.add_argument_group(
        "Expandable arguments",
        "The following arguments can be used in the '--expand' flag if "
        "multiple values are given to them.",
    )

    expandables.add_argument(
        "--filter",
        nargs="*",
        default=["open"],
        help="!OBS.filter_name keyword",
    )

    expandables.add_argument(
        "--dit",
        nargs="*",
        default=[10],
        type=_parse_dit,
        help="!OBS.dit keyword, detector integration time in seconds",
    )
    expandables.add_argument(
        "--ndit",
        nargs="*",
        default=[1],
        type=int,
        help="!OBS.ndit keyword, number of integrations",
    )

    expandables.add_argument(
        "--catg",
        nargs="*",
        default=["CALIB"],
        choices=[
            "CALIB",
        ],
        help="!OBS.catg keyword",
    )
    expandables.add_argument(
        "--tech",
        nargs="*",
        choices=[
            "IMAGE,LM",
            "IMAGE,N",
            "IFU"
        ],
        help="!OBS.tech keyword",
    )
    expandables.add_argument(
        "--type",
        nargs="*",
        choices=[
            "DARK",
            "DETLIN",
            "RSRF"
        ],
        help="!OBS.type keyword",
    )
    # if len(sys.argv) == 1:
    #     parser.print_help()

    argdict = vars(parser.parse_args())
    _logger_setup(argdict.pop("verbose"))
    # sim.rc.__config__["!SIM.file.local_packages_path"] = argdict.pop("irdb")

    expanders = argdict.pop("expand") or []
    fnames = argdict.pop("outpath")
    source = argdict.pop("source")
    mode = argdict.pop("mode")

    expdict = {arg: argdict.pop(arg) for arg in expanders}
    noexpcy = [cycle(arg) for arg in argdict.values()]
    explist = [dict(zip(chain(expdict.keys(), argdict.keys()), arg))
               for arg in (value_chain(*combo) for combo in
                           zip(product(*expdict.values()), *noexpcy))]
    n_expand = len(explist)
    logger.info("Expanding to %d combination%s",
                n_expand, "s" * (n_expand > 1))
    fnames = _expand_fnames(fnames, n_expand)

    for fname, expand in zip(fnames, explist):
        if fname is not None and not fname.suffix:
            fnamedict = {arg: expand[arg] for arg in expanders}
            expfname = ".".join(f"{k}{v}" if not isinstance(v, str)
                                else v.replace(",", ".")
                                for k, v in fnamedict.items())
            fname /= f"{expfname or 'output'}.fits"

        kwargs = argdict | expand

        props = {
            "!OBS.filter_name": kwargs["filter"],
            "!OBS.dit": kwargs["dit"],
            "!OBS.ndit": kwargs["ndit"],

            "!OBS.catg": kwargs["catg"],
            "!OBS.tech": kwargs["tech"],
            "!OBS.type": kwargs["type"],
            
            

        }

        simulate(fname, mode, props, source=source)


if __name__ == "__main__":
    main()
