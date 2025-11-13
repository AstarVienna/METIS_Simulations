#!/usr/bin/env python
from astropy.io import fits
import numpy as np
import pandas as pd
from importlib import reload
import glob
import os
import argparse

def generateSummary(fnames,outFileName):

    # get the fits files in the directory
    outFile = open(outFileName,"w")

    #header line

    line = "\Block\tFile\tDIT\tNDIT\tTech\tCATG\tTYPE\tINS.MODE\tTPL.NAME\tTPL.START\tTPL.EXPNO\tDRS.SLIT\tDRS.FILTER\tDRS.IFU\tDRS.MASK."
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

        tpl = hdul[0].header['HIERARCH ESO TPL NAME']
        tplStart = hdul[0].header['HIERARCH ESO TPL START']
        tplExpno = hdul[0].header['HIERARCH ESO TPL EXPNO']

        # pulling as wildcards reuturns a list of the variable names + values, to handle different cases

        slit = hdul[0].header['*DRS SLIT*']
        filt = hdul[0].header['*DRS FILTER*']
        ifu = hdul[0].header['*DRS IFU*']
        mask = hdul[0].header['*DRS MASK*']

        #ins = hdul[0].header['*INS OPTI*']
        mode = hdul[0].header['HIERARCH ESO INS MODE']

        #get the fine name w/o pasth

        fShort = fName.split("/")[1]
        block = fName.split("/")[0]


        # assemble the output line, tab separated

        line = f'{block}\t{fShort}\t{dit}\t{ndit}\t{tech}\t{catg}\t{tipe}\t{mode}\t{tpl}\t{tplStart}\t{tplExpno}'

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
        #for elem in mask:
        #    print(ins)

        #    line = f'{line}{hdul[0].header[elem]}'
        line=line+"\t"

        ## multiple values
        #nIns = 0
        #for elem in ins:
        #    line = f'{line}{elem}={hdul[0].header[elem]},'
        #    nIns += 1
        #
        #if(nIns > 0):
        #    # remove the trailing comma
        #    line=f'{line[:-1]}\t'

        # dump line to file
        print(line,file=outFile)
        hdul.close()
    outFile.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--outFile', type=str,
                    help='output file')
    parser.add_argument('--inDir', type=str,
                    help='List of input directories, comma separated')

    args = parser.parse_args()
    if(args.outFile):
        outFile = args.outFile
    else:
        outFile = "summary.csv"
    if(args.inDir):
        inDir = args.inDir.split(",")
    else:
        inDir = "output"


    fNames = []
    for dirName in inDir:
        temp = glob.glob(os.path.join(dirName,"METIS*.fits"))
        fNames = fNames + temp

    # sort for tidier output
    fNames.sort()

    generateSummary(fNames,outFile)



