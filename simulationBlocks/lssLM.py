#!/usr/bin/env python
"""
An example of running an observation block
"""

from metis_simulations import runSimulationBlock as rs
import os
import sys

yamlDir = os.environ['MSIM_YAML_DIR']
nCores = os.environ['MSIM_NCORES']
outputDir = os.environ['MSIM_OUTDIR']


if __name__ == "__main__":
    params = {}
    params['outputDir'] = os.path.join(outputDir,"lssLM")
    params['small'] = False
    params['doStatic'] = True
    params['doCalib'] = 2
    params['sequence'] = True
    params['startMJD'] =  "2027-01-27 00:00:00"
    params['calibFile'] = None
    params['nCores'] = nCores
    params['testRun'] = False

    yamls = ["scienceLSSLM.yaml","stdLSSLM.yaml","detlinLM.yaml","distortionLM.yaml","rsrfLSSLM.yaml","rsrfPinhLSSLM.yaml","wavecalLSSLM.yaml","slitlossLSSLM.yaml"]


    yamlFiles = []
    for y in yamls:
        yamlFiles.append(os.path.join(yamlDir,y))
        
    rs.runSimulationBlock(yamls,params,sys.argv[1:])
