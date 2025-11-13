#!/usr/bin/env python

from simulation import Simulation
import makeCalibPrototypes as mcp


def runSimulationBlock(yamlFiles, params):

    """runs a sequence of yaml files with a set of command line parameters"""

    allDarks = []
    allFlats = []
    for yamlFile in yamlFiles:
        params['inputYAML'] = yamlFile

        # instantiate a simulation set and assign the general parameters

        simulationSet = Simulation()
        simulationSet.params = params

        # load the YAML file

        simulationSet.loadYAML()

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

    # now do all the calibrations

    allDarks = list(set(allDarks))
    allFlats = list(set(allFlats))

    simulationSet.allFileNames = []
    simulationSet.allmjd = []

    simulationSet.calculateDarks(allDarks)
    print(allFlats)
    simulationSet.calculateFlats(allFlats,"skyFlat")
    simulationSet.calculateFlats(allFlats,"lampFlat")

    if(params['doStatic'] == True):
        mcp.generateStaticCalibs(params['outputDir'])
    if not params['testRun']:
        simulationSet.updateHeaders()

if __name__ == "__main__":
    pass
