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
        params['outputDir'] = os.path.join(outputDir,"LMS_OPT_1")
        params['small'] = False
        params['doStatic'] = False
        params['doCalib'] = 0
        params['sequence'] = True
        params['startMJD'] =  "2028-01-25 00:00:00"
        params['calibFile'] = None
        params['nCores'] = nCores
        params['testRun'] = False
        
        yamls = ["LMS_OPT_01/LMS_OPT_1.yaml"]
        

        yamlFiles = []
        for y in yamls:
            yamlFiles.append(os.path.join(yamlDir,y))
        
        rs.runSimulationBlock(yamlFiles,params,sys.argv[1:])
        

