#!/usr/bin/env python
""" 
Script for generating prototypes of internal use structures for external
calibration files. 

The exact format of external calibration files is still somewhat uncertain 
(FITS files, binary files, databases, text files, etc.). For pipeline
development, we will define a set of internal formats that can be 
produced from whatever form is provided, but will remain consistent
for pipeline development. 

This is a first draft of FITS file formats for the external calibration
files defined in the DRLD, setting up the format (e.g. Table, image) and a
first draft of the necessary columns, image data etc. 

At the moment, the contents are mostly empty/nonsensical; the goal
is to provide a set of files that can be found by pyedps and used
in the pipeline skeleton. The PRO.CATG values have been set for
all files, and for the most part reasonable units have been attempted. 
All files follow the primary header / extension format. 
"""


from astropy.io import fits
from glob import glob
from astropy.table import Table
import numpy as np
import argparse

def generateStaticCalibs(outputDir):


    """

    Generate a set of static calibration FITS files for internal pipeline use. 

    At the moment this is a very basic script. Eventually, the FITS files will be
    generated (once, or on the fly as appropriate) by dedicated recipes, but 
    protoyping the format is a necessary first step.
    """
    
    #################### REF_STD_CAT ###################

    # Generate a FITS file for a calibration spectrum. FITS file contains
    # a primary extension and a secondary table extension with the wavelength
    # and flux values. There is one file per calibration source

    starName = "star1"
    
    ld = fits.Column(name='wavelength', array=np.arange(0,100), format='E')
    star1 = fits.Column(name='flux', array=np.ones(100), format='E')

    hdu = fits.BinTableHDU.from_columns([ld, star1])
    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['INSTRUME'] = "METIS"
    primaryhdu.header['OBJECT'] = "star1"
    primaryhdu.header['RA'] = 0
    primaryhdu.header['DEC'] = 0
    hdu.header['TUNIT1'] = 'm'
    hdu.header['TUNIT2'] = "W m-2 Hz-1"
    hdu.header['TTYPE1'] = "wavelength"
    hdu.header['TTYPE2'] = "flux"
    primaryhdu.header['HIERARCH ESO PRO CATG'] = "REF_STD_CAT"


    hdul = fits.HDUList([primaryhdu, hdu])
    hdul.writeto(f"{outputDir}/REF_STD_CAT_{starName}.fits",overwrite=True)

    #################### FLUXSTD_CATALOG ###################

    # Generates a FITS file with an extension that contains a list of sources plus fluxes
    # in multiple METIS filters. There is one file for multiple stars. 
    
    sources = fits.Column(name='source', array=np.array(['star1','star2','star3']), format='A20')
    lp = fits.Column(name='Lp', array=np.ones(3), format='E')
    mp = fits.Column(name='Lp', array=np.ones(3), format='E')
    n1 = fits.Column(name='Lp', array=np.ones(3), format='E')
    n2 = fits.Column(name='Lp', array=np.ones(3), format='E')

    hdu = fits.BinTableHDU.from_columns([ld, star1])
    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['HIERARCH ESO PRO CATG'] = "FLUXSTD_CATALOG"
    primaryhdu.header['INSTRUME'] = "METIS"

    hdu.header['TUNIT2'] = ""
    hdu.header['TTYPE2'] = "source name"
    hdu.header['TUNIT2'] = "Jy"
    hdu.header['TTYPE2'] = "flux"
    hdu.header['TUNIT3'] = "Jy"
    hdu.header['TTYPE3'] = "flux"
    hdu.header['TUNIT4'] = "Jy"
    hdu.header['TTYPE4'] = "flux"

    hdul = fits.HDUList([primaryhdu, hdu])
    hdul.writeto(f"{outputDir}/FLUXSTD_CATALOG.fits",overwrite=True)
    

    #################### LM_SYNTH_TRANS ###################

    # Creates a synthetic transmission calibration file for LM, consisting of an
    # extension table with wavelength and transmission fraction. 
    
    ld = fits.Column(name='wavelength', array=np.arange(0,100), format='E')
    trans = fits.Column(name='transmission', array=np.ones(100), format='E')
    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['HIERARCH ESO PRO CATG'] = "LM_SYNTH_TRANS"
    primaryhdu.header['INSTRUME'] = "METIS"

    hdu = fits.BinTableHDU.from_columns([ld, trans])
    hdu.header['TUNIT1'] = 'm'
    hdu.header['TUNIT2'] = ""
    hdu.header['TTYPE1'] = "wavelength"
    hdu.header['TTYPE2'] = "fraction"

    
    hdul = fits.HDUList([primaryhdu, hdu])
    hdul.writeto(f"{outputDir}/LM_SYNTH_TRANS.fits",overwrite=True)

    #################### N_SYNTH_TRANS ###################

    # Creates a synthetic transmission calibration file for N, consisting of an
    # extension table with wavelength and transmission fraction. 

    ld = fits.Column(name='wavelength', array=np.arange(0,100), format='E')
    trans = fits.Column(name='transmission', array=np.ones(100), format='E')
    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['HIERARCH ESO PRO CATG'] = " N_SYNTH_TRANS"
    primaryhdu.header['INSTRUME'] = "METIS"

    hdu = fits.BinTableHDU.from_columns([ld, trans])
    hdu.header['TUNIT1'] = 'm'
    hdu.header['TUNIT2'] = "W m-2 Hz-1"
    hdu.header['TTYPE1'] = "wavelength"
    hdu.header['TTYPE2'] = "fraction"

    
    hdul = fits.HDUList([primaryhdu, hdu])
    hdul.writeto(f"{outputDir}/N_SYNTH_TRANS.fits",overwrite=True)
    
    #################### AO_PSF_MODEL ###################

    # creates a fits file with an image extension containing an AO PSF model
    
    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['HIERARCH ESO PRO CATG'] = "AO_PSF_MODEL"
    primaryhdu.header['INSTRUME'] = "METIS"

    data = np.zeros((30,30))
    hdu = fits.ImageHDU(data, name="AO_PSF_MODEL")
    hdu.header['CUNIT']='arcsec'
    hdu.header['CUNIT']='arcsec'
    hdu.header['CRVAL']=0
    hdu.header['CRVAL']=0
    hdu.header['CDELT']=0.00547
    hdu.header['CDELT']=0.00547
    hdu.header['CRPIX']=14.5
    hdu.header['CRPIX']=14.5

    hdul = fits.HDUList([primaryhdu,hdu])
    hdul.writeto(f"{outputDir}/AO_PSF_MODEL.fits",overwrite=True)


    #################### ATM_LINE_CAT ###################

    # creates a catalogue of atmostpheric lines and their parameters. First
    # approximation of columns taken from HITRANS website. 
    
    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['HIERARCH ESO PRO CATG'] = "ATM_LINE_CAT"
    primaryhdu.header['INSTRUME'] = "METIS"

    c1 = fits.Column(name='name', array=np.array(["mol1","mol2"]), format='A10')
    c2 = fits.Column(name='molec_id', array=np.array([]), format='i2')
    c3 = fits.Column(name='local_iso_id', array=np.array([]), format='i1')
    c4 = fits.Column(name='nu', array=np.array([]), format='e')
    c5 = fits.Column(name='sw', array=np.array([]), format='e')
    c6 = fits.Column(name='a', array=np.array([]), format='e')
    c7 = fits.Column(name='gamma_air', array=np.array([]), format='e')
    c8 = fits.Column(name='gamma_self', array=np.array([]), format='e')
    c9 = fits.Column(name='elower', array=np.array([]), format='e')
    c10 = fits.Column(name='n_air', array=np.array([]), format='e')
    c11 = fits.Column(name='delta_air', array=np.array([]), format='e')
    c12 = fits.Column(name='gp', array=np.array([]), format='e')
    c13 = fits.Column(name='gpp', array=np.array([]), format='e')

    hdu = fits.BinTableHDU.from_columns([c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13])

    tunits = ["","","","","cm-1","cm-1/(molec cm-2)","s-1","cm-1 atm-2","cm-1 atm-2","cm-1","","cm-1 atm-2","",""]
    for ii,tt in enumerate(tunits):
        hdu.header[f'TUNIT{ii+1}']=tt

    hdul = fits.HDUList([primaryhdu,hdu])
    hdul.writeto(f"{outputDir}/ATM_LINE_CAT.fits",overwrite=True)



    #################### ATM_PROFILE ###################

    # creates a FITS table extension with atmospheric line profiles. Data contents
    # are empty, but columns names and unites are taken from
    # https://eodg.atm.ox.ac.uk/RFM/atm/equ.atm as referenced in the DRLD
    
    cList = []
    cList.append(fits.Column(name='hgt', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='pre', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='tem', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='n2', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='o2', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='co2', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='o3', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='h2o', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='ch4', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='n2o', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='hno3', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='co', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='no2', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='n2o5', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='clo', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='hocl', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='clono2', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='no', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='hno4', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='hcn', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='nh3', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='f11', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='f12', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='f14', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='f22', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='ccl4', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='cof2', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='h2o2', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='c2h2', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='c2h6', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='ocs', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='so2', array=np.array(np.zeros((121))), format='e'))
    cList.append(fits.Column(name='sf6', array=np.array(np.zeros((121))), format='e'))

    hdu = fits.BinTableHDU.from_columns(cList)
    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['HIERARCH ESO PRO CATG'] = "ATM_PROFILE"

    hdu.header[f'TUNIT1']="km"
    hdu.header[f'TUNIT2']="mb"
    hdu.header[f'TUNIT3']="K"

    for i in range(len(cList)-3):
        hdu.header[f'TUNIT{i+4}']="ppmv"

    hdul = fits.HDUList([primaryhdu,hdu])
    hdul.writeto(f"{outputDir}/ATM_PROFILE.fits",overwrite=True)

    
    #################### LM_LSS_DIST_SOL ###################

    # creates a FITS file with an extension holding the functional parameters for the
    # distortion correction
    
    # at the moment the functional form of the distortion correction is uncertain. For
    # prototyping purposes the functional form is set to an 2nd order polynomial in x and y. 

    xOrder =   [0, 1, 2, 0, 1, 2, 0, 1, 2]
    yOrder =   [0, 0, 0, 1, 1, 1, 2, 2, 2]
    coeff =   [0, 1, 0, 1, 0, 0, 0, 0, 0]

    
    c1 = fits.Column(name='x_order', array=np.array(xOrder), format='i')
    c2 = fits.Column(name='y_order', array=np.array(yOrder), format='i')
    c3 = fits.Column(name='coeff', array=np.array(coeff), format='e')

    hdu = fits.BinTableHDU.from_columns([c1,c2,c3])

    hdu.header[f'TUNIT1']=""
    hdu.header[f'TUNIT2']=""
    hdu.header[f'TUNIT3']=""

    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['HIERARCH ESO PRO CATG'] = "LM_LSS_DIST_SOL"
    primaryhdu.header['INSTRUME'] = "METIS"
    hdul = fits.HDUList([primaryhdu,hdu])
    hdul.writeto(f"{outputDir}/LM_LSS_DIST_SOL.fits",overwrite=True)
    
    #################### N_LSS_DIST_SOL ###################

    # same as LM_LSS_DIST_SOL but for N band
    
    # creates a FITS file with an extension holding the functional parameters for the
    # distortion correction
    
    # at the moment the functional form of the distortion correction is uncertain. For
    # prototyping purposes the functional form is set to an 2nd order polynomial in x and y. 

    xOrder =   [0, 1, 2, 0, 1, 2, 0, 1, 2]
    yOrder =   [0, 0, 0, 1, 1, 1, 2, 2, 2]
    coeff =   [0, 1, 0, 1, 0, 0, 0, 0, 0]

    
    c1 = fits.Column(name='x_order', array=np.array(xOrder), format='i')
    c2 = fits.Column(name='y_order', array=np.array(yOrder), format='i')
    c3 = fits.Column(name='coeff', array=np.array(coeff), format='e')

    hdu = fits.BinTableHDU.from_columns([c1,c2,c3])

    hdu.header[f'TUNIT1']=""
    hdu.header[f'TUNIT2']=""
    hdu.header[f'TUNIT3']=""

    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['HIERARCH ESO PRO CATG'] = "N_LSS_DIST_SOL"
    primaryhdu.header['INSTRUME'] = "METIS"
    hdul = fits.HDUList([primaryhdu,hdu])
    hdul.writeto(f"{outputDir}/N_LSS_DIST_SOL.fits",overwrite=True)


    #################### LM_LSS_WAVE_GUESS ###################

    # creates a FITS file with a table extension giving the first guess
    # of the LM-band wavelength solution. 

    # at the moment the functional form of the distortion correction is uncertain. For
    # prototyping purposes the functional form is set to an 2nd order polynomial in x and y. 

    xOrder =   [0, 1, 2, 0, 1, 2, 0, 1, 2]
    yOrder =   [0, 0, 0, 1, 1, 1, 2, 2, 2]
    coeff =   [0, 1, 0, 1, 0, 0, 0, 0, 0]

    c1 = fits.Column(name='x_order', array=np.array(xOrder), format='i')
    c2 = fits.Column(name='y_order', array=np.array(yOrder), format='i')
    c3 = fits.Column(name='coeff', array=np.array(coeff), format='e')

    hdu = fits.BinTableHDU.from_columns([c1,c2,c3])

    hdu.header[f'TUNIT1']=""
    hdu.header[f'TUNIT2']=""
    hdu.header[f'TUNIT3']=""

    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['HIERARCH ESO PRO CATG'] = "N_LSS_WAVE_GUESS"
    primaryhdu.header['INSTRUME'] = "METIS"
    hdul = fits.HDUList([primaryhdu,hdu])
    hdul.writeto(f"{outputDir}/N_LSS_WAVE_GUESS.fits",overwrite=True)

    #################### N_LSS_WAVE_GUESS ###################

    # as for LM_LSS_WAVE_GUESS

    xOrder =   [0, 1, 2, 0, 1, 2, 0, 1, 2]
    yOrder =   [0, 0, 0, 1, 1, 1, 2, 2, 2]
    coeff =   [0, 1, 0, 1, 0, 0, 0, 0, 0]

    c1 = fits.Column(name='x_order', array=np.array(xOrder), format='i')
    c2 = fits.Column(name='y_order', array=np.array(yOrder), format='i')
    c3 = fits.Column(name='coeff', array=np.array(coeff), format='e')

    hdu = fits.BinTableHDU.from_columns([c1,c2,c3])

    hdu.header[f'TUNIT1']=""
    hdu.header[f'TUNIT2']=""
    hdu.header[f'TUNIT3']=""

    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['HIERARCH ESO PRO CATG'] = "LM_LSS_WAVE_GUESS"
    primaryhdu.header['INSTRUME'] = "METIS"
    hdul = fits.HDUList([primaryhdu,hdu])
    hdul.writeto(f"{outputDir}/LM_LSS_WAVE_GUESS.fits",overwrite=True)
    
    #################### LSF_KERNEL ###################

    # creates a FITS file with an extension with the kernel for the line spread function,
    # in the form of a table of pixels vs intensity

    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['HIERARCH ESO PRO CATG'] = "LSF_KERNEL"
    primaryhdu.header['INSTRUME'] = "METIS"
    xPos = np.arange(0,100,0.5)
    yPos = np.arange(0,100,0.5)
    
    c1 = fits.Column(name='pixel', array=xPos, format='e')
    c2 = fits.Column(name='intensity', array=yPos, format='e')

    hdu = fits.BinTableHDU.from_columns([c1,c2])
    hdu.header[f'TTYPE1']="pixels"
    hdu.header[f'TTYPE2']=""

    hdul = fits.HDUList([primaryhdu,hdu])
    hdul.writeto(f"{outputDir}/LSF_KERNEL.fits",overwrite=True)

    
    #################### LASER_TAB ###################

    # FITS file with an extension containing a table of laser frequencies for the WCU 

    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['HIERARCH ESO PRO CATG'] = "LASER_TAB"
    primaryhdu.header['INSTRUME'] = "METIS"
    freq = np.zeros((5))
    
    c1 = fits.Column(name='frequency', array=freq, format='e')

    hdu = fits.BinTableHDU.from_columns([c1])
    hdu.header[f'TTYPE1']="Hz"

    hdul = fits.HDUList([primaryhdu,hdu])
    hdul.writeto(f"{outputDir}/LASER_TAB.fits",overwrite=True)

    
    #################### PINHOLE_TABLE ###################

    # FITS file with an extension containing a table of X,Y positions for the pinhole masks

    primaryhdu = fits.PrimaryHDU()
    primaryhdu.header['HIERARCH ESO PRO CATG'] = "PINHOLE_TABLE"
    primaryhdu.header['INSTRUME'] = "METIS"
    xPos = np.arange(0,100,0.5)
    yPos = np.arange(0,100,0.5)
    
    c1 = fits.Column(name='x_pos', array=xPos, format='e')
    c2 = fits.Column(name='y_pos', array=yPos, format='e')

    hdu = fits.BinTableHDU.from_columns([c1,c2])
    hdu.header[f'TTYPE1']="mm"
    hdu.header[f'TTYPE2']="mm"

    hdul = fits.HDUList([primaryhdu,hdu])
    hdul.writeto(f"{outputDir}/PINHOLE_TABLE.fits",overwrite=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--outDir', type=str,
                    help='output directory')

    args = parser.parse_args()
    if(args.outDir):
        outDir = args.outDir
    else:
        outDir = "output"

    
    generateStaticCalibs(outDir)
