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

dirStruct = ["Test","CI"]

if __name__ == '__main__':    

        params = {}
        params['outputDir'] = os.path.join(outputDir,*dirStruct)
        params['subDir'] = os.path.join(*dirStruct)
        params['small'] = True
        params['doStatic'] = True
        params['doCalib'] = 0
        params['startMJD'] =  "2027-01-25 00:00:00"
        params['nCores'] = nCores
        
        yamls = ["ci.yaml"]

        
        yamlFiles = []
        for y in yamls:
            yamlFiles.append(os.path.join(yamlDir,y))

        rs.runSimulationBlock(yamlFiles,params,sys.argv[1:])
        

