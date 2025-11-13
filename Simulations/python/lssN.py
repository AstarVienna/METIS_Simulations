#!/usr/bin/env python
"""
An example of running an observation block
"""

import runSimulationBlock as rsb


if __name__ == "__main__":
    params = dict(
        outputDir="output/lssN",
        small=False,
        doStatic=True,
        doCalib=2,
        sequence=True,
        startMJD="2027-01-25 00:00:00",
        calibFile=None,
        nCores=8,
        testRun=False,
    )

    yamlFiles = [
        "YAML/scienceLSSN.yaml",
        "YAML/stdLSSN.yaml",
        "YAML/detlinN.yaml",
        "YAML/distortionN.yaml",
        "YAML/rsrfLSSN.yaml",
        "YAML/rsrfPinhLSSN.yaml",
        "YAML/wavecalLSSN.yaml"
    ]

    rsb.runSimulationBlock(yamlFiles, params)

