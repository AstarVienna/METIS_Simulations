"""
Simualte an LM_IMAGE_SCI_RAW
"""

import datetime
from astropy import units as u
import scopesim
import scopesim_templates

def simulate():
    """Simulate an image."""
    # The source to simulate. We should make METIS-specific sources in
    # ScopeSim_Templates at some point.
    gal = scopesim_templates.extragalactic.galaxies.spiral_two_component(
        extent=16*u.arcsec, fluxes=(15, 15)*u.mag)

    cmd = scopesim.UserCommands(use_instrument="METIS", set_modes=["img_lm"])
    cmd.update(properties={
        # Settings of the observation. Would need to be parametrized at
        # some point.
        "!OBS.filter_name": "Mp",
        "!OBS.ndit": 30,
        "!OBS.dit": 0.3,

        # Header keywords copied from DRLD.
        # Can perhaps be put in a mode yaml at some point.
        "!OBS.catg": "SCIENCE",
        "!OBS.tech": "IMAGE,LM",
        "!OBS.type": "OBJECT",

        # Use a specific date for reproducibility.
        "!OBS.mjdobs": datetime.datetime(2024, 1, 2, 3, 45, 0)
    })

    metis = scopesim.OpticalTrain(cmd)
    metis.observe(gal)
    hdus = metis.readout("LM_IMAGE_SCI_RAW.fits")
    return hdus[0]


if __name__ == "__main__":
    simulate()
