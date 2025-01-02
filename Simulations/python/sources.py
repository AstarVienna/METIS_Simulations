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

starFieldX = np.array([-8.15592743,  7.01303926,  8.01500244,  1.87226377,  6.97505972,
       -7.33994824,  0.04191974,  5.35931242,  8.40940718, -0.49102622,
        4.58550425,  6.10882803, -1.99466201, -9.72891962, -3.65611485,
       -1.20411157, -2.02697232,  8.42325234, -5.67781285,  8.68952776])


starFieldY = np.array([ 9.583468  , -5.65889576,  7.44908775,  4.17753575,  4.43878784,
        1.18114661,  5.65337934, -6.90408802, -0.49683094,  6.04866284,
        8.58989225,  8.85721093,  0.7475543 , -1.90119023,  4.98409528,
       -0.96123847,  9.34819477,  9.42408694,  8.20907011, -1.03093753])


starFieldM = np.array([13.9583468 , 12.43411042, 13.74490878, 13.41775357, 13.44387878,
       13.11811466, 13.56533793, 12.3095912 , 12.95031691, 13.60486628,
       13.85898923, 13.88572109, 13.07475543, 12.80988098, 13.49840953,
       12.90387615, 13.93481948, 13.94240869, 13.82090701, 12.89690625])

starFieldT = ["A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V"]


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
        }),

    "simple_star": (
        sim_tp.stellar.star,
        {
            "filter_name":"V",
            "amplitude": [10],
            }),
        
    "simple_star18": (
        sim_tp.stellar.star,
        {
            "filter_name":"V",
            "amplitude": [18],
        }),
    "simple_star12": (
        sim_tp.stellar.star,
        {
            "filter_name":"V",
            "amplitude": [12],
        }),
    "simple_star8": (
        sim_tp.stellar.star,
        {
            "filter_name":"V",
            "amplitude": [8 ],
        }
    ),
    "simple_star10": (
        sim_tp.stellar.star,
        {
            "filter_name":"V",
            "amplitude": [10 ],
            "x":0,
            "y":0,
        }
    ),
    "simple_stars":(
        sim_tp.stellar.stars,
        {
            "filter_name":"J",
            "amplitudes":[12],
            "x":[0],
            "y":[0],
            "spec_types":["m3v"],
            "library":"pickles",
            }
        ),

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
