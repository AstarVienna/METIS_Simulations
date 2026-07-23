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
import os

import numpy as np
from more_itertools import value_chain

from astar_utils.loggers import get_logger, ColoredFormatter
import scopesim as sim
import scopesim_templates as sim_tp
import astropy.units as u

from .simulationDefinitions import *
from .sources import *
DEFAULT_IRDB_LOCATION = os.environ["DEFAULT_IRDB_LOCATION"]
sim.rc.__config__["!SIM.file.local_packages_path"] = DEFAULT_IRDB_LOCATION

logger = get_logger(__file__)

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

    # copy over the OBS settings directly, then set up the optical train

    # keywords we always have

    reqKeys = ["catg","type","tech","MJD-OBS","dateobs"]

    keyDefaults = {}
    keyDefaults["nd_filter_name"] = "open"
    keyDefaults["filter_name"] = "open"
    
    # set required keys
    shutter = False
    for elem in reqKeys:
        cmd[f"!OBS.{elem}"] = props[elem]

    # set keys that aren't required in YAML, but have defaults 
    for elem in keyDefaults:
        cmd[f"!OBS.{elem}"] = props.get(elem,keyDefaults[elem])

    #cmd["!OBS.catg"] = props["catg"]
    #cmd["!OBS.type"] = props["type"]
    #cmd["!OBS.tech"] = props["tech"]
    #cmd["!OBS.mjd-obs"] = props["MJD-OBS"]
    #cmd["!OBS.dateobs"] = props["dateobs"]
    #cmd["!OBS.nd_filter_name"] = props.get("nd_filter_name", "open")
    #cmd["!OBS.filter_name"] = props["filter_name"]

    # now assigning remaining keys
    # TODO add checks of valid values
    for elem in props:
        if(elem not in reqKeys and elem not in keyDefaults):
            cmd[f"!OBS.{elem}"] = props[elem]

    #if("tplname" in props.keys()):
    #    cmd["!OBS.tplname"] = props["tplname"]
    #if("tplexpno" in props.keys()):
    #    cmd["!OBS.tplexpno"] = props["tplexpno"]
    #if("tplstart" in props.keys()):
    #    cmd["!OBS.tplstart"] = props["tplstart"]

    # set up the optical train

    cmd["!SIM.random.seed"] = int((props["MJD-OBS"]-60000)*100000)
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

    hdus = updateHeaders(hdus[0], props["MJD-OBS"])
    import hashlib, pathlib
    
    hash = hashlib.md5(str(hdus).encode('utf-8')).hexdigest()
    fname = pathlib.Path(str(fname).replace(".fits",f"_{hash[0:6]}.fits"))

    hdus.writeto(fname,overwrite=True)
    return hdus[0]

