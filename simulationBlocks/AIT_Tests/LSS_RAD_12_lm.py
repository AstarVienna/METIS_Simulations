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

if __name__ == '__main__':    

        params = {}
        params['outputDir'] = os.path.join(outputDir,"LSS_RAD_12_lm")
        params['small'] = False
        params['doStatic'] = False
        params['doCalib'] = 0
        params['sequence'] = True
        params['startMJD'] =  "2028-01-25 16:00:00"
        params['calibFile'] = None
        params['nCores'] = nCores
        params['testRun'] = False
        
        yamls = ["LSS_RAD_12/LSS_RAD_12_lm.yaml"]
        

        yamlFiles = []
        for y in yamls:
            yamlFiles.append(os.path.join(yamlDir,y))
        
        rs.runSimulationBlock(yamlFiles,params,sys.argv[1:])
        

