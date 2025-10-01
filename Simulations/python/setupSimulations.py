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
from multiprocessing import Pool,Process,Manager
from astropy.io import fits

import numpy as np
import yaml
import argparse
import json
import astropy
import copy
import sys

import simulationDefinitions as sd
from scopesimWrapper import simulate

class setupSimulations():

    def __init__(self):
        
        self.calibSet = None
        self.tObs = None
        self.firstIt = True
        self.tDelt = TimeDelta(0, format='sec') 
        self.allFileNames = []
        self.allmjd = []

        with Path("python/templates.yaml").open(encoding="utf-8") as file:
            self.templates =  yaml.safe_load(file)


    def parseCommandLine(self,args):

        """
        parse the command line

        Input YAML file is required; other arguments are optional. 

        Returns a dictionary of command line options
        """

        
        parser = argparse.ArgumentParser()

        parser.add_argument('-i', '--inputYAML', type=str,
                            help='input YAML File')
        
        parser.add_argument('-o', '--outputDir', type=str,
                            default = "output/",
                            help='output directory')
        
        parser.add_argument('-s', '--small', action = "store_true",
                            default=False,
                            help=('use detectors of 32x32 pixels; ' +
                                  'for running in the continuous integration'))
        
        parser.add_argument('-e', '--doStatic', action = "store_true",
                            default=False,
                            help=('Generate prototypes for static/external calibration files'))
        
        parser.add_argument('-d', '--doCalib', type=int,
                            default=0,
                            help='automatically generate darks and flats for the dataset. Will generate N of each type')

        # expects either 1 or a date stamp
        parser.add_argument('-q', '--sequence', type=str,
                            default=False,
                            help='options for generating timestamps. Set to a date in the form yyyy-mm-dd hh:mm:ss to start from a specific date, or 1 to use the first dateobs in the YAML file.')

        # if set, option to true
        parser.add_argument('-t', '--testRun', action="store_true",
                            help='run the script without executing simulate to check input')

        parser.add_argument('-f', '--calibFile', type=str,
                            default = None,
                            help='File to dump calibration file YAML to')
        
        parser.add_argument('-n', '--nCores', type=int,
                            default = 1,
                            help='number of cores for parallel processing')

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

        self.params = params

    def loadYAML(self):

        """
        read in a YAML file of recipe templates and filter as specified by command line arguments
        """
        
        with Path(self.params['inputYAML']).open(encoding="utf-8") as file:
            self.allrcps =  yaml.safe_load(file)

        print(f"Recipes loaded from {self.params['inputYAML']}")
        
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
        self.tDelt =  TimeDelta(float(recipe['properties']['dit'])*recipe['properties']['ndit']*1.2+1, format='sec')
        recipe["properties"]["dateobs"] = self.tObs.tt.datetime
        recipe["properties"]["MJD-OBS"] = self.tObs.mjd
        recipe["properties"]["tplexpno"] = self.tplExpno

        self.fname = self.outDir / self.generateFilename(recipe["properties"]['dateobs'],recipe['mode'],recipe["properties"]['dit'],recipe["do.catg"])
        self.tplExpno += 1

        return recipe

    def copyRecipe(self,tpe,band):
        
        if(",LM" in band):
            recipe = json.loads(json.dumps(self.templates[tpe]["lm"]))
        elif(",N" in band):
            recipe = json.loads(json.dumps(self.templates[tpe]["n"]))
        elif(np.any(["LMS" in band,"IFU" in band])):
            recipe = json.loads(json.dumps(self.templates[tpe]["ifu"]))
        return recipe

    def calculateFlats(self,flatParams,tpe):
        
        allArgs = []
        for elem in flatParams:
            # do a separate template for each set of parameters
            tplStart = self.tObs.tt.datetime

            # now for each iteration
            for i in range(self.params['doCalib']):

                recipe = self.copyRecipe(tpe,elem[2])
                if("wcu" not in recipe.keys()):
                    recipe["wcu"] = None

                recipe["properties"]["tplstart"] = tplStart
                recipe["properties"]["filter_name"] = elem[0]
                recipe["properties"]["ndfilter_name"] = elem[1]

 
                recipe = self.increment(recipe)

                self.allFileNames.append(self.fname)
                self.allmjd.append(self.tObs.mjd)

                # append teh arguments to the 
                allArgs.append((self.fname,recipe,self.params["small"]))
                simulate(self.fname, recipe, small=self.params['small'])
        # now actually run
        #if(not self.params['testRun']):
        #    nCores = self.params['nCores']
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
            nCores = self.params['nCores']
        
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
            # get the mode and the prefix for the title
            
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

                # if the observation is WCU, add a WCU frame to the image, as WCU darks are part of the
                # same template \TODO set to > 1 if desired
            
                if(recipe["wcu"] is not None):
                    recipeDark = self.copyRecipe("wcuOff",recipe['properties']['tech'])
                    recipe["properties"]["tplstart"] = self.tplStart
                    recipeDark["properties"]["dit"] = recipe["properties"]["dit"] 
                    recipeDark["properties"]["ndit"] = recipe["properties"]["ndit"] 
                    recipeDark = self.increment(recipeDark)

                    self.allFileNames.append(self.fname)
                    self.allmjd.append(self.tObs.mjd)

                    allArgs.append((self.fname, recipeDark, self.params["small"]))

        # calculate the observation date for the next observation, for
        # stringing a sequence of templates together
        
        self.tObs = self.tObs + self.tDelt
        self.endDate = self.tObs.tt.datetime.replace(microsecond=0)

        # now actually run
        if(not self.params['testRun']):
            nCores = self.params['nCores']
        
            with Pool(nCores) as pool:
                pool.starmap(simulate, allArgs)
                #simulate(fname, recipe, small=self.params['small'])
                pool.close()
                pool.join()

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
            flatParms.append((props['filter_name'],props['ndfilter_name'],props['tech']))
                             
        self.darkParms = darkParms
        self.flatParms = flatParms
        
        
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
            if(tech == "LMS"):
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
    
            hdul.writeto(fName,overwrite=True)
            hdul.close()
