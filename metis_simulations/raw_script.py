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

from .simulationDefinitions import *
from .sources import *
import os
DEFAULT_IRDB_LOCATION = os.environ["DEFAULT_IRDB_LOCATION"]
sim.rc.__config__["!SIM.file.local_packages_path"] = DEFAULT_IRDB_LOCATION

logger = get_logger(__file__)

# lookup table for scopesim modes based on !OBS.type, which seems to be a
# direct relation (if it's not, change ... something)

# spoiler alert: LSS,LM maps to both lss_l and lss_m, which causes problems
# the code will run with an open filter, but defaults to lss_m; using a filter
# throws an error due to no wavelength coverate
# Current Solution: use the mode field in the YAML file directly.
# may want to error trap for invalid combinations in the future

def simulate(fname, mode, kwargs, wcu, source=None, small=False):

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

    # HACK: closed filter is not yet implemented:
    # changed the hack below, because changing kwargs here changes the props dictionary from which
    # kwargs is generated, outside of this subroutine, for reasons I do not understant.
    
    #if kwargs["!OBS.filter_name"] == "closed":
    #    shutter = True
    #    kwargs["!OBS.filter_name"] = "open"
    #else:
    #    shutter = False

    #mode = MODESDICT[kwargs["!OBS.tech"]]
    logger.info("ScopeSim mode: %s", mode)
    # return None

    #changed the way the simulation is called, because the previous method wasn't
    #producing expeced results

    
    #set up the simulation
    if("wavelen" in kwargs["OBS"].keys()):
        cmd = sim.UserCommands(use_instrument="METIS", set_modes=[mode],properties={"!OBS.wavelen": kwargs["OBS"]['wavelen']})
    else:
        cmd = sim.UserCommands(use_instrument="METIS", set_modes=[mode])

    #copy over the OBS settings directly, then set up the optical train

    shutter = False
    cmd["!OBS.catg"] = kwargs["OBS"]["catg"]
    cmd["!OBS.type"] = kwargs["OBS"]["type"]
    cmd["!OBS.tech"] = kwargs["OBS"]["tech"]
    cmd["!OBS.mjd-obs"] = kwargs["OBS"]["MJD-OBS"]
    cmd["!OBS.dateobs"] = kwargs["OBS"]["dateobs"]
    cmd["!OBS.ndfilter_name"] = kwargs["OBS"]["ndfilter_name"]
    cmd["!OBS.filter_name"] = kwargs["OBS"]["filter_name"]
    if kwargs["!OBS.filter_name"] == "closed":
        cmd["!OBS.filter_name"] = "open"
        shutter = True


    if("tplname" in kwargs["OBS"].keys()):
        cmd["!OBS.tplname"] = kwargs["OBS"]["tplname"]


    metis = sim.OpticalTrain(cmd)

    
    #set the WCU mode arguments
    if(wcu is not None):
        allargs = wcu
        if(np.all(["bb_temp" in allargs,"is_temp" in allargs, "wcu_temp" in allargs])):
            metis['wcu_source'].set_temperature(bb_temp=allargs['bb_temp']*u.K, is_temp=allargs['is_temp']*u.K,wcu_temp=allargs['wcu_temp']*u.K)
        if("current_fpmask" in allargs):
            if("xshift") in allargs:
                metis['wcu_source'].set_fpmask(allargs['current_fpmask'],shift=(allargs['xshift'],allargs['yshift']))
            else:
                metis['wcu_source'].set_fpmask(allargs['current_fpmask'])

        if("bb_aperture" in allargs):
            metis['wcu_source'].set_bb_aperture(allargs['bb_aperture'])


            

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


    #metis["auto_exposure"].include = False
    if shutter:
        metis.optics_manager["METIS"].add_effect(sim.effects.Shutter())

    # now observe and readout
    metis.observe(src)
    hdus = metis.readout(dit=kwargs["OBS"]['dit'],ndit=kwargs["OBS"]['ndit'])
    
    hdus[0][0].header['HIERARCH ESO DPR TECH'] = kwargs["OBS"]["tech"]
    hdus[0].writeto(fname,overwrite=True)
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


