import astropy.units as u
import scopesim as sim
import scopesim_templates as sim_tp


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
    "simple_star12": (
        sim_tp.stellar.star,
        {
            "filter_name":"V",
            "amplitude": [12]*u.mag,
        }),
    "simple_star8": (
        sim_tp.stellar.star,
        {
            "filter_name":"V",
            "amplitude": [8 ]*u.mag,
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
        }

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

        )

}

MODESDICT = {
    "IMAGE,LM": "img_lm",
    "IMAGE,N": "img_n",
    "LSS,LM": "lss_l",
    "LSS,LM": "lss_m",
    "LSS,N": "lss_n",
    "IFU": "ifu",
    "LMS": "lms",
}


SOURCEMODEDICT = {
    "DARK": "empty",
    "DETLIN": "flat",
    "RSRF": "flat",
}

DEFAULT_IRDB_LOCATION = "../IRDB/"
