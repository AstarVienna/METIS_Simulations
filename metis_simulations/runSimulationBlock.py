#!/usr/bin/env python

from . import setupSimulations as ss
from . import makeCalibPrototypes as mcp

def runSimulationBlock(yamlFiles, params, args):

    """runs a sequence of yaml files with a set of command line parameters"""

    allDarks = []
    allFlats = []
    # parse any command line overrides
    
    for yamlFile in yamlFiles:
        params['inputFile'] = yamlFile

        # instantiate a simulation set and assign the general parameters
    
        simulationSet = ss.setupSimulations()
        extraParams = simulationSet.parseCommandLine(args)
        simulationSet.params = params

        # override parameters with input
        for elem in extraParams:
            if(extraParams[elem] is not None):
                simulationSet.params[elem] = extraParams[elem]

        simulationSet.params['nCores'] = int(simulationSet.params['nCores'])

        # load the YAML file

        simulationSet.loadYAML()

        # if both --testRun and --writeYaml are set, the user only wants the
        # parsed-recipes YAML next to each CSV input — skip the rest of the
        # per-file pipeline (simulations, header updates, calib bookkeeping)
        if simulationSet.params.get('testRun') and simulationSet.params.get('writeYaml'):
            continue

        # get the start date
        simulationSet.getStartDate()

        # run the simulations
        simulationSet.runSimulations()

        if not params['testRun']:
            simulationSet.updateHeaders()

        # keep track of the date for the next template
        params['startMJD'] = simulationSet.endDate.strftime('%Y-%m-%d %H:%M:%S')

        # and a running tally of the parameters for darks and flats
        
        if(params['doCalib'] > 0):
            simulationSet.calculateCalibs()
            allDarks = allDarks + simulationSet.darkParms
            allFlats = allFlats + simulationSet.flatParms

    # if --testRun + --writeYaml were set, every input was short-circuited
    # above; nothing was simulated and self.tObs was never initialised, so the
    # calib bookkeeping below would crash. Done.
    if params.get('testRun') and params.get('writeYaml'):
        return

    # now do all the calibrations

    allDarks = list(set(allDarks))
    allFlats = list(set(allFlats))

    simulationSet.allFileNames = []
    simulationSet.allmjd = []

    simulationSet.calculateDarks(allDarks)
    simulationSet.calculateFlats(allFlats,"skyFlat")
    simulationSet.calculateFlats(allFlats,"lampFlat")

    
    if(params['doStatic'] == True):
        mcp.generateStaticCalibs(params['outputDir'])
    if not params['testRun']:
        simulationSet.updateHeaders()

if __name__ == "__main__":
    import sys

    simulationSet = ss.setupSimulations()
    params = simulationSet.parseCommandLine(sys.argv[1:])

    if params['inputFile'] is None:
        sys.exit("error: -i/--inputFile is required")
    if params['outputDir'] is None:
        sys.exit("error: -o/--outputDir is required")

    for key, default in (('small', False), ('doStatic', False),
                         ('doCalib', 0), ('testRun', False), ('nCores', 1),
                         ('writeYaml', False)):
        if params[key] is None:
            params[key] = default

    runSimulationBlock([params['inputFile']], params, sys.argv[1:])
