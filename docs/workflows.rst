Workflow Summary
================

This page catalogues every simulation block workflow shipped with the
repository. Each workflow is a Python script that bundles a set of YAML
observation templates and parameters to produce a self-contained dataset for
one instrument mode.

All workflows follow the same pattern: call
``runSimulationBlock(yamlFiles, params)`` with a list of YAML files and a
parameter dictionary. See :doc:`writing_workflows` for how to create your own.


imgLM -- LM-band Imaging
-------------------------

:Script: ``python/imgLM.py``
:Output directory: ``output/imgLM``
:Start date: ``2027-01-25 00:00:00``
:Calibrations: 3 darks/flats per type, static calibrations enabled

YAML files used:

* ``scienceLM.yaml`` -- science exposures and sky frames
* ``stdLM.yaml`` -- standard star and sky
* ``distortionLM.yaml`` -- pinhole-mask distortion calibration
* ``detlinLM.yaml`` -- detector linearity series

Produces these FITS file categories:

.. list-table::
   :header-rows: 1
   :widths: 40 15 15 30

   * - DO category
     - Source
     - Filter
     - Notes
   * - ``LM_IMAGE_SCI_RAW``
     - star_field
     - Lp
     - 3 science exposures
   * - ``LM_IMAGE_SCI_SKY_RAW``
     - empty_sky
     - Lp
     - 3 sky frames
   * - ``LM_IMAGE_STD_RAW``
     - calib_star
     - Lp
     - 3 standard star exposures
   * - ``LM_IMAGE_STD_SKY_RAW``
     - empty_sky
     - Lp
     - 3 standard sky frames
   * - ``LM_DISTORTION_RAW``
     - pinhole_mask
     - Lp
     - WCU pinhole distortion
   * - ``DETLIN_2RG_RAW``
     - empty_sky
     - closed
     - 4 DITs (1, 2, 3, 4 s)

Plus auto-generated darks, lamp flats, and twilight flats.


imgN -- N-band Imaging
----------------------

:Script: ``python/imgN.py``
:Output directory: ``output/imgN``
:Start date: ``2027-01-26 00:00:00``
:Calibrations: 2 darks/flats per type, static calibrations enabled

YAML files used:

* ``scienceN.yaml``
* ``stdN.yaml``
* ``distortionN.yaml``
* ``detlinN.yaml``

Produces these FITS file categories:

.. list-table::
   :header-rows: 1
   :widths: 40 15 15 30

   * - DO category
     - Source
     - Filter
     - Notes
   * - ``N_IMAGE_SCI_RAW``
     - star_field
     - N2
     - 1 science exposure
   * - ``N_IMAGE_SCI_SKY_RAW``
     - empty_sky
     - N2
     - 1 sky frame
   * - ``N_IMAGE_STD_RAW``
     - calib_star
     - N2
     - 1 standard
   * - ``N_IMAGE_STD_SKY_RAW``
     - empty_sky
     - N2
     - 1 standard sky
   * - ``N_DISTORTION_RAW``
     - pinhole_mask
     - N2
     - WCU pinhole distortion
   * - ``DETLIN_GEO_RAW``
     - empty_sky
     - closed
     - 4 DITs (1, 2, 3, 4 s)


lssLM -- LM-band Long-Slit Spectroscopy
----------------------------------------

:Script: ``python/lssLM.py``
:Output directory: ``output/lssLM``
:Start date: ``2027-01-27 00:00:00``
:Calibrations: 2 darks/flats, static calibrations enabled
:Extra parameter: ``slit_name = "C-38_1"``

YAML files used:

* ``scienceLSSLM.yaml`` -- galaxy science + sky
* ``stdLSSLM.yaml`` -- standard star + sky
* ``detlinLM.yaml`` -- detector linearity
* ``distortionLM.yaml`` -- distortion
* ``rsrfLSSLM.yaml`` -- relative spectral response (2 lamp temperatures)
* ``rsrfPinhLSSLM.yaml`` -- pinhole RSRF
* ``wavecalLSSLM.yaml`` -- wavelength calibration (internal laser)
* ``slitlossLSSLM.yaml`` -- slit-loss measurement

Produces these FITS file categories:

