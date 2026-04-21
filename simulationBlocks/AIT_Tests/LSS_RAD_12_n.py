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
        params['outputDir'] = os.path.join(outputDir,"LSS_RAD_12_n")
        params['small'] = False
        params['doStatic'] = False
        params['doCalib'] = 0
        params['sequence'] = True
        params['startMJD'] =  "2028-01-25 17:00:00"
        params['calibFile'] = None
        params['nCores'] = nCores
        params['testRun'] = False
        
        yamls = ["LSS_RAD_12/LSS_RAD_12_n_nspec.yaml","LSS_RAD_12/LSS_RAD_12_n_n1.yaml","LSS_RAD_12/LSS_RAD_12_n_n2.yaml","LSS_RAD_12/LSS_RAD_12_n_n3.yaml","LSS_RAD_12/LSS_RAD_12_n_pah86.yaml","LSS_RAD_12/LSS_RAD_12_n_pah86_ref.yaml","LSS_RAD_12/LSS_RAD_12_n_pah1125.yaml","LSS_RAD_12/LSS_RAD_12_n_pah1125_ref.yaml","LSS_RAD_12/LSS_RAD_12_n_neii.yaml","LSS_RAD_12/LSS_RAD_12_n_neii_ref.yaml","LSS_RAD_12/LSS_RAD_12_n_siv.yaml","LSS_RAD_12/LSS_RAD_12_n_siv_ref.yaml"]
        
        yamlFiles = []
        for y in yamls:
            yamlFiles.append(os.path.join(yamlDir,y))
        
        rs.runSimulationBlock(yamlFiles,params,sys.argv[1:])
        

