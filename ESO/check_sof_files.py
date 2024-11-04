#!/usr/bin/env python

from pathlib import Path

PATH_HERE = Path(__file__).parent
PATH_SOFS = PATH_HERE / "sofFiles"
PATH_FITS = PATH_HERE / "output"

problems = []

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
        problems.append((filename.name, fns_raw_missing))

if problems:
    print("Some RAW files are missing:")
    for fn_sof, fns_missing in problems:
        print("-", fn_sof)
        for fn in fns_missing:
            print("  -", fn)
    exit(1)
