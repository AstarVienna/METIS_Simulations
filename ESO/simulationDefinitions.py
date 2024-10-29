"""
Useful definitions used in the simulations. This file generally does not 
need to be edited by the user.

"""

import astropy.units as u
import scopesim as sim
import scopesim_templates as sim_tp
import numpy as np

# default location of IRDB
DEFAULT_IRDB_LOCATION = "../IRDB/"


# variables that can be expanded

expandables = [
    "dit",
]

# valid values of input parameters

catgVals = ["CALIB","SCIENCE","TECHNICAL"]
techVals = ["APP,LM","IMAGE,LM","IMAGE,N","LMS","LSS,LM","LSS,N","PUP,M","PUP,N","RAVC,IFU","RAVC,LM"]
typeVals = ["CHOPHOME","DARK,WCUOFF","DETLIN","DISTORTION","FLAT,LAMP","OBJECT","PSF,OFFAXIS","PUPIL","SKY","STD","WAVE","SLITLOSS"]
modeVals = ["img_lm","lss_m","img_n","lss_l","lss_m","lss_n","lms"]


# filters sorted by mode. extracted from scopesim allowed combinations \TODO check LMS values and HCI values
validFilters = {
    "img_lm" : ["Lp","short-L","Mp","Br_alpha","Br_alpha_ref","PAH_3.3","PAH_3.3_ref","CO_1-0_ice","CO_ref","H2O-ice","IB_4.05","open","closed", "HCI_M","HCI_L_short","HCI_L_long"],
    "img_n" : ["N1","N2","N3","PAH_8.6","PAH_8.6_ref","PAH_11.25","PAH_11.25_ref","Ne_II","Ne_II_ref","S_IV","S_IV_ref","open","closed"],
     "lss_l": ["L_spec"],
     "lss_m": ["M_spec"],
     "lss_n": ["N_spec"],
      "lms": ["Lp","short-L","Mp","Br_alpha","Br_alpha_ref","PAH_3.3","PAH_3.3_ref","CO_1-0_ice","CO_ref","H2O-ice","IB_4.05","open","closed", "HCI_M","HCI_L_short","HCI_L_long"],
    }


validND = ["open","ND_OD1","ND_OD2","ND_OD3","ND_OD4","ND_OD5"]

hciFilters = ["HCI_M","HCI_L_short","HCI_L_long","open","closed"]


# keywords that must exist, either at the top level, or in properties  

topKey = ["do.catg","mode","properties"]
propKey = ["dit","ndit","filter_name","catg","tech","type","nObs"]


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


# some templates for calibration dictionaries. DIT/NDIT/obsdate need to be added
# for a runnable dictionary.
# DARK
# DARK,WCUOFF
# FLAT,LAMP
# FLAT,TWILIGHT


WCUDARKLM = {
    "do.catg": "LM_WCU_OFF_RAW",
    "mode": "img_lm",
    "source":{'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,LM",
        "type": "DARK,WCUOFF",
        "filter_name": "closed",
        "tplname":'METIS_img_lm_det_dark',}}

WCUDARKN = {
    "do.catg": "N_WCU_OFF_RAW",
    "mode": "img_n",
    "source": {'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,N",
        "type": "DARK,WCUOFF",
        "filter_name": "closed",
        "tplname":'METIS_img_n_det_dark',}}

WCUDARKIFU = {
    "do.catg": "IFU_WCU_OFF_RAW",
    "mode": "lms",
    "source": {'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "LMS",
        "type": "DARK,WCUOFF",
        "filter_name": "closed",
        "tplname":'METIS_lms_det_dark',}}

DARKLM = {
    "do.catg": "DARK_2RG_RAW",
    "mode": "img_lm",
    "source":{'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,LM",
        "type": "DARK",
        "filter_name": "closed",
        "tplname":'METIS_img_lm_det_dark',}}

DARKN = {
    "do.catg": "DARK_GEO_RAW",
    "mode": "img_n",
    "source": {'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,N",
        "type": "DARK",
        "filter_name": "closed",
        "tplname":'METIS_img_n_det_dark',}}

DARKIFU = {
    "do.catg": "DARK_IFU_RAW",
    "mode": "lms",
    "source": {'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "LMS",
        "type": "DARK",
        "filter_name": "closed",
        "tplname":'METIS_lms_det_dark',}}

LAMPFLATLM = {
    "do.catg": "LM_FLAT_LAMP_RAW",
    "mode": "img_lm",
    "source": {'name': 'flat_field', 'kwargs': {'temperature': 200, 'amplitude': 0, 'filter_curve': 'V', 'extend': 15}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,LM",
        "type": "FLAT,LAMP",
        "tplname":'METIS_img_lm_det_flat',}}

LAMPFLATN = {
    "do.catg": "N_FLAT_LAMP_RAW",
    "mode": "img_n",
    "source": {'name': 'flat_field', 'kwargs': {'temperature': 200, 'amplitude': 0, 'filter_curve': 'V', 'extend': 15}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,N",
        "type": "FLAT,LAMP",
        "tplname":'METIS_img_n_det_flat',}}

    
SKYFLATLM = {
    "do.catg": "LM_FLAT_TWILIGHT_RAW",
    "mode": "img_lm",
    "source":{'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,LM",
        "type": "FLAT,TWILIGHT",
        "tplname":'METIS_img_lm_det_flat',}}

SKYFLATN = {
    "do.catg": "N_FLAT_TWILIGHT_RAW",
    "mode": "img_lm",
    "source":{'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,N",
        "type": "FLAT,TWILIGHT",
        "tplname":'METIS_img_n_det_flat',}}