.. list-table::
   :header-rows: 1
   :widths: 40 15 15 30

   * - DO category
     - Source
     - Filter
     - Notes
   * - ``LM_LSS_SCI_RAW``
     - simple_gal
     - L_spec
     - Galaxy spectrum
   * - ``LM_LSS_SCI_SKY_RAW``
     - empty_sky
     - L_spec
     - Sky frame
   * - ``LM_LSS_STD_RAW``
     - calib_star
     - L_spec
     - Standard star
   * - ``LM_LSS_STD_SKY_RAW``
     - empty_sky
     - L_spec
     - Standard sky
   * - ``LM_LSS_RSRF_RAW``
     - flat_field
     - L_spec
     - 2 lamp temps (8000 K, 800 K)
   * - ``LM_LSS_RSRF_PINH_RAW``
     - pinhole_mask
     - L_spec
     - Pinhole RSRF, 2 lamp temps
   * - ``LM_LSS_WAVE_RAW``
     - laser_spectrum_lm
     - L_spec
     - Wavelength calibration
   * - ``LM_SLITLOSSES_RAW``
     - calib_star
     - L_spec
     - Slit-loss measurement
   * - ``DETLIN_2RG_RAW``
     - empty_sky
     - closed
     - Detector linearity
   * - ``LM_DISTORTION_RAW``
     - pinhole_mask
     - Lp
     - Distortion


lssN -- N-band Long-Slit Spectroscopy
--------------------------------------

:Script: ``python/lssN.py``
:Output directory: ``output/lssN``
:Start date: ``2027-01-28 00:00:00``
:Calibrations: 2 darks/flats, static calibrations enabled
:Extra parameter: ``slit_name = "D-57_1"``

YAML files used:

* ``scienceLSSN.yaml``
* ``stdLSSN.yaml``
* ``detlinN.yaml``
* ``distortionN.yaml``
* ``rsrfLSSN.yaml``
* ``rsrfPinhLSSN.yaml``
* ``wavecalLSSN.yaml``
* ``slitlossLSSN.yaml``

Produces these FITS file categories:

.. list-table::
   :header-rows: 1
   :widths: 40 15 15 30

   * - DO category
     - Source
     - Filter
     - Notes
   * - ``N_LSS_SCI_RAW``
     - simple_gal
     - open
     - Galaxy spectrum
   * - ``N_LSS_SCI_SKY_RAW``
     - empty_sky
     - open
     - Sky frame
   * - ``N_LSS_STD_RAW``
     - calib_star
     - open
     - Standard star
   * - ``N_LSS_STD_SKY_RAW``
     - empty_sky
     - open
     - Standard sky
   * - ``N_LSS_RSRF_RAW``
     - flat_field
     - open
     - 2 lamp temps (8000 K, 800 K)
   * - ``N_LSS_RSRF_PINH_RAW``
     - pinhole_mask
     - open
     - Pinhole RSRF, 2 lamp temps
   * - ``N_LSS_WAVE_RAW``
     - laser_spectrum_n
     - open
     - Wavelength calibration
   * - ``N_LSS_SLITLOSSES_RAW``
     - calib_star
     - open
     - Slit-loss measurement
   * - ``DETLIN_GEO_RAW``
     - empty_sky
     - closed
     - Detector linearity
   * - ``N_DISTORTION_RAW``
     - pinhole_mask
     - N2
     - Distortion


ifu -- IFU (LMS) Spectroscopy
------------------------------

:Script: ``python/ifu.py``
:Output directory: ``output/ifu``
:Start date: ``2027-02-01 00:00:00``
:Calibrations: 2 darks/flats, static calibrations enabled
:Cores: 6 (IFU simulations are memory-intensive)

YAML files used:

* ``wavecalIFU.yaml`` -- wavelength calibration (laser, 3.555 um)
* ``scienceIFU.yaml`` -- galaxy science + sky
* ``stdIFU.yaml`` -- standard star + sky
* ``detlinIFU.yaml`` -- detector linearity
* ``distortionIFU.yaml`` -- distortion
* ``rsrfIFU.yaml`` -- relative spectral response
* ``rsrfPinhIFU.yaml`` -- pinhole RSRF

Produces these FITS file categories:

