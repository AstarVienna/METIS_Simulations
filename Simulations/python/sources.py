"""
Definition of sources used in template YAML files. Sources are derived from either
scopesim, or scopesim templates; you should understand these programs before making your
own. 
"""

import astropy.units as u
import scopesim as sim
import scopesim_templates as sim_tp
import numpy as np


import numpy as np
import scipy
import astropy.io.fits as fits
from astropy import units as u
import matplotlib.pyplot as plt

import scopesim


####################### Definitions used by the sources #########################

# import  ScopeSim information needed for some of the sources

imgLM = sim.OpticalTrain(sim.UserCommands(use_instrument="METIS", set_modes=["img_lm"]))
specDictLM = imgLM.cmds['!SIM.spectral']
imgN = sim.OpticalTrain(sim.UserCommands(use_instrument="METIS", set_modes=["img_n"]))
specDictN = imgN.cmds['!SIM.spectral']



# a fixed random star field; positions based on image size. We define position, magnitude in the reference
# band and spectral type



starFieldX = np.array([-4.08,3.51,4.01,0.94,3.49,-3.67,0.02,
                       2.68,4.20,-0.25,2.29,3.05,-1.00,-4.86,
                       -1.83,-0.60,-1.01,4.21,-2.84,4.34])
starFieldY =  np.array([4.79,-2.83,3.72,2.09,2.22,0.59,2.83,
                    -3.45,-0.25,3.02,4.29,4.43,0.37,-0.95,
                        2.49,-0.48,4.67,4.71,4.10,-0.52])

starFieldM  = np.array([14.0,12.4,13.7,13.4,13.4,13.1,13.6,
                        12.3,13.0,13.6,13.9,13.9,13.1,12.8,13.5,
                        12.9,13.9,13.9,13.8,12.9])*u.ABmag

starFieldT = ["b0v","a0v","a5v","f0v","f5v",
              "g0v","g2v","k0v","k5v",'m0v',
              "m5v",'g5iii',"a5v","f0v","f5v",
              "g0v","g2v","k0v","k5v",'m0v']


skyStarXa = np.array([-3.72,1.07,4.53,4.94,-0.31,-0.43,5.57,5.00,3.31,-5.48,-1.19,4.64,1.63,5.68,1.97,1.79,-3.87,5.47,-2.71,-3.84,-2.10,2.77,3.77,-1.84,-4.06])
skyStarYa = np.array([3.70,-5.22,-3.09,3.18,-5.25,-2.19,2.88,-1.55,-0.08,2.38,0.45,5.73,-0.70,-2.50,-2.36,0.75,3.84,-4.26,-3.78,4.68,-3.61,-4.62,0.02,-0.31,-4.50])
skyStarXb = skyStarXa + 1
skyStarYb = skyStarYa - 1

skyStarM = np.array([14.78,15.82,14.24,14.03,14.26,15.17,14.20,15.17,15.12,15.49,15.86,15.50,15.23,15.33,15.47,14.57,15.53,14.78,14.14,14.73,15.06,14.97,14.36,14.85,15.41])*u.ABmag
skyStarT = ["a0v"]*25

################### Setup input Images here (e.g. HEEPS input for coronagraph) #################


hdu = fits.ImageHDU(data=scipy.datasets.face(gray=True).astype('float'))

# Give the header some proper WCS info
hdu.header.update({"CDELT1": 1, "CUNIT1": "arcsec", "CRPIX1": 0, "CRVAL1": 0,
                   "CDELT2": 1, "CUNIT2": "arcsec", "CRPIX2": 0, "CRVAL2": 0,})



####################### Dictionary of Sources #########################

# Each entry contains a unique name, a scopesim or scopesim_templates source, and
# keywords needed by the source.


"""
empty_sky: blank sky, used for twilight flats and darks, or anywhere you don't want a source

flat_field: lamp based flat field.

star_field: fixed random star field

simpleStarNN: a single stellar source at the centre of the field with magnitude NN. The magnitude is
              fixed rather than set in the YAML file due to the need to pass the value with astropy units.

simple_gal: elliptical galaxy

pinhole_mask: pinhole mask for the WCU

laser_spectrum_lm: WCU laser spectrum, LM band

laser_spectrum_n: WCU laser spectrum, N band
"""



SOURCEDICT = {
    "empty_sky": (sim_tp.empty_sky, {}),
    "flat_field": (
        sim_tp.calibration.flat_field,
        {
            "temperature": 200,
            "amplitude": 0,
            "filter_curve": "V",
            "extend": 15,
        }
    ),
    "star_field":(
        sim_tp.stellar.stars,
        {
            "amplitudes":starFieldM,
            "x":starFieldX,
            "y":starFieldY,
            "filter_name":"Ks",
            "spec_types":starFieldT,
            "library":"kurucz",
        }),
    "star_sky1":(
        sim_tp.stellar.stars,
        {
            "amplitudes":skyStarM,
            "x":skyStarXa,
            "y":skyStarYa,
            "filter_name":"Ks",
            "spec_types":skyStarT,
            "library":"kurucz",
        }),
    "star_sky2":(
        sim_tp.stellar.stars,
        {
            "amplitudes":skyStarM,
            "x":skyStarXb,
            "y":skyStarYb,
            "filter_name":"Ks",
            "spec_types":skyStarT,
            "library":"kurucz",
        }),

    "calib_star": (
        sim_tp.stellar.star,
        {
            "filter_name":"Ks",
            "amplitude": 12,
            "library": "kurucz",
            "spec_type": "k5v"
            }),
        
    "simple_gal": (
        sim_tp.extragalactic.elliptical,
        {
            "sed":"brown/NGC4473",
            "z":0,
            "amplitude":5,
            "filter_name":"Ks",
            "pixel_scale":0.1,
            "half_light_radius":30,
            "n":4,
            "ellip":0.5,
            "ellipticity":0.5,
            "angle":30,
        },
        ),

    "simple_gal1": (
        sim_tp.extragalactic.elliptical,
        {
            "sed":"brown/NGC4473",
            "z":0,
            "amplitude":0,
            "filter_name":"Ks",
            "pixel_scale":0.1,
            "half_light_radius":30,
            "n":4,
            "ellip":0.5,
            "ellipticity":0.5,
            "angle":30,
        }
        ),
    "pinhole_mask": (
        sim_tp.metis.pinhole_mask,
        {
        }
        ),
    "laser_spectrum_lm": (
        sim_tp.metis.laser.laser_spectrum_lm,
        {
            "specdict":specDictLM,
        }
        ),
    "laser_spectrum_n": (
        sim_tp.metis.laser.laser_spectrum_n,
        {
            "specdict":specDictN,
        }
        ),
    "heeps_image": (
        scopesim.Source,
        {
            "image_hdu":hdu,
            "flux":10*u.ABmag,
        }
        ),


}
