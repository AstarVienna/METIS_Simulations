#!/usr/bin/env python3
# coding: utf-8
import numpy as np
from numpy.random import rand, randint
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import scopesim as sim
from astropy.io import fits
import astropy.units as u
from astropy.wcs import WCS

fname = 'lms_sky'

cmd = sim.UserCommands(use_instrument='METIS', set_modes=['lms'],properties={"!OBS.wavelen": 3.55})
metis = sim.OpticalTrain(cmd)

src = sim.source.source_templates.empty_sky()
metis.observe(src)

result = metis.readout(exptime=600)[0]
result.writeto(fname+'.fits',overwrite=True)

# save WL into files, to later be able to plot the result
wcs_1 = WCS(result[1], key='D')
wcs_2 = WCS(result[2], key='D')
x_1, y_1 = wcs_1.all_pix2world(np.arange(2048), np.array([193] * 2048), 0)
x_2, y_2 = wcs_2.all_pix2world(np.arange(2048), np.array([193] * 2048), 0)
spt = metis['lms_spectral_traces'].spectral_traces['Slice 15']
lam_1 = spt.xy2lam(x_1, y_1)
lam_2 = spt.xy2lam(x_2, y_2)
np.save(fname+'lam1.npy',lam_1)
np.save(fname+'lam2.npy',lam_2)

# Plot the 4 detector images

fig = plt.figure(figsize=(8.29, 7.68))
axs = fig.subplots(2,2)
for i,ax in enumerate(axs.flat):
    ax.imshow(result[i+1].data,origin='lower', norm=LogNorm(vmin=100))
    ax.set_xticks([])
    ax.set_yticks([])
fig.tight_layout(pad=0.01)
fig.savefig(fname+'.png')
