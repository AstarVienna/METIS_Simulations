#!/usr/bin/env python

"""
class that acts as a wrapper to batch run a set of simulations via ScopeSim
for developing the METIS pipeline. 

Input is in the form of a YAML file containing instrumental and source
information for a single METIS observations template. 

If the template uses the WCU, WCU dark exposures will automatically
be calculated and executed as part of the template. 

Necessary darks, lamp flats and twilight flats can be determined and 
executed after the template, with each unique set of parameters a
separate template. 

This class is generally executed via the command line wrapper 
runTemplates.py 
"""

from pathlib import Path
from astropy.time import Time, TimeDelta
from itertools import product
from datetime import datetime
from multiprocessing import Pool,Process,Manager,cpu_count
from astropy.io import fits

import numpy as np
import yaml
import argparse
import json
import astropy
import copy
import sys

from . import simulationDefinitions as sd
from .scopesimWrapper import simulate
from .csvParser import loadCSV
import importlib.resources as resources

class setupSimulations():

    def __init__(self):
        
        self.calibSet = None
        self.tObs = None
        self.firstIt = True
        self.tDelt = TimeDelta(0, format='sec') 
        self.allFileNames = []
        self.allmjd = []

        with resources.open_text('metis_simulations', 'templates.yaml') as file:
            self.templates =  yaml.safe_load(file)


    def parseCommandLine(self,args):

        """
        parse the command line

        Input YAML file is required; other arguments are optional. 

        Returns a dictionary of command line options
        """

        
        parser = argparse.ArgumentParser()

        parser.add_argument('-i', '--inputFile', type=str, default=None,
                            help='input file (YAML or CSV)')
        
        parser.add_argument('-o', '--outputDir', type=str, default=None,
                            help='output directory')
        
        parser.add_argument('-s', '--small', action = "store_true", default=None,
                            help=('use detectors of 32x32 pixels; ' +
                                  'for running in the continuous integration'))
        
        parser.add_argument('-e', '--doStatic', action = "store_true", default=None,
                            help=('Generate prototypes for static/external calibration files'))
        
        parser.add_argument('-d', '--doCalib', type=int, default=None,
                            help='automatically generate darks and flats for the dataset. Will generate N of each type')

        # expects either 1 or a date stamp
        parser.add_argument('-q', '--sequence', type=str, default=None,
                            help='options for generating timestamps. Set to a date in the form yyyy-mm-dd hh:mm:ss to start from a specific date, or 1 to use the first dateobs in the YAML file.')

        # if set, option to true
        parser.add_argument('-t', '--testRun', action="store_true", default=None,
                            help='run the script without executing simulate to check input')

        parser.add_argument('-f', '--calibFile', type=str, default=None,
                            help='File to dump calibration file YAML to')
        
        parser.add_argument('-n', '--nCores', type=int, default=None,
                            help='number of cores for parallel processing')

        parser.add_argument('-w', '--writeYaml', action="store_true", default=None,
                            help='write a YAML file with the parsed recipes next to the input CSV (only meaningful with .csv input). Combine with --testRun to skip simulation entirely.')

        inArgs = parser.parse_args(args)
        params = vars(inArgs)

        if(params['sequence'] == "1"):
            params['startMJD'] = None
            params['sequence'] = True
        elif(params['sequence'] == False):
             params['sequence'] = False
             params['startMJD'] = None
        else:
             params['startMJD'] = params['sequence']
             params['sequence'] = True

        return params

    def loadInput(self):

        """
        Read in a file of recipe templates. Supports YAML and CSV formats,
        dispatching based on file extension.
        """

        input_path = Path(self.params['inputFile'])
        ext = input_path.suffix.lower()

        if ext in ('.yaml', '.yml'):
            with input_path.open(encoding="utf-8") as file:
                self.allrcps = yaml.safe_load(file)
            print(f"Recipes loaded from {input_path}")
        elif ext == '.csv':
            self.allrcps = loadCSV(input_path, write_yaml=bool(self.params.get('writeYaml')))
        else:
            raise ValueError(f"Unsupported input format: {ext}. Use .yaml, .yml, or .csv")

    def loadYAML(self):

        """Backward-compatible alias for loadInput"""

        self.loadInput()
        
    def loadRecipe(self,fname):

        """
        read in a YAML file of recipe templates for darks/flats
        """
        
        with Path(fName).open(encoding="utf-8") as file:
            recipe =  yaml.safe_load(file)

        return recipe
        
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
    
    def getStartDate(self):

        """ 
        get the start date for a template. Either given explicitly, 
        in the first entry in the YAML file, or set to default
        """
        
        recipe =  self.allrcps[list(self.allrcps.keys())[0]]

        if(self.params['startMJD'] is not None):
            self.tObs = Time(datetime.strptime(self.params['startMJD'], '%Y-%m-%d %H:%M:%S'))
            self.startMJD = self.params['startMJD']
        elif "dateobs" in recipe["properties"]:
            self.tObs = Time(recipe["properties"]["dateobs"])[0]
            self.startMJD = recipe["properties"]["dateobs"]
        else:
            print("No appropriate starting time found; setting to default value")
            self.startMJD = "2027-01-25 00:00:00"
            self.tObs = Time(datetime.strptime(self.startMJD, '%Y-%m-%d %H:%M:%S'))
        self.tplStart = self.startMJD
        self.tempNExp = 0 # exposure number
        
    def runSimulations(self):

        """Calls _run for main recipes"""
        
        self._run(self.allrcps)


    def increment(self,recipe):

        """
        increment time/nobs related variables for a recipe
        
        update dateobs, mjd-obs, teplexpno in the recipe
        update tDelt, tplExpno for the next recipe
        set the filename
        """

        self.tObs = self.tObs + self.tDelt
        dit = recipe["properties"]['dit']
        if isinstance(dit, (list, tuple)):
            assert len(dit) == 1, f"{dit=} is a list"
            dit = dit[0]

        self.tDelt =  TimeDelta(float(dit)*recipe['properties']['ndit']*1.2+1, format='sec')

        recipe["properties"]["dateobs"] = self.tObs.tt.datetime
        recipe["properties"]["MJD-OBS"] = self.tObs.mjd

        recipe["properties"]["tplexpno"] = self.tplExpno

        self.fname = self.outDir / self.generateFilename(recipe["properties"]['dateobs'],recipe['mode'],dit,recipe["do.catg"])
        self.tplExpno += 1

        return recipe

    def copyRecipe(self,tpe,band):

        recipe = None
        if(",LM" in band):
            recipe = json.loads(json.dumps(self.templates[tpe]["lm"]))
        elif(",N" in band):
            recipe = json.loads(json.dumps(self.templates[tpe]["n"]))
        elif(np.any(["IFU" in band])):
            recipe = json.loads(json.dumps(self.templates[tpe]["ifu"]))
        return recipe

    def calculateFlats(self,flatParams,tpe):
        
        allArgs = []
        for elem in flatParams:
            # do a separate template for each set of parameters
            tplStart = self.tObs.tt.datetime

            # now for each iteration
            for i in range(self.params['doCalib']):

                # for IFU: sky flat is optional and lamp flat does not exist
                if np.any(["IFU" in elem[2]]):
                    continue

                recipe = self.copyRecipe(tpe,elem[2])

                # check if recipe was copied successfully
                if(recipe is None):
                    print(f"Warning: no flat recipe defined for template {tpe} and band {elem[2]}")
                    continue

                if("wcu" not in recipe.keys()):
                    recipe["wcu"] = None

                recipe["properties"]["tplstart"] = tplStart
                recipe["properties"]["filter_name"] = elem[0]
                recipe["properties"]["nd_filter_name"] = elem[1]

                recipe = self.increment(recipe)

                self.allFileNames.append(self.fname)
                self.allmjd.append(self.tObs.mjd)

                # append the arguments to the list
                allArgs.append((self.fname,recipe,self.params["small"]))
                simulate(self.fname, recipe, small=self.params['small'])
        # now actually run
        #if(not self.params['testRun']):
        #    nCores = max(min(self.params['nCores'], cpu_count() - 1), 1)
        #
        #    with Pool(nCores) as pool:
        #        pool.starmap(simulate, allArgs)
        #        #simulate(fname, recipe, small=self.params['small'])
        #        pool.close()
        #        pool.join()

                
    def calculateDarks(self,darkParams):

        # do a separate template for each set of parameters
        
        allArgs = []
        for elem in darkParams:
            tplStart = self.tObs.tt.datetime
            # now for each iteration

            for i in range(self.params['doCalib']):
                recipe = self.copyRecipe("dark",elem[2])
                # check if recipe was copied successfully
                if(recipe is None):
                    print(f"Warning: no dark recipe defined for band {elem[2]}")
                    continue

                recipe["wcu"] = None
                recipe["properties"]["tplstart"] = tplStart
                recipe["properties"]["dit"] = elem[0]
                recipe["properties"]["ndit"] = elem[1]
 
                recipe = self.increment(recipe)

                self.allFileNames.append(self.fname)
                self.allmjd.append(self.tObs.mjd)

                # append teh arguments to the 
                allArgs.append((self.fname,recipe,self.params["small"]))

        self.endDate = self.tObs.tt.datetime.replace(microsecond=0)
        # now actually run
        if(not self.params['testRun']):
            # Always keep one core free.
            nCores = max(min(self.params['nCores'], cpu_count() - 1), 1)
        
            with Pool(nCores) as pool:
                pool.starmap(simulate, allArgs)
                #simulate(fname, recipe, small=self.params['small'])
                pool.close()
                pool.join()

            
    def _run(self,allrcps):
        
        """
        Run the set of recipes contained for a single template
        
        If testRun is set, everything except the simulation will be done. 

        Most of the routines handles some bookkeeping/formatting with the dictionaries,
        and handling the various options for the observation date/time. 
        """
        
        # if the output directory doesn't exist, create it
        
        self.outDir = Path(self.params['outputDir'])
        self.outDir.mkdir(parents=True, exist_ok=True)

        allArgs = []
        
        # cycle through all the recipes
        for name, recipe in allrcps.items():

            # force dit to be a float
            recipe["properties"]["dit"] = float(recipe["properties"]["dit"])
            
            # get the mode and the prefix for the title
            print(recipe)
            mode = recipe["mode"]
            prefix = recipe["do.catg"]
            nObs = recipe["properties"]["nObs"]
            self.tplExpno = 0
            
            props = recipe["properties"]
            
            recipe["properties"]["tplstart"] = self.tplStart

            # for nObs exposures of each set of parameters
            # this loop mostly calculates the time variables for each
            # observation, and saves the arguments for the simulation in
            # a list. The actually calling occurs afterwards, for parallelization
            
            for _ in range(nObs):        

                # set the time related keywords and increment the observing time.
                # note that tDelt = 0 on the first iteration

                recipe = self.increment(recipe)

                self.allFileNames.append(self.fname)
                self.allmjd.append(self.tObs.mjd)

                # set WCU to None if this isn't WCU data
                if("wcu" not in recipe.keys()):
                   recipe["wcu"] = None

                # add the arguments to the list
                allArgs.append((self.fname,recipe,self.params["small"]))
                simulate(self.fname, recipe, small=self.params['small'])

                # if the observation is WCU, add a WCU frame to the image, as WCU darks are part of the
                # same template. TODO: set to > 1 if desired
            
                if(recipe["wcu"] is not None):
                    recipeDark = self.copyRecipe("wcuOff",recipe['properties']['tech'])
                    if(recipeDark is not None):
                        recipeDark["properties"]["tplstart"] = self.tplStart
                        recipeDark["properties"]["tplname"] = recipe["properties"]["tplname"]
                        recipeDark["properties"]["dit"] = recipe["properties"]["dit"] 
                        recipeDark["properties"]["ndit"] = recipe["properties"]["ndit"] 
                        recipeDark["properties"]["nd_filter_name"] = recipe["properties"]["nd_filter_name"] 
                        recipeDark["properties"]["filter_name"] = recipe["properties"]["filter_name"] 
                        recipeDark = self.increment(recipeDark)
                        
                        self.allFileNames.append(self.fname)
                        self.allmjd.append(self.tObs.mjd)
                        
                        allArgs.append((self.fname, recipeDark, self.params["small"]))
                        simulate(self.fname, recipeDark, small=self.params['small'])

        # calculate the observation date for the next observation, for
        # stringing a sequence of templates together
        
        self.tObs = self.tObs + self.tDelt
        self.endDate = self.tObs.tt.datetime.replace(microsecond=0)

        # now actually run
        if(not self.params['testRun']):
            # Always keep one core free.
            nCores = max(min(self.params['nCores'], cpu_count() - 1), 1)
        
            #with Pool(nCores) as pool:
            #    pool.starmap(simulate, allArgs)
            #    #simulate(fname, recipe, small=self.params['small'])
            #    pool.close()
            #    pool.join()

    def calculateCalibs(self):

        """
        determine which darks and flats should be run based on a set of recipe templates
        create a dictionary containing the results, in the same form as that for recipes
        read from the YAML file.

        The results are stored in self.calibSet. The labels for each entry are set to 
        dNNN for darks, lNNN for map flats and sNNN for sky flats, with NNN being an 
        increasing number. 
        """

        darkParms = []
        flatParms = []

        #list of modes that use WCU OFF
        wcuModes = ["SLITLOSS","DETLIN","DISTORTION","RSRF","CHOPHOME","PUPIL","WAVE","FLAT,LAMP"]

        # assemble a list of the dark / skyflat / lampflat recipe dicionaries

        for name, recipe in self.allrcps.items():
            props = recipe["properties"]
                
            if(props["type"] in wcuModes):
                pass
             
            else:
                darkParms.append((props['dit'],props['ndit'],props['tech']))
            flatParms.append((props['filter_name'],props['nd_filter_name'],props['tech']))

            
                             
        self.darkParms = darkParms
        self.flatParms = flatParms
        
        
