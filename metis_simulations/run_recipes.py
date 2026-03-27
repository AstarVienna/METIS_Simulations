#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" run a set of recipes from a YAML file"""
#!/usr/bin/env python


import setupSimulations as rr
import sys
import makeCalibPrototypes


def runRecipes(argv):
    
    simulationSet = rr.setupSimulations()

    #simulationSet.setParms(inputYAML = None) \TODO - set parameters directly rather than commandline

    # get the command line arguments
    
    simulationSet.parseCommandLine(argv[1:])
    # read in the YAML
    simulationSet.loadYAML()
    simulationSet.getStartDate()

    # if requested, get the list of flats and darks
    if(simulationSet.params['doCalib'] > 0):
        simulationSet.calculateCalibs()

    # run the simulations
    simulationSet.runSimulations()
    
    # run the calibrations if requested
    if(simulationSet.params['doCalib'] > 0):
        simulationSet.calculateDarks(simulationSet.darkParms)
        simulationSet.calculateFlats(simulationSet.flatParms)

    # if simulations were done, update the headers
    if(not simulationSet.params['testRun']):
        simulationSet.updateHeaders()
        
    if(simulationSet.params['doStatic']):
        makeCalibPrototypes.generateStaticCalibs(simulationSet.params['outputDir'])
        
if __name__ == "__main__":
    
    runRecipes(sys.argv)
