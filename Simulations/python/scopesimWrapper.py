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
#sim.rc.__config__["!SIM.file.local_packages_path"] = DEFAULT_IRDB_LOCATION

logger = get_logger(__file__)

# HACK: closed filter is not yet implemented:
# changed the hack below, because changing kwargs here changes the props dictionary from which
# kwargs is generated, outside of this subroutine, for reasons I do not understant.

def simulate(fname, rcp, small=False):

    """
    Workhorse for an individual simulation.
    
    """

    props = rcp["properties"]
    wcu = rcp["wcu"]
    source = rcp["source"]

    
    # some massaging of the source object, to get into the right
    # format and units
    
    if isinstance(source, Mapping):
        src_name = source["name"]
    else:
        src_name = source
    src_fct, src_kwargs = SOURCEDICT[src_name]

    if isinstance(source, Mapping):
        src_kwargs |= source["kwargs"]

    # Fix units
    if "temperature" in src_kwargs and not isinstance(src_kwargs["temperature"], u.Quantity):
        src_kwargs["temperature"] <<= u.K
    if "amplitude" in src_kwargs and not isinstance(src_kwargs["amplitude"], u.Quantity):
        src_kwargs["amplitude"] <<= u.ABmag

    src = src_fct(**src_kwargs)
    #logger.info("Source function: %s", src_fct.__name__)
    #logger.debug("Source kwargs: %s", src_kwargs)
    #logger.info("ScopeSim mode: %s", mode)

    # set up the cmd structure to pass to ScopeSim. This is a bit clunky, but it works, so I'm not
    # going to mess with it for now. 
    
    #set up the simulation

    mode = rcp['mode']
    
    if("wavelen" in rcp['properties']):
        cmd = sim.UserCommands(use_instrument="METIS", set_modes=[mode],properties={"!OBS.wavelen": rcp['properties']['wavelen']})
    else:
        cmd = sim.UserCommands(use_instrument="METIS", set_modes=[mode])

    #copy over the OBS settings directly, then set up the optical train

    # the shutter stuff is a hack to deal with the fact that closed shutter is not
    # implemented in ScopeSim yet

    # keywords we always have

    shutter = False
    cmd["!OBS.catg"] = props["catg"]
    cmd["!OBS.type"] = props["type"]
    cmd["!OBS.tech"] = props["tech"]
    cmd["!OBS.mjd-obs"] = props["MJD-OBS"]
    cmd["!OBS.dateobs"] = props["dateobs"]
    # TODO: Ensure ndfilter_name is always defined.
    cmd["!OBS.nd_filter_name"] = props.get("ndfilter_name", "open")
    cmd["!OBS.filter_name"] = props["filter_name"]
    if cmd["!OBS.filter_name"] == "closed":
        cmd["!OBS.filter_name"] = "open"
        shutter = True

    # optional keywords
    
    if("tplname" in props.keys()):
        cmd["!OBS.tplname"] = props["tplname"]
    if("tplexpno" in props.keys()):
        cmd["!OBS.tplexpno"] = props["tplexpno"]
    if("tplstart" in props.keys()):
        cmd["!OBS.tplstart"] = props["tplstart"]

    # set up the optical train

    metis = sim.OpticalTrain(cmd)

    #set the WCU mode arguments
    if(rcp['wcu'] is not None):
        
        # set temperatures of black body
        if(np.all(["bb_temp" in wcu,"is_temp" in wcu, "wcu_temp" in wcu])):
            metis['wcu_source'].set_temperature(bb_temp=wcu['bb_temp']*u.K, is_temp=wcu['is_temp']*u.K,wcu_temp=wcu['wcu_temp']*u.K)

        # set focal plane mask
        if("current_fpmask" in wcu):
            if("xshift") in wcu:
                metis['wcu_source'].set_fpmask(wcu['current_fpmask'],shift=(wcu['xshift'],wcu['yshift']))
            else:
                metis['wcu_source'].set_fpmask(wcu['current_fpmask'])

        # set aperture
        if("bb_aperture" in wcu):
            metis['wcu_source'].set_bb_aperture(wcu['bb_aperture'])

    if small:
        # Hack to make the detectors smaller, so we can run the simulations
        # quickly in the continuous integration. For example, we want
        # ScopeSim_Data to download all the required external data, but we
        # don't care about the output.

        # this is rapidly becoming obsolete with functional recipes, but
        # we'll leave in. 
        
        for key in ['detector_array', 'detector_array_list']:
            if key in metis.effects['name']:
                metis[key].table['x_size'] = 32
                metis[key].table['y_size'] = 32

    # and a warning for old versions of the IRDB
    
    if "common_fits_keywords" not in metis.effects["name"]:
        logger.error(
            "The 'common_fits_keywords' effect was not found in the optical "
            "train, FITS header will be incomplete. Make sure you are using "
            "an up-to-date version of the METIS IRDB package!")

    # more of the shutter hack
    if shutter:
        metis.optics_manager["METIS"].add_effect(sim.effects.Shutter())

    # now observe and readout
    metis.observe(src)
    hdus = metis.readout(dit=props['dit'],ndit=props['ndit'])

    # can't remember why this is here, check \TODO
    hdus[0][0].header['HIERARCH ESO DPR TECH'] = props["tech"]
    hdus[0].writeto(fname,overwrite=True)
    return hdus[0]


def _logger_setup(verbosity: int) -> None:
    loglevel = max(-10 * verbosity + logging.WARNING, logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(loglevel)
    handler.setFormatter(ColoredFormatter(False))
    logger.addHandler(handler)
    logger.setLevel(loglevel)
    logger.propagate = False