.. list-table::
   :header-rows: 1
   :widths: 40 15 15 30

   * - DO category
     - Source
     - Filter
     - Notes
   * - ``IFU_WAVE_RAW``
     - laser_spectrum_lm
     - open
     - Laser at 3.555 um
   * - ``IFU_SCI_RAW``
     - simple_gal1
     - open
     - Galaxy, dit=100 s
   * - ``IFU_SCI_SKY_RAW``
     - empty_sky
     - open
     - Sky frame
   * - ``IFU_STD_RAW``
     - calib_star
     - open
     - Standard, dit=100 s, ndit=3
   * - ``IFU_STD_SKY_RAW``
     - empty_sky
     - open
     - Standard sky
   * - ``DETLIN_IFU_RAW``
     - empty_sky
     - closed
     - 4 DITs (1, 2, 3, 4 s)
   * - ``IFU_DISTORTION_RAW``
     - pinhole_mask
     - open
     - Distortion
   * - ``IFU_RSRF_RAW``
     - flat_field
     - open
     - 2 bb_aperture settings
   * - ``IFU_RSRF_PINH_RAW``
     - pinhole_mask
     - open
     - 2 bb_aperture settings


calib -- Standalone Calibrations
--------------------------------

:Script: ``python/calib.py``
:Output directory: ``output/Calib``
:Start date: ``2027-02-02 00:00:00``
:Calibrations: 2 darks/flats, static calibrations enabled

YAML files used:

* ``chophomeLM.yaml`` -- chopper home position
* ``pupilLM.yaml`` -- LM pupil imaging
* ``pupilN.yaml`` -- N pupil imaging
* ``slitlossLSSLM.yaml`` -- LM slit-loss
* ``slitlossLSSN.yaml`` -- N slit-loss

Produces these FITS file categories:

.. list-table::
   :header-rows: 1
   :widths: 40 15 15 30

   * - DO category
     - Source
     - Filter
     - Notes
   * - ``LM_CHOPHOME_RAW``
     - empty_sky
     - Lp
     - 3 chopper home frames
   * - ``LM_PUPIL_RAW``
     - star_sky1
     - Lp
     - Pupil imaging LM
   * - ``N_PUPIL_RAW``
     - star_sky1
     - N2
     - Pupil imaging N
   * - ``LM_SLITLOSSES_RAW``
     - calib_star
     - L_spec
     - Slit-loss LM
   * - ``N_LSS_SLITLOSSES_RAW``
     - calib_star
     - open
     - Slit-loss N


hciRavcLM -- High-Contrast Imaging, RAVC (LM)
-----------------------------------------------

:Script: ``python/hciRavcLM.py``
:Output directory: ``output/hciRavcLM``
:Start date: ``2027-01-31 00:00:00``
:Calibrations: 2 darks/flats, static calibrations enabled

YAML files used:

* ``offAxisLM.yaml`` -- off-axis PSF reference
* ``hciRavcLM.yaml`` -- RAVC coronagraphic science + sky
* ``distortionLM.yaml``
* ``detlinLM.yaml``
* ``stdLM.yaml`` -- photometric standard

Produces these FITS file categories:

.. list-table::
   :header-rows: 1
   :widths: 40 15 15 30

   * - DO category
     - Source
     - Filter
     - Notes
   * - ``LM_OFF_AXIS_PSF_RAW``
     - star_sky2
     - Lp
     - Off-axis PSF
   * - ``LM_IMAGE_SCI_CORONAGRAPH_RAW``
     - calib_star
     - open
     - RAVC coronagraph, dit=0.25 s
   * - ``LM_IMAGE_SKY_CORONAGRAPH_RAW``
     - empty_sky
     - Lp
     - Sky for coronagraph
   * - ``LM_DISTORTION_RAW``
     - pinhole_mask
     - Lp
     - Distortion
   * - ``DETLIN_2RG_RAW``
     - empty_sky
     - closed
     - Detector linearity
   * - ``LM_IMAGE_STD_RAW``
     - calib_star
     - Lp
     - Standard star
   * - ``LM_IMAGE_STD_SKY_RAW``
     - empty_sky
     - Lp
     - Standard sky


hciAppLM -- High-Contrast Imaging, APP (LM)
--------------------------------------------

:Script: ``python/hciAppLm.py``
:Output directory: ``output/hciAppLM``
:Start date: ``2027-01-29 00:00:00``
:Calibrations: 2 darks/flats, static calibrations enabled

YAML files used:

* ``offAxisLM.yaml`` -- off-axis PSF reference
* ``hciAppLM.yaml`` -- APP coronagraphic science + sky
* ``distortionLM.yaml``
* ``detlinLM.yaml``

Produces these FITS file categories:

