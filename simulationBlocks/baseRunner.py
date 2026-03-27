#!/usr/bin/env python
"""
An example of running an observation block
"""

from Simulations import runSimulationBlock as rs
import os

yamlDir = os.environ['MSIM_YAML_DIR']
nCores = os.environ['MSIM_NCORES']

if __name__ == '__main__':    


    parser = argparse.ArgumentParser()

    parser.add_argument('--nCores', type=str,
                    help='number of cores')
    parser.add_argument('--testRun', type=boolean,
                    help='test')

    
	params = {}
	params['outputDir'] = ""
	params['small'] = False
	params['doStatic'] = True
	params['doCalib'] = 3
	params['sequence'] = True
	params['startMJD'] =  ""
	params['calibFile'] = None
	params['nCores'] = nCores
	params['testRun'] = False

        yamls = ["chophomeLM.yaml","pupilLM.yaml","pupilN.yaml","slitlossLSSLM.yaml","slitlossLSSN.yaml"]

        yamls = ["scienceLM.yaml","stdLM.yaml","distortionLM.yaml","detlinLM.yaml"]
        yamls = ["scienceN.yaml","stdN.yaml","distortionN.yaml","detlinN.yaml"]

        yamls = ["scienceLSSLM.yaml","stdLSSLM.yaml","detlinLM.yaml","distortionLM.yaml","rsrfLSSLM.yaml","rsrfPinhLSSLM.yaml","wavecalLSSLM.yaml","slitlossLSSLM.yaml"]

    yamls = ["wavecalIFU.yaml","scienceIFU.yaml","stdIFU.yaml","detlinIFU.yaml","distortionIFU.yaml","rsrfIFU.yaml","rsrfPinhIFU.yaml"]

        yamls = ["offAxisLM.yaml","hciAppLM.yaml","distortionLM.yaml","detlinLM.yaml"]
	yamls = ["offAxisLM.yaml","hciRavcIfu.yaml","distortionIFU.yaml","detlinIFU.yaml","distortionIFU.yaml","rsrfIFU.yaml","rsrfPinhIFU.yaml","wavecalIFU.yaml"]
	yamls = ["offAxisLM.yaml","hciRavcLM.yaml","distortionLM.yaml","detlinLM.yaml","stdLM.yaml"]

        yamlFiles = []
        for y in yamls:
            yamlFiles.append(os.path.join(yamlDir,y))
	
	rs.runSimulationBlock(yamls,params,argv[1:])

        

