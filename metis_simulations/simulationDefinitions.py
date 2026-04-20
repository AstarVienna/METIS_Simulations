#!/usr/bin/env python
"""
Useful definitions used in the simulations. This file generally does not 
need to be edited by the user.

"""

import astropy.units as u
import scopesim as sim
import scopesim_templates as sim_tp
import numpy as np
import os
DEFAULT_IRDB_LOCATION = os.environ["DEFAULT_IRDB_LOCATION"]
sim.rc.__config__["!SIM.file.local_packages_path"] = DEFAULT_IRDB_LOCATION

# valid values of input parameters.
#
# DPR.CATG / .TYPE / .TECH values below follow the pipeline classification
# rules in METIS_Pipeline/metisp/workflows/metis/metis_classification.py,
# which is the authoritative source. A few extensions are kept for YAML
# inputs that don't map 1:1 onto a classification rule:
#   - TECHNICAL (catg): used for engineering/AIT frames like pupil imaging.
#   - APP,LM / RAVC,LM / RAVC,IFU / PUP,LM / PUP,N (tech): coronagraph /
#     pupil tech modes outside the core pipeline's classification scope.
#   - LMS (tech): ScopeSim-side form of IFU; updateHeaders() rewrites it
#     to IFU on output.
#   - CHOPHOME / PSF,OFFAXIS / PUPIL / PERSISTENCE (type): simulation-only
#     types without a matching pipeline classification rule.

catgVals = ["CALIB", "SCIENCE", "TECHNICAL"]
techVals = ["APP,LM", "IFU", "IMAGE,LM", "IMAGE,N", "LMS",
            "LSS,LM", "LSS,N", "PUP,LM", "PUP,N", "RAVC,IFU", "RAVC,LM"]
typeVals = ["CHOPHOME", "DARK", "DARK,WCUOFF", "DETLIN", "DISTORTION",
            "FLAT,LAMP", "FLAT,LAMP,PINH", "FLAT,TWILIGHT", "OBJECT",
            "PERSISTENCE", "PSF,OFFAXIS", "PUPIL", "RSRF", "SKY", "STD",
            "SLITLOSS", "WAVE"]
modeVals = ["img_lm", "img_n", "lms", "lss_l", "lss_m", "lss_n",
            "wcu_img_lm", "wcu_img_n", "wcu_lms",
            "wcu_lss_l", "wcu_lss_m", "wcu_lss_n"]


# filters sorted by mode. extracted from scopesim allowed combinations
# \TODO check LMS values and HCI values
_IMG_LM_FILTERS = ["Lp", "short-L", "Mp", "Br_alpha", "Br_alpha_ref",
                   "PAH_3.3", "PAH_3.3_ref", "CO_1-0_ice", "CO_ref",
                   "H2O-ice", "IB_4.05", "open", "closed",
                   "HCI_M", "HCI_L_short", "HCI_L_long"]
_IMG_N_FILTERS = ["N1", "N2", "N3", "PAH_8.6", "PAH_8.6_ref",
                  "PAH_11.25", "PAH_11.25_ref", "Ne_II", "Ne_II_ref",
                  "S_IV", "S_IV_ref", "open", "closed"]

# LSS and IMG share the same filter wheel, so any LM-band or N-band
# imaging filter is reachable in the matching LSS mode (AIT transmission
# sweeps rely on this). Hence LSS lists = spec filter + imaging filters
# of the same band.
_LSS_L_FILTERS = ["L_spec"] + _IMG_LM_FILTERS
_LSS_M_FILTERS = ["M_spec"] + _IMG_LM_FILTERS
_LSS_N_FILTERS = ["N_spec"] + _IMG_N_FILTERS

validFilters = {
    "img_lm": _IMG_LM_FILTERS,
    "img_n": _IMG_N_FILTERS,
    "lss_l": _LSS_L_FILTERS,
    "lss_m": _LSS_M_FILTERS,
    "lss_n": _LSS_N_FILTERS,
    "lms": _IMG_LM_FILTERS,
    # WCU-lamp variants share the filter set of their non-WCU equivalent.
    "wcu_img_lm": _IMG_LM_FILTERS,
    "wcu_img_n": _IMG_N_FILTERS,
    "wcu_lss_l": _LSS_L_FILTERS,
    "wcu_lss_m": _LSS_M_FILTERS,
    "wcu_lss_n": _LSS_N_FILTERS,
    "wcu_lms": _IMG_LM_FILTERS,
}


validND = ["open", "ND-2.8", "ND_OD1", "ND_OD2", "ND_OD3", "ND_OD4", "ND_OD5"]

hciFilters = ["HCI_M","HCI_L_short","HCI_L_long","open","closed"]


# keywords that must exist, either at the top level, or in properties  

topKey = ["do.catg","mode","properties"]
propKey = ["dit","ndit","filter_name","catg","tech","type","nObs"]


