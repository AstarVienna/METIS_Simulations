#!/usr/bin/env python3

"""
Script to generate SOF files from the templates, to add 
the real file names.

Note that as of Nov 15 2024, the Coronagraphic recipes have the same 
format for input data as standard LM/N/IFU science imaging routines.
Therefore the LM/N/IFU SCI imaging routines need a quick fix to 
remove those data. 

The routine reads in the SOF templates from sofTemplates, and creates
an identical list of files in sofFiles. 

"""

import glob

# read the list of files from the template directory
fList = glob.glob("sofTemplates/*.sof")

# cycle through, read in line by line. If there is a "*" in the filename
# do wildcard pattern matching for the list of files, otherwise just copy

for fNameIn in fList:
    ffIn = open(fNameIn)
    fNameOut = fNameIn.replace("sofTemplates","sofFiles")
    ffOut = open(fNameOut,"w")
    print(fNameOut)
    for line in ffIn:
        aa = line.split()
        if("*" in aa[0]):
            infList = glob.glob(f"output/{aa[0]}")
            
            for f in infList:
                print(aa)
                temp=f.replace("output","$SOF_DATA")
                print(f'{temp} {aa[1]}',file=ffOut)
        else:
            print(f'$SOF_DATA/{line.strip()}',file=ffOut)
    ffOut.close()
    ffIn.close()
                
            
            
    
    
