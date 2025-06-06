
# IMPORTANT NOTICE

<span style="color: red">This repository contains code that is a work in progress.  The current
set of simulations are designed for METIS pipeline development, at
this point including correct FITS headers and file format.  The
resultant files **DO NOT** contain instrumentally or scientifically
accurate data, and under no circumstances should be used to evaluate
potential performance of the METIS instrument.</span>

# METIS Simulations

This respository contains scripts which can be used as a wrapper for ScopeSim to generate a set of simulated METIS data for pipeline development. 

 - [Installing the Code](#installing-the-code)
 - [Simulated Data Summary](#simulated-data-summary)
 - [List of Output Fits Files](#output-fits-files)
 - [Running the Code](#running-the-code)
 - [Custom Simulations](#custom-simulations)


# Installing the Code

First create a clean Python environment with a recent Python version and poetry, for example through conda:
```
> conda create -n metissim python==3.12 poetry
> conda activate metissim
```

The following sequence of commands will
download and install the software with the correct dependencies. 


```
> git clone git@github.com:AstarVienna/METIS_Simulations.git

> cd METIS_Simulations/Simulations
> poetry install
> poetry shell
```


# Running the Code

Before the first time you run the code, execute the script

```
> ./python/downloadPackages.py
```

Which will download the instrument, telescope and site specific data packages. 

To run the default set of FITS files, as described in [Data Product Summary](#data-product-summary), 


```
> /runESO.sh
```

This will run the script, automatically determining the necessary flats and darks and running them at the end of the sequence; the number indicates
how many of each type to generate. The sequence takes the observation time of the first entry in the YAML file and increments from there. 

## Command Line Options

```
--doCalib=n
```
automatically determine and generate the required flats and darks, n is the number of each type to generate. Default is turned off.

```
--sequence=1
--sequence="yyyy-mm-dd hh:mm:ss"
```

automatically generate a time sequence of observations

   - if sequence is not specified, use explicitly given dateObs from the YAML tempates
   - if sequence=1, generate starting either from the dateObs in the first template, or using a default value
   - if sequence="yyyy-mm-dd hh:mm:ss" start the sequence from the given date

```
--outputDir=outDir
```

   set output directory to outDir, default is output/

```
--inputYAML=myfile.yaml
```

   set input YAML file to myfile.yaml, default is YAML/recipes.yaml

```
--small
```

   generate small images with correct headers, useful for skeleton testing. Default is off

```
--testRun
```

   do everything except the actual file generation, useful for checking input YAML templates. Default is off

```
--calibFile=calib.yaml
```

   dump the YAML templates generated for doCalib to a calib.yaml, default is off

```
--fixed
```

   use a fixed random seed for the image generation, for testing and validation purposes, default is off

## Generating a summary

./python/generateSummary.py

generates a CSV file containing a list of files and a summary of the important keywords. Options are

```
--inDir=myDir
```

Read the files from directory myDir, default is output/

```
--outFile=outfile.csv
```

write output to file outfile.csv, default is summary.csv


```
--nCores=n
```

Will run the code in parallel mode, using n cores. The default is 1.


# Simulated Data Summary

Running the versions of the command listed at the top of this document generates a minimal set of input test files for skeleton pipeline development, i.e. one each of any file needed for input to a recipes as specified in Chapter 6 of the DRLD.  Each file has the correct dimensions, plus ESO compliant keywords as required for developing the EDPS skeleton, specifically the matched keywords and derived aliases, as well as the standard FITS keywords provided by ScopeSim. 

## Included Keywords

 - DET.DIT
 - DET.NDIT
 - DPR.CATG
 - DPR.TECH
 - DPR.TYPE
 - INS.MODE
 - INS.OPTI*.NAME (depends on instrument)
 - SEQ.WCU.LASERn

 - DRS.FILTER
 - DRS.SLIT
 - DRS.IFU
 - DRS.MASK
 - DRS.PUPIL

## FITS file contents

All of the FITS files were generated by ScopeSim using the provided
script. In most cases, they contain data which is a first
approximation of real data; further work is needed in many cases to
set DIT/NDIT/Filters for reasonable flux levels, and to refine the
choice of science targets and standard stars for more accurate (and
science-case appropriate) choices. We have generated data and
calibrations for one set of filters for each mode as a base set; this
can easily be extended to multiple sets as needed. One of each type of
image has been generated; this is sufficient for pipeline skeleton development. 

The coronagraph, pupil imaging and chopper home images currently
contain placeholder data as these are not modes sximulated by
ScopeSim; by the next release these will be updated to include input
simulated images.

This release contains placeholder files for the internal pipeline
representation of the of the external calibration files (such as
source catalogues). The EDPS relevant header keywords are set, and
there is a first draft of the internal format.

FITS keywords needed by the recipes themselves (but not by the EDPS skeleton) may not
be complete. 

## SOF Files

A set of SOF files to match the simulated data is provided in sofFiles/. There is one SOF file for
each recipe, with the exception of

 - SOF files for both lamp and twilight flats
 - recipes for both sci/std  processing in the metis_det_img_basic_reduce recipes
 
due to recipes that handle more than one type of input data that is used as input for another recipe.

# Output FITS Files

A summary spreadsheet of the files can be found [here].(https://docs.google.com/spreadsheets/d/1WW2CTb9ZTmTsDVCFfH5E_shXY9rRbVToDdXYt0VA-_4/edit?usp=sharing)

The set of simulations is as follows

## Science + Calibrations

- LM/N Science Source: a star field 
- LSS/IFU Science Source: extended galaxy

  - sky fields for each science exposure
  - standard star (centred point source) for each filter/instrument combination
  - sky fields for each standard star

- Coronagraphic RAW Files for

   - RAVC,LM, APP,LM, RAVC,IFU
       - sky fields for each mode
       - off axis PSF

- Flat field / RSRF as appropriate for each  instrument / filter combination.
- RSRF images are generated for two lamp temperatures. 

- Dark Frames for each exposure time / instrument combination
   
## Technical and Calibrations

- Set of images for detector linearity and gain calculationes
- Distortion images with the pinhole mask
- RSRF images with the pinhole mask for order tracing
- set of images for slitloss determination
- set of laser spectrum images for wavelength calibration
- chopperhome images
- pupil images
- dark frames to match the exposure times for the above

## External Calibration Files

 - PINHOLE_TABLE
 - LASER_TAB
 - LSF_KERNEL
 - LM_LSS_WAVE_GUESS
 - N_LSS_WAVE_GUESS
 - N_LSS_DIST_SOL
 - LM_DIST_SOL
 - ATM_PROFILE
 - AO_PSF_MODEL
 - N_SYNTH_TRANS
 - LM_SYNTH_TRANS
 - FLUXSTD_CATALOG
 - REF_STD_CAT_star1
 - PERSISTANCE_MAP

The list of  RAW files and external calibration files was compiled from the DRLD recipe listings
in Chapter 6, specifically the "Input Data" entry. FITS keywords and file types were
cross-checked against

    - INS.mode values of Table 2 of the DRLD.
    - List of needed calibrations / mode from Table 4
    - Alias keywords (needed for the EDPS skeleton)  given in Table 5
    - Matched keywords (needed for the EDPS skeleton)  given in Table 6.
    - The DPR.CATG, TECH, TYPE etc. given in Table 20.

# Generating Custom Simulations

If you want to run the scripts for your own models, there are two files you will need to edit, in addition to the command line options given above.

## YAML file

This file consists of a sequence of templates in the form

```
LM_IMAGE_SCI_RAW1:
  do.catg: LM_IMAGE_SCI_RAW
  mode: "img_lm"
  source: 
    name: star_field
    kwargs: {}
  properties:
    dit: 0.25
    ndit: 4
    filter_name: "Lp"
    catg: "SCIENCE"
    tech: "IMAGE,LM"
    type: "OBJECT"
    nObs: 5
```

The first line is a unique label for the template.

mode: one of

|mode  |description    |
|------|---------------|
|img_lm|imaging LM band|
|img_n |imaging N band |
|lss_l |LSS L band     |
|lss_m |LSS M band     |
|lss_n |LSS N band     |
|lms   |IFU            |


source:  details on the source to be used. Sources are given in sources.py
  A source consists of a name, as in sources.py, and a (possibly empty)
  list of kwargs (key word arguments). See file sources.py for details.

current sources

|source           |description                    |
|-----------------|-------------------------------|
|empty_sky        |blank sky                      |
|flat_field       |lamp flat                      |
|star_field       |fixed set of stellar sources   |
|simple_star12    |12th mag point source at centre|
|simple_star18    |18th mag point source at centre|
|simple_gal       |elliptical galaxy              |
|pinhole_mask     |pinhole mask on WCU            |
|laser_spectrum_lm|laser spectrum (LM) on WCU     |
|laser_spectrum_n |laser spectrum (N) on WCU      |

properties:

dit:  DIT value (float)

ndit: NDIT value (integer)

filter_name: one of

|filter_name  |band|
|-------------|----|
|open         |any |
|closed       |any |
|Lp           |LM  |
|short-L      |LM  |
|L_spec       |LM  |
|Mp           |LM  |
|M_spec       |LM  |
|Br_alpha     |LM  |
|Br_alpha_ref |LM  |
|PAH_3.3      |LM  |
|PAH_3.3_ref  |LM  |
|CO_1-0_ice   |LM  |
|CO_ref       |LM  |
|H2O-ice      |LM  |
|IB_4.05      |LM  |
|HCI_L_short  |LM  |
|HCI_L_long   |LM  |
|HCI_M        |LM  |
|N1           |N   |
|N2           |N   |
|N3           |N   |
|N_spec       |N   |
|PAH_8.6      |N   |
|PAH_8.6_ref  |N   |
|PAH_11.25    |N   |
|PAH_11.25_ref|N   |
|Ne_II        |N   |
|Ne_II_ref    |N   |
|S_IV         |N   |
|S_IV_ref     |N   |

ndfilter_name: optional, one of

|ndfilter_name|
|-------------|
|open         |
|ND_OD1       |
|ND_OD2       |
|ND_OD3       |
|ND_OD4       |
|ND_OD5       |

catg: one of

|catg     |
|---------|
|CALIB    |
|SCIENCE  |
|TECHNICAL|
|---------|

tech:  one of

|tech    |description              |
|--------|-------------------------|
|IMAGE,LM|imaging                  |
|IMAGE,N |imaging                  |
|LMS     |ifu                      |
|LSS,LM  |longslit spectroscopy    |
|LSS,N   |longslit spectroscopy    |
|PUP,M   |pupil imaging            |
|PUP,N   |pupil imaging            |
|APP,LM  |APP coronagraph, imaging |
|RAVC,IFU|RAVC coronagraph, IFU    |
|RAVC,LM |RAVC coronagraph, imaging|


 type: one of

|TYPE         |description                   |
|-------------|------------------------------|
|DARK         |   dark frame                 |
|CHOPHOME     |chopper home                  |
|DARK,WCUOFF  |dark (WCU)                    |
|FLAT,TWILIGHT|   skyflat                    |
|FLAT,LAMP    |lamp flat                     |
|DETLIN       |linearity determination       |
|OBJECT       |science object                |
|SKY          |sky frame                     |
|STD          |standard source               |
|DISTORTION   |distortion (WCU, pinhole mask)|
|WAVE         |wavelength calibration        |
|PSF,OFFAXIS  |off axis PSF (coronagraph)    |
|PUPIL        |pupil imaging                 |


 nObs: number of each observation to execute

 dateobs: date in the form  yyyy-mm-dd hh:mm:ss.s

