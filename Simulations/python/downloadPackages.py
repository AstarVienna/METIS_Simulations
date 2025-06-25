#!/usr/bin/env python

import scopesim as sim
from pathlib import Path

pkgs = ["METIS", "Armazones", "ELT"]

for pkg in pkgs:
    sim.download_packages(pkg,release="stable", save_dir=str(Path.home()) + '/.inst_pkgs' )