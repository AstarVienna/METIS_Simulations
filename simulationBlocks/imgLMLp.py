#!/usr/bin/env python
"""
An example of running an observation block
"""

import runSimulationBlock as rs
if __name__ == '__main__':    

	params = {}
	params['outputDir'] = "output/imgLM"
	params['small'] = False
	params['doStatic'] = True
	params['doCalib'] = 3
	params['sequence'] = True
	params['startMJD'] =  "2027-01-25 00:00:00"
	params['calibFile'] = None
	params['nCores'] = 8
	params['testRun'] = False
	
	yamls = ["YAML/scienceLMLp.yaml","YAML/stdLMLp.yaml"]
	
        yamlFiles = []
        for y in yamls:
            yamlFiles.append(os.path.join(yamlDir,y))
	
	rs.runSimulationBlock(yamls,params,argv[1:])

        
