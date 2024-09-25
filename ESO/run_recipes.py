#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""."""

from pathlib import Path
from itertools import product

import argparse

import simulationDefinitions as sd


import yaml

from astar_utils import NestedMapping

from raw_script import simulate
from astropy.time import Time, TimeDelta
import numpy as np
from datetime import datetime
from updateHeaders import updateHeaders


def run(inputYAML, outputDir, small=False, sequence = False, nCalib = 0, startMJD = None, testRun = False, catglist=None):
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

    # check for valid values, abort if not
    
    cRep = checkRecipes(dorcps)
    if(cRep == 1):
        return
    
    print(f'Recipes loaded from {inputYAML}')
    tObs = None
    out_dir = Path(outputDir)
    out_dir.mkdir(parents=True, exist_ok=True)

    expandables = [
        "dit",
    ]

        
    darks = []
    skyFlats = []
    lampFlats = []
    
    # check for the first iteration
    firstIt = True
    tDelt = TimeDelta(0, format='sec') 
    # cycle through all the recipes
    for name, recipe in dorcps.items():

        # expand the expandables

        expanded = [key for key in expandables
                    if isinstance(recipe["properties"][key], list)]
        combos = product(*[recipe["properties"][key] for key in expanded])

        # get the mode and the prefix for the title; the latter is not needed for an
        # observation sequence
        
        mode = recipe["mode"]
        prefix = recipe["do.catg"]
        nObs = recipe["properties"]["nObs"]

        # cycle through the combos (may only be one)
        sequence = True
        for combo in combos:

            # extract the properties and combine with the combo dictionary
            
            combodict = dict(zip(expanded, combo))
            props = recipe["properties"] | combodict
            # a blank value of ndfilter_name if not explicitly given
            try:
                nfname = props["ndfilter_name"]
            except:
                props["ndfilter_name"] = "open"

            # if needed, keep a tally of the different sets of parameters that will be passed to simulate()
            if(nCalib > 0):


                if(nCalib > 0):
                    # keep a running tally of dark and flat recipes
                    darks.append(calcDark(props))
                    skyFlats.append(calcSkyFlat(props))
                    lampFlats.append(calcLampFlat(props))
                
            # first iteration, need to intialize dateobs regardless of method for timestamp
            if(firstIt):

                #if sequence=True, we get this from startMJD if set, or the YAML file
                if(sequence):
                            
                    if(startMJD is not None):
                        tObs = Time(datetime.strptime(startMJD, '%Y-%m-%d %H:%M:%S'))
                    elif "dateobs" in recipe["properties"]:
                        tObs = Time(recipe["properties"]["dateobs"])[0]
                    else:
                        print("No appropriate starting time found; exiting")
                        return

                    # tDelt is 0 because we've just set the value
                    
                #if sequence = False, get from the YAML file
                else:
                    if "dateobs" in recipe["properties"]:
                        tObs = Time(recipe["properties"]["dateobs"])[0]
                    else:
                        print("No appropriate starting time found; exiting")
                        return
                firstIt = False

            # if this isn't the first iteration, we increment if sequence=True,
            # otherwise get from the YAML entry. If the YAML  doesn't have an dateobs set
            # increment as for the seuqence case
            else:
                if(not sequence):
                    # set explicitly, and tDelt = 0
                    if "dateobs" in recipe["properties"]:
                        tObs = Time(recipe["properties"]["dateobs"])[0]
                    else:
                        print("No appropriate starting time found; exiting")
                        return


            # for nObs exposures of each set of parameters
            for _ in range(nObs):        

                # note that tDelt = 0 if we've explicitly set it above
                tObs = tObs + tDelt

                # update the dateobs in the dictionary
                props["dateobs"] = tObs.tt.datetime
                sdate = tObs.tt.datetime.isoformat()

                # update tDelt for the next iteration
                tDelt = TimeDelta(props['dit']*props['ndit']*1.2+1, format='sec')   

                # get the filename
                fname = out_dir / generateFilename(props['dateobs'],mode,props['dit'],prefix)

                print("Starting simulate()")
                print(f"    fname={fname}")
                print(f'    source =  {recipe["source"]}')

                # get kwargs for scopeSim
                kwargs = NestedMapping({"OBS": props})
                print(f"    dit={props['dit']},ndit={props['ndit']},catg={props['catg']},tech={props['tech']},type={props['type']},filter_name={props['filter_name']}, ndfilter_name={props['ndfilter_name']}")

                # and run the 
                if(not testRun):
                    
                    simulate(fname, mode, kwargs, source=recipe["source"], small=small)


    # do the calibrations if needed
    if(nCalib > 0):
        # increment the observing time from the last exposure
        if(tObs is None):
            tObs = Time(recipe["properties"]["dateobs"])[0]+tDelt
        else:
            tObs += tDelt

        generateCalibs(darks,skyFlats,lampFlats,tObs,nCalib,small,out_dir,testRun)
    return


