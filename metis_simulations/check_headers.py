#!/usr/bin/env python
"""Check whether header files of FITS files are correct.

First install the DRLD with
METIS_DRLD> pip install -e .

But that does not always work (TODO: fix), so you can also specify the
Python path:
export PYTHONPATH=/path/to/METIS_DRLD/codes
"""

import sys
from pathlib import Path

from astropy.io import fits

from codes.drld_parser.data_reduction_library_design import METIS_DataReductionLibraryDesign

from compare_yaml_with_drld import HACK_RAWS_THAT_SHOULD_BE_ADDED_TO_THE_DRLD

def checkHeaders(argv):
    if(len(sys.argv) > 1):
       inDir = argv[1]
    else:
       inDir = "output"
    
    PATH_HERE = Path(__file__).parents[1]
    PATH_OUTPUT = PATH_HERE / inDir
    
    print(PATH_OUTPUT)
    
    ks_toplevel_allowed = {"ESO", "WISE"}
    
    fns_fits = PATH_OUTPUT.glob("*.fits")
    
    for fn_fits in fns_fits:
        print(fn_fits)
        hdus = fits.open(fn_fits)
        for hdu in hdus:
            for card in hdu.header.cards:
                k, v, c = card
                ks = k.split()
                # Assert keyword is uppercase.
                assert k.upper() == k, k
                # Assert HIERARCH keywords start with allowed top level key.
                if len(ks) > 1:
                    assert ks[0] in ks_toplevel_allowed, k
                # Assert all subsystems in HIERARCH keyword are max 8 characters.
                assert all(len(ki) <= 8 for ki in ks), k
    
        fn_split = fn_fits.name.split(".")
        catg = fn_split[1] if fn_split[0] == "METIS" else fn_split[0]
        if catg in HACK_RAWS_THAT_SHOULD_BE_ADDED_TO_THE_DRLD:
            continue
        di = METIS_DataReductionLibraryDesign.dataitems[catg]
        if di.dpr_catg:
            assert hdus[0].header["ESO DPR CATG"] == di.dpr_catg
        if di.dpr_type:
            assert hdus[0].header["ESO DPR TYPE"] == di.dpr_type
        if di.dpr_tech:
            assert hdus[0].header["ESO DPR TECH"] == di.dpr_tech

if __name__ == "__main__":
    
    checkHeaders(sys.argv)
