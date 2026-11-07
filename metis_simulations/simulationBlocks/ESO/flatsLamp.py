#!/usr/bin/env python

from metis_simulations import runSimulationBlock as rs
import os
import sys

yamlDir = os.environ['MSIM_YAML_DIR']
nCores = os.environ['MSIM_NCORES']
outputDir = os.environ['MSIM_OUTDIR']

dirStruct = ["ESO","Calib","Flats","Lamp","Set1"]

if __name__ == "__main__":
    params = {}
    params['outputDir'] = os.path.join(outputDir,*dirStruct)
    params['subDir'] = os.path.join(*dirStruct)
    params['doStatic'] = False
    params['doCalib'] = 0
    params['startMJD'] =  "2027-02-02 13:00:00"
    params['nCores'] = nCores

    yamls = ["flatLampLM.yaml","flatLampN.yaml"]

    yamlFiles = []
    for y in yamls:
        yamlFiles.append(os.path.join(yamlDir,y))
                     
    rs.runSimulationBlock(yamlFiles,params,sys.argv[1:])

