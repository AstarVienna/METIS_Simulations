#!/usr/bin/env python

from pathlib import Path

PATH_HERE = Path(__file__).parent
PATH_SOFS = PATH_HERE / "sofFiles"
PATH_FITS = PATH_HERE / "output"

for filename in PATH_SOFS.glob("*.sof"):
    # print(filename)
    lines = open(filename, mode="r", encoding="utf-8").readlines()
    fns_raw = [
        line.split()[0].split("/")[1]
        for line in lines
        if "RAW" in line
    ]
    fns_raw_missing = [
        fn
        for fn in fns_raw
        if not (PATH_FITS / fn).exists()
    ]
    if fns_raw_missing:
        print(filename)
        print(fns_raw_missing)

