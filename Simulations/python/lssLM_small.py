#!/usr/bin/env python
"""
An example of running an observation block
"""

import runSimulationBlock as rsb


if __name__ == "__main__":
    params = {}
    params['outputDir'] = "outputSmall/lssLM"
    params['small'] = True
    params['doStatic'] = True
    params['doCalib'] = 2
    params['sequence'] = True
    params['startMJD'] =  "2027-01-25 00:00:00"
    params['calibFile'] = None
    params['nCores'] = 8
    params['testRun'] = False

    yamlFiles = ["YAML/scienceLSSLM.yaml","YAML/stdLSSLM.yaml","YAML/detlinLM.yaml","YAML/distortionLM.yaml","YAML/rsrfLSSLM.yaml","YAML/rsrfPinhLSSLM.yaml","YAML/wavecalLSSLM.yaml"]

    rsb.runSimulationBlock(yamlFiles,params)

