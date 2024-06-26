#!/usr/bin/env python
"""
Somewhat klugy routine to automatically add ESO/EDPS framework 
keywords not clurrently included in ScopeSim
"""


from astropy.io import fits
import numpy as np
from importlib import reload
import glob
import argparse
import os
import astropy.time


def updateHeaders(inDir,outDir):

    """
    add keywords to a seris of files
    
    DPR .TECH, .FILTER and .TYPE are set by ScopeSim, DRS.FILTER .NDFILTER, 
    and DET.DIT and .NDIT are set in ScopeSim

    We use the TECH to get INS.MODE
    Sets the DRS.SLIT to the default value for now (will fix later)
    Sets INS.OPTI*.NAME to the filter, slit as indicated by the TECH, FILTER and SLIT keyword

    For HCI / Coronagraph modes, we set the TECH keyword to a non valid value in Scopesim, 
    and use that to set the DRS.MASK, correct DPR.TECH, and INS.OPTI*.NAME values. This is kludgy,
    and will be fixed later. 

    We check the TYPE keyword for LASER Sources. 

    Files are written to the given directory, AND WILL OVERWRITE EXISTING FILES
    """
    

    # find all FITS files in input Dir
    
    fNames = glob.glob(os.path.join(inDir,"*.fits"))

    # sort for tidier output
    fNames.sort()

    for fName in fNames:
        print(f'Processing {fName}')
        # open the file
        hdul = fits.open(fName)
        if type(hdul[0].header['MJD-OBS']) == str:
            mjdobs = hdul[0].header['MJD-OBS']
            hdul[0].header['MJD-OBS'] = astropy.time.Time(mjdobs,format="isot").mjd
        # get the tech and filter keywords
        try:
            tech = hdul[0].header['HIERARCH ESO DPR TECH']
            filt = hdul[0].header['HIERARCH ESO DRS FILTER']
            print(fName,tech)
        except:
            printf(f'Header keywords are not existed.')
            exit(0)
            #spectra
        if(tech == "LSS,LM"):
            hdul[0].header['HIERARCH ESO INS MODE'] = "SPEC_LM"
            hdul[0].header['HIERARCH ESO INS OPTI9 NAME'] = filt
            hdul[0].header['HIERARCH ESO INS DRS SLIT'] = "C-38_1"
        if(tech == "LSS,N"):
            hdul[0].header['HIERARCH ESO INS MODE'] = "SPEC_N_LOW"
            hdul[0].header['HIERARCH ESO INS OPTI12 NAME'] = filt
            hdul[0].header['HIERARCH ESO INS DRS SLIT'] = "C-38_1"
        
        #IMAGING
        if(tech == "IMAGE,LM"):
            hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_LM"
            hdul[0].header['HIERARCH ESO INS OPTI10 NAME'] = filt
        if(tech == "IMAGE,N"):
            hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_N"
            hdul[0].header['HIERARCH ESO INS OPTI13 NAME'] = filt
        
        #IFU
        if(tech == "LMS"):
            hdul[0].header['HIERARCH ESO INS MODE'] = "IFU_nominal"
            hdul[0].header['HIERARCH ESO INS OPTI6 NAME'] = filt
            hdul[0].header['HIERARCH ESO DRS IFU'] = filt
            hdul[0].header['HIERARCH ESO DPR TECH'] = "IFU"
            
        #HCI
        if(tech == "RAVC,LM"):
            hdul[0].header['HIERARCH ESO INS OPTI10 NAME'] = filt
            hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_LM_RAVC"
            hdul[0].header['HIERARCH ESO DRS MASK'] = "VPM-L,RAP-LM,RLS-LMS"
            hdul[0].header['HIERARCH ESO INS OPTI1 NAME'] = "RAP-LM"
            hdul[0].header['HIERARCH ESO INS OPTI3 NAME'] = "VPM-L"
            hdul[0].header['HIERARCH ESO INS OPTI5 NAME'] = "RLS-LMS"
            hdul[0].header['HIERARCH ESO DPR TECH'] = "IMAGE,LM"
        
        if(tech == "APP,LM"):
            hdul[0].header['HIERARCH ESO INS OPTI10 NAME'] = filt
            hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_LM_APP"
            hdul[0].header['HIERARCH ESO DPR TECH'] = "IMAGE,LM"
            hdul[0].header['HIERARCH ESO INS OPTI1 NAME'] = "RAP-LM"
            hdul[0].header['HIERARCH ESO INS OPTI3 NAME'] = "VPM-L"
            hdul[0].header['HIERARCH ESO INS OPTI5 NAME'] = "APP-LMS"
            hdul[0].header['HIERARCH ESO DRS MASK'] = "VPM-L,RAP-LM,APP-LMS"
        
        if(tech == "RAVC,IFU"):
            hdul[0].header['HIERARCH ESO INS OPTI6 NAME'] = filt
            hdul[0].header['HIERARCH ESO INS MODE'] = "IFU_nominal_RAVC"
            hdul[0].header['HIERARCH ESO DRS IFU'] = filt
            hdul[0].header['HIERARCH ESO DPR TECH'] = "IFU"
            hdul[0].header['HIERARCH ESO INS OPTI1 NAME'] = "RAP-LM"
            hdul[0].header['HIERARCH ESO INS OPTI3 NAME'] = "VPM-L"
            hdul[0].header['HIERARCH ESO INS OPTI5 NAME'] = "RLS-LMS"
            hdul[0].header['HIERARCH ESO DRS MASK'] = "VPM-L,RAP-LM,RLS-LMS"

        #OTHER
        if(hdul[0].header['HIERARCH ESO DPR TYPE'] == "WAVE"):   
            hdul[0].header['HIERARCH ESO SEQ WCU LASER1 NAME'] = "LASER1"

        #OTHER
        if(tech == "PUP,M"):
            hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_LM"
            hdul[0].header['HIERARCH ESO INS OPTI15 NAME'] = "PUPIL1"
        if(tech == "PUP,N"):
            hdul[0].header['HIERARCH ESO INS MODE'] = "IMG_N"
            hdul[0].header['HIERARCH ESO INS OPTI15 NAME'] = "PUPIL2"

        
        # get the filename from the path
        fShort = os.path.basename(fName)
        
        hdul.writeto(os.path.join(outDir,fShort),overwrite=True)
        hdul.close()
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--outDir', type=str,
                    help='output directory')
    parser.add_argument('--inDir', type=str, 
                    help='directory containing input files')

    args = parser.parse_args()
    if(args.outDir):
        outDir = args.outDir
    else:
        outDir = "output"
    if(args.inDir):
        inDir = args.inDir
    else:
        inDir = "output"

    print(inDir,outDir)
    updateHeaders(inDir,outDir)
 

