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
    
    cRep = checkRecipes(rcps)
    if(cRep == 1):
        return
    
    print(f'Recipes loaded from {inputYAML}')
    tObs = None
    out_dir = Path(outputDir)
    out_dir.mkdir(parents=True, exist_ok=True)

    expandables = [
        "dit",
    ]

        
    allParms = []
    
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
        prefix = recipe["prefix"]
        nObs = recipe["properties"]["nObs"]

        # cycle through the combos (may only be one)
        sequence = True
        for combo in combos:

            # extract the properties and combine with the combo dictionary
            
            combodict = dict(zip(expanded, combo))
            props = recipe["properties"] | combodict

            # if needed, keep a tally of the different sets of parameters that will be passed to simulate()
            if(nCalib > 0):

                # a blank value of ndfilter_name if not explicitly given
                try:
                    nfname = props["ndfilter_name"]
                except:
                    nfname = ""

                allParms.append((props['dit'],props["ndit"],props["catg"],props["tech"],props["type"],props["filter_name"],nfname))


            print(firstIt, startMJD is not None, sequence)
            # first iteration, need to intialize mjdObs regardless of method for timestamp
            if(firstIt):

                #if sequence=True, we get this from startMJD if set, or the YAML file
                if(sequence):
                            
                    if(startMJD is not None):
                        tObs = Time(datetime.strptime(startMJD, '%Y-%m-%d %H:%M:%S'))
                    elif "mjdobs" in recipe["properties"]:
                        tObs = Time(recipe["properties"]["mjdobs"])[0]
                    else:
                        print("No appropriate starting time found; exiting")
                        return

                    # tDelt is 0 because we've just set the value
                    
                #if sequence = False, get from the YAML file
                else:
                    if "mjdobs" in recipe["properties"]:
                        tObs = Time(recipe["properties"]["mjdobs"])[0]
                    else:
                        print("No appropriate starting time found; exiting")
                        return
                firstIt = False

            # if this isn't the first iteration, we increment if sequence=True,
            # otherwise get from the YAML entry. If the YAML  doesn't have an mjdObs set
            # increment as for the seuqence case
            else:
                if(not sequence):
                    # set explicitly, and tDelt = 0
                    if "mjdobs" in recipe["properties"]:
                        tObs = Time(recipe["properties"]["mjdobs"])[0]
                    else:
                        print("No appropriate starting time found; exiting")
                        return


            # for nObs exposures of each set of parameters
            for i in range(nObs):        

                # note that tDelt = 0 if we've explicitly set it above
                tObs = tObs + tDelt

                # update the mjdobs in the dictionary
                props["mjdobs"] = tObs.tt.datetime
                sdate = tObs.tt.datetime.isoformat()

                # update tDelt for the next iteration
                tDelt = TimeDelta(props['dit']*props['ndit']*1.2+1, format='sec')   

                # get the filename
                fname = out_dir / generateFilename(props['mjdobs'],mode,props['dit'],prefix)

                print("Starting simulate()")
                print(f"    fname={fname}")
                print(f'    source =  {recipe["source"]}')

                # get kwargs for scopeSim
                kwargs = NestedMapping({"OBS": props})
                print(f"    dit={props['dit']},ndit={props['ndit']},catg={props['catg']},tech={props['tech']},type={props['type']},filter_name={props['filter_name']}",end="")
                if("ndfilter_name" in props):
                    print(f",ndfilter_name={props['ndfilter_name']}")
                else:
                    print()



                # and run the 
                if(not testRun):
                    simulate(fname, mode, kwargs, source=recipe["source"], small=small)


    # do the calibrations if needed
    if(nCalib):
        # increment the observing time from the last exposure
        if(tObs is None):
            tObs = Time(recipe["properties"]["mjdobs"])[0]+tDelt
        else:
            tObs += tDelt

        generateCalibs(allParms,tObs,nCalib,small,out_dir,testRun)
    return


def checkRecipes(rcps):

    """check recipe dictionary for necessary input"""

    goodInput = 0

    # keywords that must exist, either at the top level, or in properties
    ex1 = ["prefix","mode","properties"]
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
>>>>>>> 314e488 (Some major updates to the calling of run_recipes.)

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

