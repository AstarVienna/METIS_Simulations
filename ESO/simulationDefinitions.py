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
typeVals = ["CHOPHOME","DARK,WCUOFF","DETLIN","DISTORTION","FLAT,LAMP","OBJECT","PSF,OFFAXIS","PUPIL","SKY","STD","WAVE",'SLITLOSS']
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

# some templates for calibrations
DARKLM = {
    "do.catg": "DARK_LM_RAW",
    "mode":"",
    "source":{'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,LM",
        "type": "DARK",
        "filter_name": "closed",
        "tplname":'METIS_img_lm_det_dark',}}

 # some templates for calibrations

DARKN = {
    "do.catg": "DARK_N_RAW",
    "mode":"",
    "source": {'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,N",
        "type": "DARK",
        "filter_name": "closed",
        "tplname":'METIS_img_n_det_dark',}}

DARKIFU = {
    "do.catg": "DARK_IFU_RAW",
    "mode":"",
    "source": {'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "LMS",
        "type": "DARK",
        "filter_name": "closed",
        "tplname":'METIS_lms_det_dark',}}

LAMPFLATLM = {
    "do.catg": "FLAT_LM_RAW",
    "mode":"",
    "source": {'name': 'flat_field', 'kwargs': {'temperature': 200, 'amplitude': 0, 'filter_curve': 'V', 'extend': 15}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,LM",
        "type": "FLAT,LAMP",
        "tplname":'METIS_img_lm_det_flat',}}

LAMPFLATN = {
    "do.catg": "FLAT_N_RAW",
    "mode":"",
    "source": {'name': 'flat_field', 'kwargs': {'temperature': 200, 'amplitude': 0, 'filter_curve': 'V', 'extend': 15}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,N",
        "type": "FLAT,LAMP",
        "tplname":'METIS_img_n_det_flat',}}

    
SKYFLATLM = {
    "do.catg": "FLAT_LM_RAW",
    "mode":"",
    "source":{'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,LM",
        "type": "FLAT,TWILIGHT",
        "tplname":'METIS_img_lm_det_flat',}}

SKYFLATN = {
    "do.catg": "FLAT_N_RAW",
    "mode":"",
    "source":{'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,N",
        "type": "FLAT,TWILIGHT",
        "tplname":'METIS_img_n_det_flat',}}

    
