"""dictionaries and other definitions for running raw_script"""

import astropy.units as u
import scopesim as sim
import scopesim_templates as sim_tp

MODESDICT = {
    "IMAGE,LM": "img_lm",
    "IMAGE,N": "img_n",
    "IFU": "ifu",
}

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
    "simple_star": (
        sim_tp.stellar.star,
        {
            "filter_name":"V",
            "amplitude": [12]*u.mag,
        }
        )
}
SOURCEMODEDICT = {
    "DARK": "empty",
    "DETLIN": "flat",
    "RSRF": "flat",
}

DEFAULT_IRDB_LOCATION = "../IRDB/"
