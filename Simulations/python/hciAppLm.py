#!/usr/bin/env python
"""
An example of running an observation block
"""

import runSimulationBlock as rs
if __name__ == '__main__':

    params = {}
    params['outputDir'] = "output/hciAppLM"
    params['small'] = False
    params['doStatic'] = True
    params['doCalib'] = 2
    params['sequence'] = True
    params['startMJD'] =  "2027-01-25 00:00:00"
    params['calibFile'] = None
    params['nCores'] = 8
    params['testRun'] = False
    
    yamlFiles = ["YAML/offAxisLM.yaml","YAML/hciAppLM.yaml","YAML/distortionLM.yaml","YAML/detlinLM.yaml"]
    
    rs.runSimulationBlock(yamlFiles,params)