def calcDark(props):

    """determine what sort of dark, if any, is needed for a YAML entry"""

    if("DARK" not in props['type']):
        if(",LM" in props['tech']):
            df = sd.DARKLM
            df['mode'] = "img_lm"
        elif(",N" in props['tech']):
            df = sd.DARKN
            df['mode'] = "img_n"
        elif(np.any(["LMS" in props['tech'],"IFU" in props['tech']])):
            df = sd.DARKIFU
            df['mode'] = "lms"
        else:
            return{}

        df['dit'] = props['dit']
        df['ndit'] = props['ndit']
        return df
    else:
       return {}

def calcSkyFlat(props):

    """determine what sort of sky flat, if any, is needed for a YAML entry"""

    if(np.all(["DARK" not in props['type'], "FLAT" not in props['type'],"DETLIN" not in props['type'],"LMS" not in props['type']])):
        if(",LM" in props['tech']):
            df = sd.SKYFLATLM
            df['mode'] = "img_lm"
        elif(",N" in props['tech']):
            df = sd.SKYFLATN
            df['mode'] = "img_n"
        else:
            return{}

        df['properties']['filter_name'] = props['filter_name']
        df['properties']['ndfilter_name'] = "open"
        df['dit'] = 0.25
        df['ndit'] = 1
        
        return df
    else:
        return {}

def calcLampFlat(props):

    """determine what sort of lamp flat, if any, is needed for a YAML entry"""
    if(np.all(["DARK" not in props['type'], "FLAT" not in props['type'],"DETLIN" not in props['type'],"LMS" not in props['type']])):
        if(",LM" in props['tech']):
            df = sd.LAMPFLATLM
            df['mode'] = "img_lm"
        elif(",N" in props['tech']):
            df = sd.LAMPFLATN
            df['mode'] = "img_n"
        else:
            return{}

        df['properties']['filter_name'] = props['filter_name']
        df['properties']['ndfilter_name'] = "open"
        df['dit'] = 0.25
        df['ndit'] = 1
        
        return df
    else:
        return {}

