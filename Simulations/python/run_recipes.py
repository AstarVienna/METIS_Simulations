#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" run a set of recipes from a YAML file"""


import runRecipes as rr
import sys
import makeCalibPrototypes
from pathlib import Path

def runRecipes_with_pars(inputYAML=Path(__file__).parent.parent / "YAML" / "allRecipes.yaml", 
                                       outputDir="output/", 
                                       small=False, 
                                       doStatic=True, 
                                       catglist=None,
                                       doCalib=1, 
                                       sequence='1', 
                                       testRun=False, 
                                       calibFile=None, 
                                       nCores=8, 
                                       irdb_path='./inst_pks', 
                                       **kwargs):
    """
    Run a set of recipes with explicit arguments instead of command line.
    Arguments:
        inputYAML: Path to the input YAML file.
        doCalib: Integer flag for calibration.
        calibFile: Path to calibration file.
        testRun: Boolean flag for test run.
        doStatic: Boolean flag for static calibration.
        outputDir: Output directory.
        kwargs: Any additional parameters.
    """
    simulationSet = rr.runRecipes()

    # Set parameters directly
    simulationSet.setParms(
        irdb_path=irdb_path,
        inputYAML=inputYAML,
        outputDir=outputDir,
        small=small,
        doStatic=doStatic,
        catglist=catglist,
        doCalib=doCalib,
        sequence=sequence,
        testRun=testRun,
        calibFile=calibFile,
        nCores=nCores,
        **kwargs
    )

    # read in the YAML
    simulationSet.loadYAML()

    # validate the YAML
    goodInput = simulationSet.validateYAML()

    # exit if the YAML entries are not valid
    if not goodInput:
        return

    # if requested, get the list of flats and darks
    if simulationSet.params['doCalib'] > 0:
        simulationSet.calculateCalibs()

    # run the simulations
    simulationSet.runSimulations()
    
    # run the calibrations if requested
    if simulationSet.params['doCalib'] > 0:
        simulationSet.runCalibrations()

        # if requested, dump the calibration dictionary to a YAML file in the same format as the input YAML
        if simulationSet.params['calibFile'] is not None:
            simulationSet.dumpCalibsToFile()

    simulationSet.allFileNames.sort()
    for elem in simulationSet.allFileNames:
        print(elem)


    # if simulations were done, update the headers
    if not simulationSet.params['testRun']:
        simulationSet.updateHeaders()

    if simulationSet.params['doStatic']:
        makeCalibPrototypes.generateStaticCalibs(simulationSet.params['outputDir'])

def runRecpies_with_argv(argv):
    simulationSet = rr.runRecipes()
    simulationSet.parseCommandLine(argv[1:])
    runRecipes_with_pars(**simulationSet.params)
        
if __name__ == "__main__":
    runRecpies_with_argv(sys.argv)
