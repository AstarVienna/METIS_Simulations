#!/usr/bin/env python
"""
An example of running an observation block
"""

import runSimulationBlock as rs
if __name__ == '__main__':    

	params = {}
	params['outputDir'] = "outputSmall/hciRavcIfu"
	params['small'] = True
	params['doStatic'] = True
	params['doCalib'] = 2
	params['sequence'] = True
	params['startMJD'] =  "2027-01-30 00:00:00"
	params['calibFile'] = None
	params['nCores'] = 8
	params['testRun'] = False
	
	yamlFiles = ["YAML/offAxisLM.yaml","YAML/hciRavcIFU.yaml","YAML/distortionIFU.yaml","YAML/detlinIFU.yaml","YAML/distortionIFU.yaml","YAML/rsrfIFU.yaml","YAML/rsrfPinhIFU.yaml","YAML/wavecalIFU.yaml"]
	
	rs.runSimulationBlock(yamlFiles,params)

        
