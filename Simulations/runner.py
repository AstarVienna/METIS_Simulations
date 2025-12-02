#!/usr/bin/env python
import copy
import multiprocessing as mp

from scalyca import Scalyca

from python.setupSimulations import Simulation



class SimulationRunner(Scalyca):
    _prog = "ScopeSim simulation runner"
    _version = "0.0.1"

    def add_arguments(self):
        self.add_argument('--cores', '-j', default=mp.cpu_count() - 1)

    def main(self):
        """runs a sequence of yaml files with a set of command line parameters"""

        allDarks = []
        allFlats = []

        for yaml_file in self.config.yaml_files:
            params = copy.copy(self.config.parameters)
            params['nCores'] = self.args.cores
            params = params.toDict()

            params['inputYAML'] = yaml_file

            # instantiate a simulation set and assign the general parameters

            simulationSet = Simulation()
            simulationSet.params = params

            # load the YAML file

            simulationSet.loadYAML()

            # get the start date
            simulationSet.getStartDate()

            # run the simulations
            simulationSet.runSimulations()

            if not params['test_run']:
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




SimulationRunner().run()

