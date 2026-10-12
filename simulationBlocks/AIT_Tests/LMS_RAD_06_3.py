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

subDir = ["AIT_Tests","IFU","LMS_RAD_06_3"]

if __name__ == '__main__':    

        params = {}
        params['outputDir'] = os.path.join(outputDir,*subDir)
        params['subDir'] = os.path.join(*subDir)
        params['doStatic'] = False
        params['doCalib'] = 0
        params['startMJD'] =  "2028-01-25 05:00:00"
        params['nCores'] = nCores
        
        yamls = ["LMS_RAD_06/LMS_RAD_06_3.yaml"]
        

        yamlFiles = []
        for y in yamls:
            yamlFiles.append(os.path.join(yamlDir,y))
        
        rs.runSimulationBlock(yamlFiles,params,sys.argv[1:])
        

