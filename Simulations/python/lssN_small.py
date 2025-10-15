#!/usr/bin/env python
"""
An example of running an observation block
"""

import runSimulationBlock as rsb


if __name__ == "__main__":
    params = {}
    params['outputDir'] = "outputSmall/lssN"
    params['small'] = True
    params['doStatic'] = True
    params['doCalib'] = 2
    params['sequence'] = True
    params['startMJD'] =  "2027-01-25 00:00:00"
    params['calibFile'] = None
    params['nCores'] = 8
    params['testRun'] = False

    yamlFiles = ["YAML/scienceLSSN.yaml","YAML/stdLSSN.yaml","YAML/detlinN.yaml","YAML/distortionN.yaml","YAML/rsrfLSSN.yaml","YAML/rsrfPinhLSSN.yaml","YAML/wavecalLSSN.yaml"]

    rsb.runSimulationBlock(yamlFiles,params)

