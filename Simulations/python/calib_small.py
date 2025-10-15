#!/usr/bin/env python
"""
An example of running an observation block
"""

import runSimulationBlock as rsb


if __name__ == "__main__":
    params = {}
    params['outputDir'] = "outputSmall/Calib"
    params['small'] = True
    params['doStatic'] = True
    params['doCalib'] = 2
    params['sequence'] = True
    params['startMJD'] =  "2027-01-25 00:00:00"
    params['calibFile'] = None
    params['nCores'] = 8
    params['testRun'] = False

    yamlFiles = ["YAML/chophomeLM.yaml","YAML/pupilLM.yaml","YAML/pupilN.yaml","YAML/slitlossLSSLM.yaml","YAML/slitlossLSSN.yaml"]

    rsb.runSimulationBlock(yamlFiles,params)

