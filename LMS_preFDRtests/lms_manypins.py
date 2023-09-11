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

cmd = sim.UserCommands(use_instrument='METIS', set_modes=['lms'])
metis = sim.OpticalTrain(cmd)


src = sim.source.source_templates.star(x=0, y=0, flux=0.0001*u.Jy)
nx=25; X = np.linspace(-0.45,0.45,nx)
ny=28; Y = np.linspace(-0.27945,0.27945,ny)

for y in Y:
    for x in X :
        src += sim.source.source_templates.star(x=x, y=y, flux=randint(1,12)*u.Jy)

metis.observe(src, update=True)
result = metis.readout(detector_readout_mode="auto")[0]

fname = 'lms_manypins'
result.writeto(fname+'.fits',overwrite=True)

fig = plt.figure(figsize=(8.29, 7.68))
axs = fig.subplots(2,2)
for i,ax in enumerate(axs.flat):
    ax.imshow(result[i+1].data,origin='lower', norm=LogNorm(vmin=100))
    ax.set_xticks([])
    ax.set_yticks([])
fig.tight_layout(pad=0.01)
fig.savefig(fname+'.png')