.. list-table::
   :header-rows: 1
   :widths: 40 15 15 30

   * - DO category
     - Source
     - Filter
     - Notes
   * - ``LM_OFF_AXIS_PSF_RAW``
     - star_sky2
     - Lp
     - Off-axis PSF
   * - ``LM_IMAGE_SCI_CORONAGRAPH_RAW``
     - calib_star
     - Lp
     - APP coronagraph
   * - ``LM_IMAGE_SKY_CORONAGRAPH_RAW``
     - empty_sky
     - Lp
     - Sky for coronagraph
   * - ``LM_DISTORTION_RAW``
     - pinhole_mask
     - Lp
     - Distortion
   * - ``DETLIN_2RG_RAW``
     - empty_sky
     - closed
     - Detector linearity


hciRavcIfu -- High-Contrast Imaging, RAVC (IFU)
-------------------------------------------------

:Script: ``python/hciRavcIfu.py``
:Output directory: ``output/hciRavcIfu``
:Start date: ``2027-01-30 00:00:00``
:Calibrations: 2 darks/flats, static calibrations enabled
:Cores: 6 (IFU simulations are memory-intensive)

YAML files used:

* ``offAxisLM.yaml`` -- off-axis PSF reference (img_lm mode)
* ``hciRavcIfu.yaml`` -- RAVC IFU coronagraphic science + sky
* ``distortionIFU.yaml``
* ``detlinIFU.yaml``
* ``rsrfIFU.yaml`` -- relative spectral response
* ``rsrfPinhIFU.yaml`` -- pinhole RSRF
* ``wavecalIFU.yaml`` -- wavelength calibration

Produces these FITS file categories:

.. list-table::
   :header-rows: 1
   :widths: 40 15 15 30

   * - DO category
     - Source
     - Filter
     - Notes
   * - ``LM_OFF_AXIS_PSF_RAW``
     - star_sky2
     - Lp
     - Off-axis PSF (img_lm mode)
   * - ``IFU_SCI_CORONAGRAPH_RAW``
     - calib_star
     - open
     - RAVC IFU, dit=100 s, 3.555 um
   * - ``IFU_SKY_CORONAGRAPH_RAW``
     - empty_sky
     - open
     - Sky, dit=100 s, 3.555 um
   * - ``IFU_DISTORTION_RAW``
     - pinhole_mask
     - open
     - Distortion
   * - ``DETLIN_IFU_RAW``
     - empty_sky
     - closed
     - 4 DITs (1, 2, 3, 4 s)
   * - ``IFU_RSRF_RAW``
     - flat_field
     - open
     - Relative spectral response
   * - ``IFU_RSRF_PINH_RAW``
     - pinhole_mask
     - open
     - Pinhole RSRF
   * - ``IFU_WAVE_RAW``
     - laser_spectrum_lm
     - open
     - Laser wavelength calibration


Auto-Generated Calibrations
----------------------------

When ``doCalib > 0``, the framework inspects every template that was simulated
and automatically generates matching calibration frames:

**Dark frames** -- one set for each unique DIT/NDIT/detector combination
found in the science and calibration templates.

**Lamp flats** -- flat-field exposures using the WCU blackbody source, matched
to each filter used.

**Twilight flats** -- flat-field exposures using a twilight sky source, matched
to each filter used.

The ``doCalib`` parameter controls how many of each calibration type to
generate (e.g. ``doCalib=3`` produces 3 darks and 3 flats per configuration).


Static Calibration Files
-------------------------

When ``doStatic=True``, the framework generates prototype FITS files for
external/static calibrations via ``makeCalibPrototypes.py``:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - File
     - Description
   * - ``REF_STD_CAT``
     - Reference standard star catalogue
   * - ``FLUXSTD_CATALOG``
     - Flux standard source catalogue
   * - ``PINHOLE_TABLE``
     - Pinhole mask position table
   * - ``LASER_TAB``
     - Laser spectrum table
   * - ``LSF_KERNEL``
     - Line Spread Function kernel
   * - ``LM_LSS_WAVE_GUESS`` / ``N_LSS_WAVE_GUESS``
     - Initial wavelength guess for LSS
   * - ``LM_DIST_SOL`` / ``N_LSS_DIST_SOL``
     - Distortion solution tables
   * - ``ATM_PROFILE``
     - Atmospheric transmission profile
   * - ``AO_PSF_MODEL``
     - Adaptive optics PSF model
   * - ``LM_SYNTH_TRANS`` / ``N_SYNTH_TRANS``
     - Synthetic transmission curves
   * - ``PERSISTANCE_MAP``
     - Detector persistence map
