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

dirStruct = ["ESO","Inst","hciAppLM","Set1"]

if __name__ == '__main__':    

        params = {}
        params['outputDir'] = os.path.join(outputDir,*dirStruct)
        params['subDir'] = os.path.join(*dirStruct)
        params['doStatic'] = False
        params['doCalib'] = 0
        params['startMJD'] =  "2027-01-29 00:00:00"
        params['nCores'] = nCores
        
        yamls = ["offAxisLM.yaml","hciAppLM.yaml"]

        yamlFiles = []
        for y in yamls:
            yamlFiles.append(os.path.join(yamlDir,y))
        
        rs.runSimulationBlock(yamlFiles,params,sys.argv[1:])



        
