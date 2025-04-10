#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Class to run a set of simulations in Scopesim, based on an input YAML file"""

from pathlib import Path
import yaml
import argparse
import simulationDefinitions as sd
import json
from raw_script import simulate
from astropy.time import Time, TimeDelta
from itertools import product
from astar_utils import NestedMapping
from datetime import datetime
import numpy as np
from astropy.io import fits
import astropy
import copy
from multiprocessing import Pool,Process,Manager

class runRecipes():

    def __init__(self):
        
        self.calibSet = None
        self.tObs = None
        self.firstIt = True
        self.tDelt = TimeDelta(0, format='sec') 
        self.allFileNames = []
        self.allmjd = []
        
    def parseCommandLine(self,args):

        """
        Parse the command line options to get the paramters to run the set of simulations
        Creates a dictionary, params, containing all command line options
        """
        
        parser = argparse.ArgumentParser()

        params = {}

        parser.add_argument('-i', '--inputYAML', type=str,
                            help='input YAML File')
        parser.add_argument('-o', '--outputDir', type=str,
                            help='output directory')
        parser.add_argument('-s', '--small', action = "store_true",
                            default=False,
                            help=('use detectors of 32x32 pixels; ' +
                                  'for running in the continuous integration'))
        
        parser.add_argument('-e', '--doStatic', action = "store_true",
                            default=False,
                            help=('Generate prototypes for static/external calibration files'))

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

        parser.add_argument('-f', '--calibFile', type=str,
                            default = None,
                            help='File to dump calibration file YAML to')
        parser.add_argument('-n', '--nCores', type=int,
                            default = 1,
                            help='number of cores for parallel processing')

        
        args = parser.parse_args()
        if args.inputYAML:
            params['inputYAML'] = args.inputYAML
        else:
            params['inputYAML'] = Path(__file__).parents[1] / "YAML/allRecipes.yaml/"

        if args.outputDir:
            params['outputDir'] = args.outputDir
        else:
            params['outputDir'] = Path(__file__).parents[1] / "output/"
        if(args.sequence):
            if(args.sequence == "1"):
                params['startMJD'] = None
                params['sequence'] = True
            else:
                params['startMJD'] = args.sequence
                params['sequence'] = True
        else:
            params['sequence'] = False
            params['startMJD'] = None
        
        if(args.doCalib):
            params['doCalib'] = args.doCalib
        else:
            params['doCalib'] = 0
        
        if args.catg:
            params['catglist'] = args.catg.split(',')
        else:
            params['catglist'] = None
        
            
        params['small'] = args.small

        params['doStatic'] = args.doStatic
                            
        params['testRun'] = args.testRun

        params['calibFile'] = args.calibFile

        if args.nCores:
            params['nCores'] = args.nCores
        else:
            params['nCores'] = 1
        
        print(f"Starting Simulations")
        print(f"   input YAML = {params['inputYAML']}, output directory =  {params['outputDir']}")
        if(params['startMJD'] is not None):
            print(f"  observation sequence starting at {params['startMJD']}")
        elif(params['sequence']):
            print(f"  Observation sequence will start from first date in YAML file")
        else:
            print(f"  Observation dates will be taken from YAML file if given")
        print(f"  Automatically generated darks and flats {params['doCalib']}")
        print(f"  Small output option {params['small']}")
        print(f"  Generate External Calibs {params['doCalib']}")
    
        self.params = params

    def loadYAML(self):

        """
        read in a YAML file of recipe templates and filter as specified by command line arguments
        """
        
        allrcps = self._load_yaml(self.params['inputYAML'])
        self.dorcps = self._filter_yaml(allrcps)

        print(f"Recipes loaded from {self.params['inputYAML']}")

        
    def _load_yaml(self,inputYAML) -> dict:

        """load a YAML file of recipes"""

        with Path(inputYAML).open(encoding="utf-8") as file:
            return yaml.safe_load(file)

    def _filter_yaml(self,allrcps):

        """filter a dictionary of recipes"""

        if self.params['catglist'] is None:
            
            dorcps = allrcps
        else:
            dorcps = {}
            for catg in self.params['catglist']:
                if catg in allrcps.keys():
                    dorcps[catg] = allrcps[catg]
                else:
                    raise ValueError(f"ERROR: {catg} is not a supported product category")
        return dorcps
    
    def validateYAML(self):

        """
        Validate the YAML based on acceptable input parameters.
        Checks for: 
            necessary keywords
            valid filters for the mode
            valid nd filter
            valid catg, type, tech
            nObs, ndit positive integers
            dit(s) a positive float

        Prints diagnostic message and returns a boolean where True = passed the test

        The lists of valid parameter values can be found/updated in simulationDefintions.py
        """
        
        goodInput = True
        
        # check for existence of needed keywords before checking anything else
        
        for name, recipe in self.dorcps.items():    
            for keyword in sd.topKey:
                if(keyword not in recipe):
                    print(f'Recipe {name} does not contain required field {keyword} for recipe {name}')
                    goodInput = False
        
            for keyword in sd.propKey:
                if(keyword not in recipe["properties"]):
                    print(f'Recipe {name} does not contain required field {keyword} for recipe {name}')
                    goodInput = False
                
            return goodInput
    
        for name, recipe in self.dorcps.items():
           
            # check for filter values (/TODO check HCI non HCI validity)
            if(recipe['properties']['filter_name'] not in sd.validFilters[recipe['mode']]):
               print(f"Recipe {name} Filter value of {recipe['properties']['filter_name']} not valid for mode {recipe['mode']}")
               goodInput = False
                
            # check ND filter values, if any    
            if('ndfilter_name' in recipe['properties']):
               if(recipe['properties']['ndfilter_name'] not in sd.validND[recipe['mode']]):
                  print(f"Recipe {name} ND Filter value of {recipe['properties']['ndfilter_name']} not valid")
                  goodInput = False

            # catg, type and tech in list of valid values. update list in simulationDefinitions as needed
 
            if(recipe['properties']['catg'] not in sd.catgVals):
               print(f"Recipe {name} has invalid CATG of {recipe['properties']['catg']})")
               goodInput = False
            if(recipe['properties']['tech'] not in sd.techVals):
               print(f"Recipe {name} has invalid TECH of {recipe['properties']['tech']})")
               goodInput = False
            if(recipe['properties']['type'] not in sd.typeVals):
               print(f"Recipe {name} has invalid TYPE of {recipe['properties']['type']})")
               goodInput = False
            if(recipe['mode'] not in sd.modeVals):
               print(f"Recipe {name} has invalid MODE of {recipe['mode']})")
               goodInput = False
        
            # nObs, ndit > 0 
            
            if(not isinstance(recipe["properties"]["nObs"], int)):
               print(f"Recipe {name} has invalid NOBS of {recipe['properties']['nObs']})")
               goodInput = False
            elif(recipe["properties"]["nObs"] <= 0):
                print(f"Recipe {name} has invalid NOBS of {recipe['properties']['nObs']})")
                goodInput = False
        
            if(not isinstance(recipe["properties"]["ndit"], int)):
               print(f"Recipe {name} has invalid NDIT of {recipe['properties']['ndit']})")
               goodInput = False
            elif(recipe["properties"]["ndit"] <= 0):
                print(f"Recipe {name} has invalid NDIT of {recipe['properties']['ndit']})")
                goodInput = False
        
            # note that dit can be a number or a list
            
            if(type(recipe["properties"]["dit"]) is list):
                for elem in recipe["properties"]["dit"]:
                    if(not isinstance(elem, (int,float))):
                        print(f"Recipe {name} has invalid DIT of {recipe['properties']['dit']})")
                        goodInput = False
                    elif(elem <= 0):
                        print(f"Recipe {name} has invalid DIT of {recipe['properties']['dit']})")
                        goodInput = False
            else:
                if(not isinstance(recipe["properties"]["dit"], (int,float))):
                    print(f"Recipe {name} has invalid DIT of {recipe['properties']['dit']})")
                    goodInput = False
                elif(recipe["properties"]["dit"] <= 0):
                    print(f"Recipe {name} has invalid DIT of {recipe['properties']['dit']})")
                    goodInput = False

        if(goodInput):
            print(f"YAML file {self.params['inputYAML']} validated")
            
        return goodInput
                      
    def calcDark(self,props):

        """determine what sort of dark, if any, is needed for a YAML entry and return a recipe dictionary for it"""
    
        if(np.all(["DARK" not in props['type'],"PERSISTENCE" not in props['type']])):
            if(",LM" in props['tech']):
                df = copy.deepcopy(sd.DARKLM)
                df['mode'] = "img_lm"
            elif(",N" in props['tech']):
                df = copy.deepcopy(sd.DARKN)
                df['mode'] = "img_n"
            elif(np.any(["LMS" in props['tech'],"IFU" in props['tech']])):
                df = copy.deepcopy(sd.DARKIFU)
                df['mode'] = "lms"
            else:
                return{}
    
            df['properties']['dit'] = props['dit']
            df['properties']['ndit'] = props['ndit']
            df['properties']['nObs'] = self.params['doCalib']

            return df
        else:
           return {}

    def calcWcuDark(self,props):

        """determine what sort of dark, if any, is needed for a YAML entry and return a recipe dictionary for it"""
    
        if(np.all(["DARK" not in props['type'],"PERSISTENCE" not in props['type']])):
            if(",LM" in props['tech']):
                df = copy.deepcopy(sd.WCUDARKLM)
                df['mode'] = "img_lm"
            elif(",N" in props['tech']):
                df = copy.deepcopy(sd.WCUDARKN)
                df['mode'] = "img_n"
            elif(np.any(["LMS" in props['tech'],"IFU" in props['tech']])):
                df = copy.deepcopy(sd.WCUDARKIFU)
                df['mode'] = "lms"
            else:
                return{}

            df['properties']['dit'] = props['dit']
            df['properties']['ndit'] = props['ndit']
            df['properties']['nObs'] = self.params['doCalib']
            return df
        else:
           return {}

    def calcSkyFlat(self,props):
    
        """determine what sort of sky flat, if any, is needed for a YAML entry and return a recipe dictionary for it"""
    
        if(np.all(["DARK" not in props['type'], "FLAT" not in props['type'],"DETLIN" not in props['type'],"LMS" not in props['type'],"PERSISTENCE" not in props['type']])):
            if(",LM" in props['tech']):
                df = copy.deepcopy(sd.SKYFLATLM)
                df['mode'] = "img_lm"
            elif(",N" in props['tech']):
                df = copy.deepcopy(sd.SKYFLATN)
                df['mode'] = "img_n"
            else:
                return{}
    
            df['properties']['filter_name'] = props['filter_name']
            df['properties']['ndfilter_name'] = "open"
            df['properties']['dit'] = 0.25
            df['properties']['ndit'] = 1
            df['properties']['nObs'] = self.params['doCalib']

            return df
        else:
            return {}
    
    def calcLampFlat(self,props):
    
        """determine what sort of lamp flat, if any, is needed for a YAML entry and return a recipe dictionary for it"""
        if(np.all(["DARK" not in props['type'], "FLAT" not in props['type'],"DETLIN" not in props['type'],"LMS" not in props['type'],"PERSISTENCE" not in props['type']])):
            if(",LM" in props['tech']):
                df = copy.deepcopy(sd.LAMPFLATLM)
                df['mode'] = "img_lm"
            elif(",N" in props['tech']):
                df = copy.deepcopy(sd.LAMPFLATN)
                df['mode'] = "img_n"
            else:
                return{}
    
            df['properties']['filter_name'] = props['filter_name']
            df['properties']['ndfilter_name'] = "open"
            df['properties']['dit'] = 0.25
            df['properties']['ndit'] = 1
            df['properties']['nObs'] = self.params['doCalib']

            return df
        else:
            return {}

    def calculateCalibs(self):

        """
        determine which darks and flats should be run based on a set of recipe templates
        create a dictionary containing the results, in the same form as that for recipes
        read from the YAML file.

        The results are stored in self.calibSet. The labels for each entry are set to 
        dNNN for darks, lNNN for map flats and sNNN for sky flats, with NNN being an 
        increasing number. 
        """

        darks = []
        wcuDarks = []
        skyFlats = []
        lampFlats = []

        # assemble a list of the dark / skyflat / lampflat recipe dicionaries

        ii=0
        for name, recipe in self.dorcps.items():
            expanded = [key for key in sd.expandables
                        if isinstance(recipe["properties"][key], list)]
            combos = product(*[recipe["properties"][key] for key in expanded])

            for combo in combos:
                combodict = dict(zip(expanded, combo))
                props = recipe["properties"] | combodict
                
                try:
                    nfname = props["ndfilter_name"]
                except:
                    props["ndfilter_name"] = "open"


                if(np.any(["SLITLOSS" in props["type"],"DETLIN" in props["type"], "DISTORTION" in props["type"]])):

                    wcuDarks.append(self.calcWcuDark(props))
                    
                    
                else:
                    darks.append(self.calcDark(props))
                skyFlats.append(self.calcSkyFlat(props))
                lampFlats.append(self.calcLampFlat(props))

                ii+=1

            
        nLab = 0
        self.calibSet = {}

        # use set to get the unique values, with some json fiddling because you can't
        # use set on a list of dictionaries
        # assign each dictionary to the master dictionary, with a unique label

                      
        for rcp in np.unique([json.dumps(i, sort_keys=True) for i in darks]):
            drcp = json.loads(rcp)
            if bool(drcp):
                label = f'd{nLab}'
                nLab += 1
                self.calibSet[label] = drcp

        for rcp in np.unique([json.dumps(i, sort_keys=True) for i in wcuDarks]):
            drcp = json.loads(rcp)
            if bool(drcp):
                label = f'd{nLab}'
                nLab += 1
                self.calibSet[label] = drcp

        for rcp in np.unique([json.dumps(i, sort_keys=True) for i in skyFlats]):
            drcp = json.loads(rcp)
            if bool(drcp):
                label = f's{nLab}'
                nLab += 1
                self.calibSet[label] = drcp

        for rcp in np.unique([json.dumps(i, sort_keys=True) for i in lampFlats]):
            drcp = json.loads(rcp)
            if bool(drcp):
                label = f'l{nLab}'
                nLab += 1
                self.calibSet[label] = drcp

        print("Calculated calibration set")
        
    def generateFilename(self,dateobs,doCatg,dit,prefix):
    
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
        
        sdate = dateobs.isoformat(":", 'seconds')
        sdate = sdate.replace(":", "_")
        
        fname = f'METIS.{prefix}.{sdate.replace(":","_")}.fits'
                
        return fname
                
    def dumpCalibsToFile(self):

        """
        Dump the calibration yaml recipes to a file, similar to the recipes YAML file
        """
        
        with open(self.params['calibFile'], 'w') as outfile:
            yaml.dump(self.calibSet, outfile, default_flow_style=False)
    
    def updateHeaders(self):
    
        """
        add keywords to a list of files, fixing anything that isn't handled by ScopeSim. 
        
        DPR .TECH, .FILTER and .TYPE are set by ScopeSim, DRS.FILTER .NDFILTER, 
        and DET.DIT and .NDIT are set in ScopeSim
    
        We use the TECH to get INS.MODE
        Sets the DRS.SLIT to the default value for now (will fix later)\TODO
        Sets INS.OPTI*.NAME to the filter, slit as indicated by the TECH, FILTER and SLIT keyword
    
        For HCI / Coronagraph modes, we set the TECH keyword to a non valid value in Scopesim, 
        and use that to set the DRS.MASK, correct DPR.TECH, and INS.OPTI*.NAME values. This is kludgy,
        and will be fixed later. \TODO
    
        We check the TYPE keyword for LASER Sources. 
    
        The correct MJD date is written

        Adjusted files **WILL OVERWRITE EXISTING FILES**

        The list of files is compiled during the previous running of the simulations
        """
        
    
        for fName,mjd in zip(self.allFileNames,self.allmjd):
            print(f'Processing {fName}')
            # open the file
            hdul = fits.open(fName)

            for hdu in hdul:
                # Remove lower case keywords, in particular "pixel_size"
                for k in hdu.header:
                    if k.upper() != k:
                        print(f"Lower case keyword found and removed: {k}")
                        hdu.header.pop(k)

            hdul[0].header['MJD-OBS'] = mjd
            
            #if type(hdul[0].header['MJD-OBS']) == str:
            #    mjdobs = hdul[0].header['MJD-OBS']
            #    hdul[0].header['MJD-OBS'] = astropy.time.Time(mjdobs,format="isot").mjd
            # get the tech and filter keywords
           
            tech = hdul[0].header['HIERARCH ESO DPR TECH']
            filt = hdul[0].header['HIERARCH ESO DRS FILTER']
    
            if(tech == "LSS,LM"):
                hdul[0].header['HIERARCH ESO INS MODE'] = "SPEC_LM"
                hdul[0].header['HIERARCH ESO INS OPTI9 NAME'] = filt
                hdul[0].header['HIERARCH ESO INS DRS SLIT'] = "C-38_1"
            if(tech == "LSS,N"):
                hdul[0].header['HIERARCH ESO INS MODE'] = "SPEC_N_LOW"
                hdul[0].header['HIERARCH ESO INS OPTI12 NAME'] = filt
                hdul[0].header['HIERARCH ESO INS DRS SLIT'] = "C-38_1"
            
            #IMAGING
            if(tech == "IMAGE,LM"):
                hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_LM"
                hdul[0].header['HIERARCH ESO INS OPTI10 NAME'] = filt
            if(tech == "IMAGE,N"):
                hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_N"
                hdul[0].header['HIERARCH ESO INS OPTI13 NAME'] = filt
            
            #IFU
            if(tech == "LMS"):
                hdul[0].header['HIERARCH ESO INS MODE'] = "IFU_nominal"
                hdul[0].header['HIERARCH ESO INS OPTI6 NAME'] = filt
                hdul[0].header['HIERARCH ESO DRS IFU'] = filt
                hdul[0].header['HIERARCH ESO DPR TECH'] = "IFU"
                
            #HCI
            if(tech == "RAVC,LM"):
                hdul[0].header['HIERARCH ESO INS OPTI10 NAME'] = filt
                hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_LM_RAVC"
                hdul[0].header['HIERARCH ESO DRS MASK'] = "VPM-L,RAP-LM,RLS-LMS"
                hdul[0].header['HIERARCH ESO INS OPTI1 NAME'] = "RAP-LM"
                hdul[0].header['HIERARCH ESO INS OPTI3 NAME'] = "VPM-L"
                hdul[0].header['HIERARCH ESO INS OPTI5 NAME'] = "RLS-LMS"
                hdul[0].header['HIERARCH ESO DPR TECH'] = "IMAGE,LM"
            
            if(tech == "APP,LM"):
                hdul[0].header['HIERARCH ESO INS OPTI10 NAME'] = filt
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
    
            
            
            hdul.writeto(fName,overwrite=True)
            hdul.close()

        
    def runSimulations(self):

        """Calls _run for main recipes"""
        
        self._run(self.dorcps)
        
    def runCalibrations(self):

        """Calls _run for calibration recipes"""

        self._run(self.calibSet)
        

    def _run(self,dorcps):
        
        """
        Run the set of recipes contained in the passed dictionary
        
        If testRun is set, everything except the simulation will be done. 

        Most of the routines handles some bookkeeping/formatting with the dictionaries,
        and handling the various options for the observation date/time. 
        """
        
        # if the output directory doesn't exist, create it
        
        out_dir = Path(self.params['outputDir'])
        out_dir.mkdir(parents=True, exist_ok=True)

        allArgs = []
        
        # cycle through all the recipes
        for name, recipe in dorcps.items():

    
            # expand the expandables

            expanded = [key for key in sd.expandables
                        if isinstance(recipe["properties"][key], list)]
            combos = product(*[recipe["properties"][key] for key in expanded])
    
            # get the mode and the prefix for the title
            
            mode = recipe["mode"]
            prefix = recipe["do.catg"]
            nObs = recipe["properties"]["nObs"]
    
            # cycle through the combos (may only be one)
            for combo in combos:
    
                # extract the properties and combine with the combo dictionary
                
                combodict = dict(zip(expanded, combo))
                props = recipe["properties"] | combodict
                # a blank value of ndfilter_name if not explicitly given
                try:
                    nfname = props["ndfilter_name"]
                except:
                    props["ndfilter_name"] = "open"
    
                    
                # first iteration, need to intialize dateobs regardless of method for timestamp
                if(self.firstIt):
    
                    #if sequence=True, we get this from startMJD if set, or the YAML file
                    if(self.params['sequence']):
                                
                        if(self.params['startMJD'] is not None):
                            self.tObs = Time(datetime.strptime(self.params['startMJD'], '%Y-%m-%d %H:%M:%S'))
                        elif "dateobs" in recipe["properties"]:
                            self.tObs = Time(recipe["properties"]["dateobs"])[0]
                        else:
                            print("No appropriate starting time found; setting to default value")
                            self.tObs = Time(datetime.strptime("2027-01-25 00:00:00", '%Y-%m-%d %H:%M:%S'))
    
                        # tDelt is 0 because we've just set the value
                        
                    #if sequence = False, get from the YAML file
                    else:
                        if "dateobs" in recipe["properties"]:
                            self.tObs = Time(recipe["properties"]["dateobs"])[0]
                        else:
                            print("No appropriate starting time found; exiting")
                            return
                    self.firstIt = False
    
                # if this isn't the first iteration, we increment if sequence=True,
                # otherwise get from the YAML entry. If the YAML  doesn't have an dateobs set
                # increment as for the seuqence case
                else:
                    if(not self.params['sequence']):
                        # set explicitly, and tDelt = 0
                        if "dateobs" in recipe["properties"]:
                            self.tObs = Time(recipe["properties"]["dateobs"])[0]
                            self.tDelt = TimeDelta(0, format='sec') 
                        else:
                            print("No appropriate starting time found; exiting")
                            return
    
    
                # for nObs exposures of each set of parameters
                for _ in range(nObs):        
    
                    # note that tDelt = 0 if we've explicitly set it above
                    self.tObs = self.tObs + self.tDelt

                    # update the dateobs in the dictionary
                    props["dateobs"] = self.tObs.tt.datetime
                    props["MJD-OBS"] = self.tObs.mjd
                    # update tDelt for the next iteration
                    self.tDelt = TimeDelta(props['dit']*props['ndit']*1.2+1, format='sec')   

                    # get the filename
                    fname = out_dir / self.generateFilename(props['dateobs'],mode,props['dit'],prefix)
                    self.allFileNames.append(fname)
                    self.allmjd.append(self.tObs.mjd)
                    print("Starting simulate()")
                    print(f"    fname={fname}")
                    print(f'    source =  {recipe["source"]}')
    
                    # get kwargs for scopeSim
                    kwargs = NestedMapping({"OBS": props})
                    print(f"    dit={props['dit']},ndit={props['ndit']},catg={props['catg']},tech={props['tech']},type={props['type']},filter_name={props['filter_name']}, ndfilter_name={props['ndfilter_name']}")

                    # keep track of the list of arguments
                    allArgs.append((fname,mode,kwargs,recipe["source"],self.params["small"]))
    
        # and run the


        if not self.params['testRun']:
            nCores = self.params['nCores']

            with Pool(nCores) as pool:
                pool.starmap(simulate, allArgs)
                #simulate(fname, mode, kwargs, source=recipe["source"], small=self.params['small'])
                pool.close()
                pool.join()
    
                       