def updateHeaders(hdul, mjd):

    """
    add keywords to a list of files, fixing anything that isn't handled by ScopeSim. 
    
    DPR .TECH, .FILTER and .TYPE are set by ScopeSim, DRS.FILTER .ND_FILTER, 
    and DET.DIT and .NDIT are set in ScopeSim

    We use the TECH to get INS.MODE
    Sets the DRS.SLIT to the default value for now (will fix later). TODO.
    Sets INS.OPTI*.NAME to the filter, slit as indicated by the TECH, FILTER and SLIT keyword

    For HCI / Coronagraph modes, we set the TECH keyword to a non valid value in Scopesim, 
    and use that to set the DRS.MASK, correct DPR.TECH, and INS.OPTI*.NAME values. This is kludgy,
    and will be fixed later. TODO.

    We check the TYPE keyword for LASER Sources. 

    The correct MJD date is written

    Adjusted files **WILL OVERWRITE EXISTING FILES**

    The list of files is compiled during the previous running of the simulations
    """
    

    for hdu in hdul:
        # Remove lower case keywords, in particular "pixel_size"
        for k in hdu.header:
            if k.upper() != k:
                print(f"Lower case keyword found and removed: {k}")
                hdu.header.pop(k)


    # fix for the occasional keyword that gets written as boolean not string
    for elem in hdul[0].header:
        if("OPTI" in elem and "NAME" in elem):
            if isinstance(hdul[0].header[elem], bool):
                hdul[0].header[elem] = str(hdul[0].header[elem])
        if("CUBE MODE" in elem):
            if isinstance(hdul[0].header[elem], bool):
                hdul[0].header[elem] = str(hdul[0].header[elem])
        
    hdul[0].header['MJD-OBS'] = mjd
    
    #if type(hdul[0].header['MJD-OBS']) == str:
    #    mjdobs = hdul[0].header['MJD-OBS']
    #    hdul[0].header['MJD-OBS'] = astropy.time.Time(mjdobs,format="isot").mjd
    # get the tech and filter keywords
    
    tech = hdul[0].header['HIERARCH ESO DPR TECH']
    filt = hdul[0].header['HIERARCH ESO DRS FILTER']

    
    if(tech == "LSS,LM"):
        hdul[0].header['HIERARCH ESO INS MODE'] = "SPEC_LM"
        #hdul[0].header['HIERARCH ESO INS OPTI9 NAME'] = filt
        #hdul[0].header['HIERARCH ESO INS DRS SLIT'] = "C-38_1"
    if(tech == "LSS,N"):
        hdul[0].header['HIERARCH ESO INS MODE'] = "SPEC_N_LOW"
        #hdul[0].header['HIERARCH ESO INS OPTI12 NAME'] = filt
        hdul[0].header['HIERARCH ESO INS DRS SLIT'] = "C-38_1"
    
    #IMAGING
    if(tech == "IMAGE,LM"):
        hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_LM"
        #hdul[0].header['HIERARCH ESO INS OPTI10 NAME'] = filt
    if(tech == "IMAGE,N"):
        hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_N"
        #hdul[0].header['HIERARCH ESO INS OPTI13 NAME'] = filt
    
    #IFU
    if(tech == "IFU"):
        hdul[0].header['HIERARCH ESO INS MODE'] = "IFU_nominal"
        #hdul[0].header['HIERARCH ESO INS OPTI6 NAME'] = filt
        hdul[0].header['HIERARCH ESO DRS IFU'] = filt
        hdul[0].header['HIERARCH ESO DPR TECH'] = "IFU"
        
    #HCI
    if(tech == "RAVC,LM"):
        #hdul[0].header['HIERARCH ESO INS OPTI10 NAME'] = filt
        hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_LM_RAVC"
        hdul[0].header['HIERARCH ESO DRS MASK'] = "VPM-L,RAP-LM,RLS-LMS"
        hdul[0].header['HIERARCH ESO INS OPTI1 NAME'] = "RAP-LM"
        hdul[0].header['HIERARCH ESO INS OPTI3 NAME'] = "VPM-L"
        hdul[0].header['HIERARCH ESO INS OPTI5 NAME'] = "RLS-LMS"
        hdul[0].header['HIERARCH ESO DPR TECH'] = "IMAGE,LM"
    
    if(tech == "APP,LM"):
        #hdul[0].header['HIERARCH ESO INS OPTI10 NAME'] = filt
        hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_LM_APP"
        hdul[0].header['HIERARCH ESO DPR TECH'] = "IMAGE,LM"
        hdul[0].header['HIERARCH ESO INS OPTI1 NAME'] = "RAP-LM"
        hdul[0].header['HIERARCH ESO INS OPTI3 NAME'] = "VPM-L"
        hdul[0].header['HIERARCH ESO INS OPTI5 NAME'] = "APP-LMS"
        hdul[0].header['HIERARCH ESO DRS MASK'] = "VPM-L,RAP-LM,APP-LMS"
    
    if(tech == "RAVC,IFU"):
        hdul[0].header['HIERARCH ESO INS OPTI6 NAME'] = filt
        hdul[0].header['HIERARCH ESO INS MODE'] = "IFU_nominal_RAVC"
        hdul[0].header['HIERARCH ESO DRS IFU'] = filt
        hdul[0].header['HIERARCH ESO DPR TECH'] = "IFU"
        hdul[0].header['HIERARCH ESO INS OPTI1 NAME'] = "RAP-LM"
        hdul[0].header['HIERARCH ESO INS OPTI3 NAME'] = "VPM-L"
        hdul[0].header['HIERARCH ESO INS OPTI5 NAME'] = "RLS-LMS"
        hdul[0].header['HIERARCH ESO DRS MASK'] = "VPM-L,RAP-LM,RLS-LMS"

    #OTHER
    if(hdul[0].header['HIERARCH ESO DPR TYPE'] == "WAVE"):   
        hdul[0].header['HIERARCH ESO SEQ WCU LASER1 NAME'] = "LASER1"

    #OTHER
    if(tech == "PUP,LM"):
        hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_LM"
        hdul[0].header['HIERARCH ESO INS OPTI15 NAME'] = "PUPIL1"
    if(tech == "PUP,N"):
        hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_N"
        hdul[0].header['HIERARCH ESO INS OPTI15 NAME'] = "PUPIL2"

    return hdul

def _logger_setup(verbosity: int) -> None:
    loglevel = max(-10 * verbosity + logging.WARNING, logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(loglevel)
    handler.setFormatter(ColoredFormatter(False))
    logger.addHandler(handler)
    logger.setLevel(loglevel)
    logger.propagate = False

