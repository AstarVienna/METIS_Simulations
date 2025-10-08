#!/usr/bin/env python
"""
An example of running an observation block
"""

import runSimulationBlock as rs
if __name__ == '__main__':    

	params = {}
	params['outputDir'] = "outputSmall/imgLM"
	params['small'] = True
	params['doStatic'] = True
	params['doCalib'] = 2
	params['sequence'] = True
	params['startMJD'] =  "2027-01-25 00:00:00"
	params['calibFile'] = None
	params['nCores'] = 8
	params['testRun'] = False
	
	yamlFiles = ["YAML/scienceLM.yaml","YAML/stdLM.yaml","YAML/distortionLM.yaml","YAML/detlinLM.yaml"]
	
	rs.runSimulationBlock(yamlFiles,params)

        
