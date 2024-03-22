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
            "amplitude": [5]*u.mag,
        }
    ),
    "simple_gal": (
        sim_tp.extragalactic.galaxy,
        {
            "sed":"brown/NGC4473",
            "z":0.1, 
            "amplitude":-100, 
            "filter_curve":"g", 
            "pixel_scale":0.05, 
            "r_eff":2.5, 
            "n":4, 
            "ellip":0.5, 
            "theta":45, 
            "extend":3,
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