# some templates for calibration dictionaries. DIT/NDIT/obsdate need to be added
# for a runnable dictionary.
# DARK
# DARK,WCUOFF
# FLAT,LAMP
# FLAT,TWILIGHT
#
#templates = {}
#templates['wcudarklm'] = "wcudarklm.yaml"
#templates['wcudarkn'] = "wcudarklm.yaml"
#templates['wcudarkifu'] = "wcudarklm.yaml"
#templates['darklm'] = "darklm.yaml"
#templates['darkn'] = "darklm.yaml"
#templates['darkifu'] = "darklm.yaml"
#
#templates['lampflatlm'] = "lampflatlm.yaml"
#templates['lampflatn'] = "lampflatlm.yaml"
#templates['skyflatlm'] = "skyflatlm.yaml"
#templates['skyflatn'] = "skyflatlm.yaml"


WCUDARKLM = {
    "do.catg": "LM_IMG_WCUOFF_RAW",
    "mode": "wcu_img_lm",
    "source":{'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,LM",
        "type": "DARK,WCUOFF",
        "filter_name": "open",
        "ndfilter_name": "closed",
        "tplname":'METIS_img_lm_det_dark',},
    "wcu": {
        "current_lamp": "bb",
        "current_fpmask": "open",
        "bb_aperture": 0.0,
        "bb_temp": 300,
        "is_temp": 300,
        "wcu_temp": 300}}


WCUDARKN = {
    "do.catg": "N_IMG_WCUOFF_RAW",
    "mode": "wcu_img_n",
    "source": {'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,N",
        "type": "DARK,WCUOFF",
        "filter_name": "open",
        "ndfilter_name": "closed",
        "tplname":'METIS_img_n_det_dark',},
    "wcu": {
        "current_lamp": "bb",
        "current_fpmask": "open",
        "bb_aperture": 0.0,
        "bb_temp": 300,
        "is_temp": 300,
        "wcu_temp": 300}}


WCUDARKIFU = {
    "do.catg": "IFU_WCUOFF_RAW",
    "mode": "wcu_lms",
    "source": {'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "LMS",
        "type": "DARK,WCUOFF",
        "filter_name": "open",
        "ndfilter_name": "closed",
        "tplname":'METIS_lms_det_dark',},
    "wcu": {
        "current_lamp": "bb",
        "current_fpmask": "open",
        "bb_aperture": 0.0,
        "bb_temp": 300,
        "is_temp": 300,
        "wcu_temp": 300}}


DARKLM = {
    "do.catg": "DARK_2RG_RAW",
    "mode": "img_lm",
    "source":{'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "catg": "CALIB",
        "tech": "IMAGE,LM",
        "type": "DARK",
        "filter_name": "closed",
        "ndfilter_name": "open",
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
        "ndfilter_name": "open",
        "tplname":'METIS_lms_det_dark',}}

LAMPFLATLM = {
    "do.catg": "LM_FLAT_LAMP_RAW",
    "mode": "img_lm",
    "source": {'name': 'flat_field', 'kwargs': {'temperature': 200, 'amplitude': 0, 'filter_curve': 'V', 'extend': 15}},
    "properties": {
        "dit": 1,
        "ndit": 1,
        "catg": "CALIB",
        "tech": "IMAGE,LM",
        "type": "FLAT,LAMP",
        "ndfilter_name": "open",
        "tplname":'METIS_img_lm_det_flat',}}

LAMPFLATN = {
    "do.catg": "N_FLAT_LAMP_RAW",
    "mode": "img_n",
    "source": {'name': 'flat_field', 'kwargs': {'temperature': 200, 'amplitude': 0, 'filter_curve': 'V', 'extend': 15}},
    "properties": {
        "dit": 1,
        "ndit": 1,
        "catg": "CALIB",
        "tech": "IMAGE,N",
        "type": "FLAT,LAMP",
        "ndfilter_name": "open",
        "tplname":'METIS_img_n_det_flat',}}

    
SKYFLATLM = {
    "do.catg": "LM_FLAT_TWILIGHT_RAW",
    "mode": "img_lm",
    "source":{'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "dit": 1,
        "ndit": 1,
        "catg": "CALIB",
        "tech": "IMAGE,LM",
        "type": "FLAT,TWILIGHT",
        "ndfilter_name": "open",
        "tplname":'METIS_img_lm_det_flat',}}

SKYFLATN = {
    "do.catg": "N_FLAT_TWILIGHT_RAW",
    "mode": "img_lm",
    "source":{'name': 'empty_sky', 'kwargs': {}},
    "properties": {
        "dit": 1,
        "ndit": 1,
        "catg": "CALIB",
        "tech": "IMAGE,N",
        "type": "FLAT,TWILIGHT",
        "ndfilter_name": "open",
        "tplname":'METIS_img_n_det_flat',}}
