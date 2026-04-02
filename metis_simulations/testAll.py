#!/usr/bin/env python
"""
An example of running an observation block
"""

import runSimulationBlock as rs
if __name__ == '__main__':    

	params = {}
	params['outputDir'] = "outputTest/"
	params['small'] = True
	params['doStatic'] = True
	params['doCalib'] = 1
	params['sequence'] = True
	params['startMJD'] =  "2027-01-25 00:00:00"
	params['calibFile'] = None
	params['nCores'] = 1
	params['testRun'] = False
	
	yamlFiles = ["YAML/testYAML.yaml"]
	
	rs.runSimulationBlock(yamlFiles,params)

        
