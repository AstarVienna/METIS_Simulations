#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" run a set of recipes from a YAML file"""


import runRecipes as rr
import sys
import makeCalibPrototypes


def runRecipes(argv):
    
    simulationSet = rr.runRecipes()

    #simulationSet.setParms(inputYAML = None) \TODO - set parameters directly rather than commandline

    # get the command line arguments
    
    simulationSet.parseCommandLine(argv[1:])

    # read in the YAML
    simulationSet.loadYAML()

    # validate the YAML
    
    goodInput = simulationSet.validateYAML()

    # exit if the YAML entries are not valid
    if (not goodInput):
        exit

    # if requested, get the list of flats and darks
    if(simulationSet.params['doCalib'] > 0):
        simulationSet.calculateCalibs()

    # run the simulations
    simulationSet.runSimulations()
    
    # run the calibrations if requested
    if(simulationSet.params['doCalib'] > 0):
        simulationSet.runCalibrations()

        # if requested, dump the calibration dictionary to a YAML file in the same format as the input YAML
        if(simulationSet.params['calibFile'] is not None):
            simulationSet.dumpCalibsToFile()

    simulationSet.allFileNames.sort()
    for elem in simulationSet.allFileNames:
        print(elem)


    # if simulations were done, update the headers
    if(not simulationSet.params['testRun']):
        simulationSet.updateHeaders()

    if(simulationSet.params['doStatic']):
        makeCalibPrototypes.generateStaticCalibs(simulationSet.params['outputDir'])
        
if __name__ == "__main__":
    
    runRecipes(sys.argv)
