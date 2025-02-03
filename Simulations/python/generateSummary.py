#!/usr/bin/env python
from astropy.io import fits
import numpy as np
import pandas as pd
from importlib import reload
import glob
import os
import argparse

def generateSummary(inDir,outFileName):

    # get the fits files in the directory
    fNames = glob.glob(os.path.join(inDir,"METIS*.fits"))

    # sort for tidier output
    fNames.sort()
    outFile = open(outFileName,"w")

    #header line
    
    line = "File\tDIT\tNDIT\tTech\tCATG\tTYPE\tINS.MODE\tDRS.SLIT\tDRS.FILTER\tDRS.IFU\tDRS.MASK\tINS."
    print(line,file=outFile)

    
    for fName in fNames:
        print(fName)
        hdul = fits.open(fName)

        # pull out the values
        
        dit = hdul[0].header['HIERARCH ESO DET DIT']
        ndit = hdul[0].header['HIERARCH ESO DET NDIT']
        
        tech = hdul[0].header['HIERARCH ESO DPR TECH']
        catg = hdul[0].header['HIERARCH ESO DPR CATG']
        tipe = hdul[0].header['HIERARCH ESO DPR TYPE']

        # pulling as wildcards reuturns a list of the variable names + values, to handle different cases

        slit = hdul[0].header['*DRS SLIT*']
        filt = hdul[0].header['*DRS FILTER*']
        ifu = hdul[0].header['*DRS IFU*']
        mask = hdul[0].header['*DRS MASK*']
        
        ins = hdul[0].header['*INS OPTI*']
        mode = hdul[0].header['HIERARCH ESO INS MODE']

        #get the fine name w/o pasth
        
        fShort = os.path.basename(fName)

        # assemble the output line, tab separated
        
        line = f'{fShort}\t{dit}\t{ndit}\t{tech}\t{catg}\t{tipe}\t{mode}\t'

        # single value, or empty
        for elem in slit:
            line = f'{line}{hdul[0].header[elem]}'
        line=line+"\t"
        for elem in filt:
            line = f'{line}{hdul[0].header[elem]}'
        line=line+"\t"
        for elem in ifu:
            line = f'{line}{hdul[0].header[elem]}'
        line=line+"\t"
        for elem in mask:
            print(ins)

            line = f'{line}{hdul[0].header[elem]}'
        line=line+"\t"
        
        # multiple values
        nIns = 0
        for elem in ins:
            line = f'{line}{elem}={hdul[0].header[elem]},'
            nIns += 1

        if(nIns > 0):
            # remove the trailing comma
            line=f'{line[:-1]}\t'

        # dump line to file 
        print(line,file=outFile)
        hdul.close()
    outFile.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--outFile', type=str,
                    help='output file')
    parser.add_argument('--inDir', type=str, 
                    help='directory containing input files')

    args = parser.parse_args()
    if(args.outFile):
        outFile = args.outFile
    else:
        outFile = "summary.csv"
    if(args.inDir):
        inDir = args.inDir
    else:
        inDir = "output"

    generateSummary(inDir,outFile)
 

