#!/usr/bin/env python
"""
An example of running an observation block
"""


import scopesimWrapper as rr
import runSimulationBlock as rs

if __name__ == '__main__':    

	params = {}
	params['outputDir'] = "output/imgN"
	params['small'] = False
	params['doStatic'] = True
	params['doCalib'] = 2
	params['sequence'] = True
	params['startMJD'] =  "2027-01-26 00:00:00"
	params['calibFile'] = None
	params['nCores'] = 8
	params['testRun'] = False
	
	yamlFiles = ["YAML/scienceN.yaml","YAML/stdN.yaml","YAML/distortionN.yaml","YAML/detlinN.yaml","YAML/persistN.yaml"]

	rs.runSimulationBlock(yamlFiles,params)

        