def checkRecipes(rcps):

    """check recipe dictionary for necessary input"""

    goodInput = 0

    # keywords that must exist, either at the top level, or in properties
    ex1 = ["do.catg","mode","properties"]
    ex2 = ["dit","ndit","filter_name","catg","tech","type","nObs"]

    # check for existence
    
    for name, recipe in rcps.items():    
        for elem in ex1:
            if(elem not in recipe):
                print(f'Recipe {name} does not contain required field {elem}')
                goodInput = 1

        for elem in ex2:
            if(elem not in recipe["properties"]):
                print(f'Recipe {name} does not contain required field {elem}')
                goodInput = 1
            
    # check for values

    # /TODO get list of filter names / ndfilter names

    for name, recipe in rcps.items():
       

        # catg, type and tech in list of valid values. update list in simulationDefinitions as needed
        
        if(recipe['properties']['catg'] not in sd.catgVals):
           print(f"Recipe {name} has invalid CATG of {recipe['properties']['catg']})")
           goodInput = 1
        if(recipe['properties']['tech'] not in sd.techVals):
           print(f"Recipe {name} has invalid TECH of {recipe['properties']['tech']})")
           goodInput = 1
        if(recipe['properties']['type'] not in sd.typeVals):
           print(f"Recipe {name} has invalid TYPE of {recipe['properties']['type']})")
           goodInput = 1
        if(recipe['mode'] not in sd.modeVals):
           print(f"Recipe {name} has invalid MODE of {recipe['mode']})")
           goodInput = 1

        # nObs, ndit and dit are integers / numbers > 0
        
        if(not isinstance(recipe["properties"]["nObs"], int)):
           print(f"Recipe {name} has invalid NOBS of {recipe['properties']['nObs']})")
           goodInput = 1
        elif(recipe["properties"]["nObs"] <= 0):
            print(f"Recipe {name} has invalid NOBS of {recipe['properties']['nObs']})")
            goodInput = 1

        if(not isinstance(recipe["properties"]["ndit"], int)):
           print(f"Recipe {name} has invalid NDIT of {recipe['properties']['ndit']})")
           goodInput = 1
        elif(recipe["properties"]["ndit"] <= 0):
            print(f"Recipe {name} has invalid NDIT of {recipe['properties']['ndit']})")
            goodInput = 1

        # note that dit can be a number or a list
        if(type(recipe["properties"]["dit"]) is list):
            for elem in recipe["properties"]["dit"]:
                if(not isinstance(elem, (int,float))):
                    print(f"Recipe {name} has invalid DIT of {recipe['properties']['dit']})")
                    goodInput = 1
                elif(elem <= 0):
                    print(f"Recipe {name} has invalid DIT of {recipe['properties']['dit']})")
                    goodInput = 1
        else:
            if(not isinstance(recipe["properties"]["dit"], (int,float))):
                print(f"Recipe {name} has invalid DIT of {recipe['properties']['dit']})")
                goodInput = 1
            elif(recipe["properties"]["dit"] <= 0):
                print(f"Recipe {name} has invalid DIT of {recipe['properties']['dit']})")
                goodInput = 1

                    
                   
    return goodInput
           

def _load_recipes(inputYAML) -> dict:

    with Path(inputYAML).open(encoding="utf-8") as file:
        return yaml.safe_load(file)

def generateFilename(dateobs,doCatg,dit,prefix):

    """
    Generate a METIS like filename based on the dateobs, DO.CATG and dit

     The filenames from the ICS software will probably look like
         METIS.2024-02-29T01:23:45.678.fits
     However, this has two drawbacks:
     - There are colons that cannot be used in Windows filenames.
     - They don't contain any information about the type of file.
     Therefor the colons are replaced and extra information is added.
     The resulting filenames look like
         METIS.2024-01-02T03_45_00.DETLIN_LM_RAW-dit1.0.fits
     Replace colon so the date can be in Windows filenames.
    """
    
    sdate = dateobs.isoformat()
    sdate = sdate.replace(":", "_")
    
    fname = f'METIS.{prefix}.{sdate.replace(":","_")}.{doCatg}.{str(dit)}.fits'
            
    return fname


