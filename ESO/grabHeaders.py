from astropy.io import fits
import numpy as np
import pandas as pd
from importlib import reload
import glob
import os

fNames = glob.glob("/Users/karr/software/METIS_Simulations/ESO/output/METIS*.fits")
fNames.sort()

outFile = open("summary.csv","w")

line = "File\tDIT\tNDIT\tTech\tCATG\tTYPE\tDRS.SLIT\tDRS.FILTER\tDRS.IFU\tDRS.MASK\tINS."
print(line,file=outFile)

for fName in fNames:
    print(fName)
    hdul = fits.open(fName)
    dit = hdul[0].header['HIERARCH ESO DET DIT']
    ndit = hdul[0].header['HIERARCH ESO DET NDIT']
    
    tech = hdul[0].header['HIERARCH ESO DPR TECH']
    catg = hdul[0].header['HIERARCH ESO DPR CATG']
    tipe = hdul[0].header['HIERARCH ESO DPR TYPE']

    slit = hdul[0].header['*DRS SLIT*']
    filt = hdul[0].header['*DRS FILTER*']
    ifu = hdul[0].header['*DRS IFU*']
    mask = hdul[0].header['*DRS MASK*']

    ins = hdul[0].header['*INS OPTI*']
    
    fShort = os.path.basename(fName)
    line = ""
    line = f'{fShort}\t{dit}\t{ndit}\t{tech}\t{catg}\t{tipe}\t'

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
        line = f'{line}{hdul[0].header[elem]}'
    line=line+"\t"


        
    for elem in ins:
        line = f'{line}{elem}={hdul[0].header[elem]},'
    line=f'{line[:-1]}\t'

    print(line,file=outFile)
    hdul.close()
outFile.close()
