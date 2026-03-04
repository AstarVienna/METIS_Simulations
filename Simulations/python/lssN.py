#!/usr/bin/env python
"""
An example of running an observation block
"""

import runSimulationBlock as rsb


if __name__ == "__main__":
    params = {}
    params['outputDir'] = "../AIT_Tests/LSS_RAD_12"
    params['small'] = False
    params['doStatic'] = False
    params['doCalib'] = 2
    params['sequence'] = True
    params['startMJD'] =  "2027-01-28 00:00:00"
    params['calibFile'] = None
    params['nCores'] = 6
    params['testRun'] = False

    yamlFiles = ["../AIT_Tests/LSS_RAD_12/LSS_RAD_12_n_list.yaml"]

    rsb.runSimulationBlock(yamlFiles,params)

