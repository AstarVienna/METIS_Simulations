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
                
        yamls= ["LSS_RAD_12/LSS_RAD_12_lm_lspec.yaml","LSS_RAD_12/LSS_RAD_12_lm_lp.yaml","LSS_RAD_12/LSS_RAD_12_lm_shortl.yaml","LSS_RAD_12/LSS_RAD_12_lm_bralpha.yaml","LSS_RAD_12/LSS_RAD_12_lm_bralpha_ref.yaml","LSS_RAD_12/LSS_RAD_12_lm_pah33.yaml","LSS_RAD_12/LSS_RAD_12_lm_pah33_ref.yaml","LSS_RAD_12/LSS_RAD_12_lm_h2oice.yaml","LSS_RAD_12/LSS_RAD_12_lm_h2oice_ref.yaml","LSS_RAD_12/LSS_RAD_12_lm_ib405.yaml","LSS_RAD_12/LSS_RAD_12_lm_hcilshort.yaml","LSS_RAD_12/LSS_RAD_12_lm_hcillong.yaml","LSS_RAD_12/LSS_RAD_12_lm_co10ice.yaml","LSS_RAD_12/LSS_RAD_12_lm_co_ref.yaml","LSS_RAD_12/LSS_RAD_12_lm_mspec.yaml","LSS_RAD_12/LSS_RAD_12_lm_mp.yaml"]
        yamlFiles = []
        for y in yamls:
            yamlFiles.append(os.path.join(yamlDir,y))
        
        rs.runSimulationBlock(yamlFiles,params,sys.argv[1:])
        