def generateCalibs(darks,skyFlats,lampFlats,tObs,nObs,small,out_dir,testRun):


    """
    Routine to parse the recipes dictionary, determine what darks (dit/ndit/detector) 
    and flats (dit/ndit/detector/filter/ndfilter) are needed to go with the generated data.
    
    Input
      allParms: list of tuples of the input parameters derived from the input YAML file
      tObs: starting observation time for the sequence
      nObs: number of each set of calibs to do
      small: flag for small images
      out_dir: output directory 

    Output:
      set of FITS files, nObs for each unique set of input parameters.

    There are probably some beautifully opaque pythonic ways of doing some of this, 
    probably involving list comprehension and iterators, 
    but the current code works, so I'm not going to devote time to figuring it 
    how to do it more elegantly. 

    """

    calibSet = {}
    nLab = 0
    import json
    
    for rcp in set(json.dumps(i, sort_keys=True) for i in darks):
        if(rcp):
            label = f'd{nLab}'
            nLab += 1
            calibSet[label] = rcp

    for rcp in set(json.dumps(i, sort_keys=True) for i in skyFlats):
        if(rcp):
            label = f's{nLab}'
            nLab += 1
            calibSet[label] = rcp

    for rcp in set(json.dumps(i, sort_keys=True) for i in lampFlats):
        if(rcp):
            label = f'l{nLab}'
            nLab += 1
            calibSet[label] = rcp

    for key in calibSet:
        elem=json.loads(calibSet[key])
        if(elem):
            source = elem['source']
            props = elem['properties']

            # do nObs of each uniq file
            for _ in range(nObs):
            
                fname = out_dir / generateFilename(tObs.tt.datetime,elem['mode'],elem['dit'],elem['do.catg'])
                elem["properties"]["dateobs"] = tObs.tt.datetime
                # get kwargs for scopeSim
                kwargs = NestedMapping({"OBS": elem['properties']})

                print("Starting simulate() for calibration files")
                print(f"    fname={fname}")
                print(f'    source =  {source}')

                print(f"    dit={elem['dit']},ndit={elem['ndit']},catg={props['catg']},tech={props['tech']},type={props['type']},filter_name={props['filter_name']}")
            
                if(not testRun):
                    simulate(fname, elem['mode'], kwargs, source=source, small=small)
                tObs += TimeDelta(elem['dit']*elem['ndit']*1.2+1, format='sec') 


if __name__ == "__main__":

    parser = argparse.ArgumentParser()


    parser.add_argument('-i', '--inputYAML', type=str,
                        help='input YAML File')
    parser.add_argument('-o', '--outputDir', type=str,
                        help='output directory')
    parser.add_argument('-s', '--small', action = "store_true",
                        default=False,
                        help=('use detectors of 32x32 pixels; ' +
                              'for running in the continuous integration'))
    parser.add_argument('-c', '--catg', type=str,
                        help='comma-separated list of selected output file categories')
    parser.add_argument('--doCalib', type=int,
                    default=0, help='automatically generate darks and flats for the dataset. Will generate N of each type')

    # expects either 1 or a date stamp
    parser.add_argument('--sequence', type=str,
                    default=False, help='options for generating timestamps. Set to a date in the form yyyy-mm-dd hh:mm:ss to start from a specific date, or 1 to use the first dateobs in the YAML file.')

    # if set, option to true
    parser.add_argument('--testRun', action="store_true",
                        help='run the script without executing simulate to check input')

    args = parser.parse_args()
    if args.inputYAML:
        inputYAML = args.inputYAML
    else:
        inputYAML = Path(__file__).parent / "recipes.yaml"

    if args.outputDir:
        outputDir = args.outputDir
    else:
        outputDir = Path(__file__).parent / "output/"
    if(args.sequence):
        if(args.sequence == "1"):
            startMJD = None
            sequence = True
        else:
            startMJD = args.sequence
            sequence = True
    else:
        sequence = False
        startMJD = None

    if(args.doCalib):
        doCalib = args.doCalib
    else:
        doCalib = 0


        
    small = args.small
    
    testRun = args.testRun
    
    print(f"Starting Simulations")
    print(f'   input YAML = {inputYAML}, output directory =  {outputDir}')
    if(startMJD is not None):
        print(f'  observation sequence starting at {startMJD}')
    elif(sequence):
        print(f'  Observation sequence will start from first date in YAML file')
    else:
        print(f'  Observation dates will be taken from YAML file if given')
    print(f'  Automatically generated darks and flats {doCalib}')
    print(f'  Small output option {small}')
    
    run(inputYAML, outputDir, small, sequence, doCalib, startMJD, testRun)


    if args.catg:
        catglist = args.catg.split(',')
    else:
        catglist = None


    if(not testRun):
        updateHeaders(outputDir,outputDir)