def generateFilename(mjdobs,doCatg,dit,prefix):

    """
    Generate a METIS like filename based on the mjdobs, DO.CATG and dit

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
    
    sdate = mjdobs.isoformat()
    sdate = sdate.replace(":", "_")
    
    fname = f'METIS.{prefix}.{sdate.replace(":","_")}.{doCatg}.{str(dit)}.fits'
            
    return fname


def generateCalibs(allParms,tObs,nObs,small,out_dir,testRun):


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

    # pare down the list to just the simulations that will need darks or flats for processing
    
    darks = []
    flats = []
    
    for elem in set(allParms):

        # if DARK isn't in the TYPE, it needs a corresponding DARK
        if(np.all(["DARK" not in elem[4]])):
            darks.append((elem[0],elem[1],elem[3]))

            # if it's not a DARK, FLAT or DETLIN, it needs a flat image
            if(np.all(["FLAT" not in elem[4],"DETLIN" not in elem[4]])):
                flats.append((elem[0],elem[1],elem[3],elem[5],elem[6]))
    
                   
    # there are three different detectors for darks/flats, but multiple names which can refer to them,
    # so we need to filter them. 
    # here, get lists of the dit/ndit/filter/ndfilter for the darks and flats
    # also, add in the strings for the file name/mode/tech, and the source
    

    # two sources here - empty sky and a lamp flat

    sources = {}
    sources["sky"] = {'name': 'empty_sky', 'kwargs': {}}
    sources["lamp"] = {'name': 'flat_field', 'kwargs': {'temperature': 200, 'amplitude': 0, 'filter_curve': 'V', 'extend': 15}}
    # another list of tuples with input parameters
    # separate loops for teh darks, and twice for the flats (once for sky flats, once for lamp).
    # logically, we want to generate them sequentially by type
    calibSet = []
    for elem in set(darks):
        if(",LM" in elem[2]):
            calibSet.append((elem[0],elem[1],"IMAGE,LM","DARK_LM_RAW","DARK","img_lm","closed","","sky"))
        elif(",N" in elem[2]):        
            calibSet.append((elem[0],elem[1],"IMAGE,N","DARK_N_RAW","DARK","img_n","closed","","sky"))
        elif(np.any(["LMS" in elem[2],"IFU" in elem[2]])):
            calibSet.append((elem[0],elem[1],"LMS","DARK_IFU_RAW","DARK","lms","closed","","sky"))
    for elem in set(flats):
        if(",LM" in elem[2]):
            calibSet.append((elem[0],elem[1],"IMAGE,LM","FLAT_LM_RAW","FLAT,TWILIGHT","img_lm",elem[3],elem[4],"sky"))
        elif(",N" in elem[2]):       
            calibSet.append((elem[0],elem[1],"IMAGE,N","FLAT_N_RAW","FLAT,TWILIGHT","img_n",elem[3],elem[4],"sky"))
        elif(np.any(["LMS" in elem[2],"IFU" in elem[2]])):
            calibSet.append((elem[0],elem[1],"LMS","FLAT_IFU_RAW","FLAT,TWILIGHT","lms",elem[3],elem[4],"sky"))
    for elem in set(flats):
        if(",LM" in elem[2]):
            calibSet.append((elem[0],elem[1],"IMAGE,LM","FLAT_LM_RAW","FLAT,LAMP","img_lm",elem[3],elem[4],"lamp"))
        elif(",N" in elem[2]):       
            calibSet.append((elem[0],elem[1],"IMAGE,N","FLAT_N_RAW","FLAT,LAMP","img_n",elem[3],elem[4],"lamp"))
        elif(np.any(["LMS" in elem[2],"IFU" in elem[2]])):
            calibSet.append((elem[0],elem[1],"LMS","FLAT_IFU_RAW","FLAT,LAMP","lms",elem[3],elem[4],"lamp"))

    # now we're going to call simulate for each of the unique combinations involved
    # by setting up the parameters dictionary and the filename in the same way as
    # is done in the main routine

    dProps={}
    aa = set(calibSet)
    for elem in set(calibSet):
        dProps["catg"] = "CALIB"
        dProps["type"] = elem[4]
        dProps["dit"] = elem[0]
        dProps["ndit"] = elem[1]
        dProps["tech"] = elem[2]
        dProps["filter_name"] = elem[6]

        # ndfilter if present
        if(elem[7] != ""):
            dProps["ndfilter_name"] = elem[7]
        else:
            dProps.pop("ndfilter_name",None)

        mode = elem[5]

        source = sources[elem[8]]

        # do nObs of each uniq file
        for i in range(nObs):
            
            fname = out_dir / generateFilename(tObs.tt.datetime,elem[3],elem[0],prefix)
            dProps["mjdobs"] = tObs.tt.datetime
            kwargs = NestedMapping({"OBS": dProps})

            print("Starting simulate() for calibration files")
            print(f"    fname={fname}")
            print(f'    source =  {source}')

            # get kwargs for scopeSim
            kwargs = NestedMapping({"OBS": dProps})
            print(f"    dit={dProps['dit']},ndit={dProps['ndit']},catg={dProps['catg']},tech={dProps['tech']},type={dProps['type']},filter_name={dProps['filter_name']}",end="")
            if("ndfilter_name" in dProps):
                print(f",ndfilter_name={ndfilter_name}")
            else:
                print()

            
            if(not testRun):
                simulate(fname, mode, kwargs, source=source, small=small)
            tObs += TimeDelta(elem[0]*elem[1]*1.2+1, format='sec') 


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
    parser.add_argument('d','--doCalib', type=int,
                    default=0, help='automatically generate darks and flats for the dataset. Will generate N of each type')
    parser.add_argument('--sequence', type=str,
                    default=False, help='options for generating timestamps. Set to a date in the form yyyy-mm-dd hh:mm:ss to start from a specific date, or 1 to use the first mjdObs in the YAML file.')
    parser.add_argument('--testRun', type=bool,
                        default=False, help='run the script without executing simulate to check output')

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
    doCalib = args.doCalib
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

    small = args.small

    if args.catg:
        catglist = args.catg.split(',')
    else:
        catglist = None

    print(inputYAML, outputDir, small, catglist)
    run(inputYAML, outputDir, small, catglist)
