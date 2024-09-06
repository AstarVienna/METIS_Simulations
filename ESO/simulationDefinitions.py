"""
Useful definitions used in the simulations. This file generally does not 
need to be edited by the user.

"""

import astropy.units as u
import scopesim as sim
import scopesim_templates as sim_tp
import numpy as np

# valid values of input parameters

catgVals = ["CALIB","SCIENCE","TECHNICAL"]
techVals = ["APP,LM","IMAGE,LM","IMAGE,N","LMS","LSS,LM","LSS,N","PUP,M","PUP,N","RAVC,IFU","RAVC,LM"]
typeVals = ["CHOPHOME","DARK,WCUOFF","DETLIN","DISTORTION","FLAT,LAMP","OBJECT","PSF,OFFAXIS","PUPIL","SKY","STD","WAVE"]
modeVals = ["img_lm","lss_m","img_n","lss_l","lss_m","lss_n","lms"]


# dictionary of modes and tech

MODESDICT = {
    "RAVC,LM": "img_lm_ravc",
    "IMAGE,LM": "img_lm",
    "IMAGE,N": "img_n",
    "LSS,LM": "lss_m",
    "LSS,LM": "lss_l",
    "LSS,N": "lss_n",
    "IFU": "ifu",
    "LMS": "lms",
}


SOURCEMODEDICT = {
    "DARK": "empty",
    "DETLIN": "flat",
    "RSRF": "flat",
}

# default location of IRDB
DEFAULT_IRDB_LOCATION = "../IRDB/"


