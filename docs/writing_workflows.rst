How to Write a Workflow
=======================

A *workflow* (or *simulation block*) is a self-contained Python script that
produces all raw and calibration FITS files for a particular instrument mode.
This guide walks you through creating one from scratch.


Overview
--------

Every workflow does three things:

1. Lists the **YAML template files** that define which observations to simulate.
2. Provides a **parameter dictionary** controlling output location, calibration
   depth, parallelism, etc.
3. Calls ``runSimulationBlock(yamlFiles, params)`` to execute everything.


Quick Start
-----------

Create a file ``Simulations/python/myWorkflow.py``:

.. code-block:: python

   import runSimulationBlock as rs

   if __name__ == "__main__":

       params = {
           "outputDir":  "output/myWorkflow",
           "small":      False,
           "doStatic":   True,
           "doCalib":    2,
           "sequence":   True,
           "startMJD":   "2027-03-15 00:00:00",
           "calibFile":  None,
           "nCores":     8,
           "testRun":    False,
       }

       yamlFiles = [
           "YAML/scienceLM.yaml",
           "YAML/stdLM.yaml",
           "YAML/distortionLM.yaml",
           "YAML/detlinLM.yaml",
       ]

       rs.runSimulationBlock(yamlFiles, params)

Run it from the ``Simulations/`` directory::

   python python/myWorkflow.py


Parameter Reference
-------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Default
     - Description
   * - ``outputDir``
     - (required)
     - Directory where FITS files are written. Created automatically.
   * - ``small``
     - ``False``
     - If ``True``, generate 32x32 pixel images instead of full-size. Useful
       for quick testing and CI.
   * - ``doStatic``
     - ``False``
     - If ``True``, generate static calibration prototype files (pinhole table,
       laser table, distortion solution, etc.) alongside the raw files.
   * - ``doCalib``
     - ``0``
     - Number of dark and flat frames to auto-generate per unique DIT/filter
       combination found in the templates. Set to 0 to skip.
   * - ``sequence``
     - ``True``
     - If ``True``, observations get sequential, incrementing timestamps
       (``MJD-OBS``). If ``False``, each template uses the date from the YAML
       ``dateobs`` field.
   * - ``startMJD``
     - (required)
     - ISO-format start date for the observation sequence
       (``"YYYY-MM-DD HH:MM:SS"``).
   * - ``calibFile``
     - ``None``
     - Path to a separate YAML file defining calibration parameters. Usually
       left as ``None`` to use defaults from ``simulationDefinitions.py``.
   * - ``nCores``
     - ``8``
     - Number of CPU cores for parallel execution. The framework will use at
       most ``os.cpu_count() - 1``.
   * - ``testRun``
     - ``False``
     - If ``True``, run through all validation and setup but skip actual
       ScopeSim simulation. Useful for checking YAML templates.

Additional per-mode parameters can be added to the dict and will be forwarded:

* ``slit_name`` -- slit identifier for LSS modes (e.g. ``"C-38_1"``).


Writing YAML Templates
-----------------------

YAML files live in ``Simulations/YAML/`` and define one or more observation
templates. Each template is a YAML mapping with a unique label as key:

.. code-block:: yaml

   MY_UNIQUE_LABEL:
     do.catg: LM_IMAGE_SCI_RAW
     mode: "img_lm"
     source:
       name: star_field
       kwargs: {}
     properties:
       dit: 0.25
       ndit: 4
       filter_name: "Lp"
       catg: "SCIENCE"
       tech: "IMAGE,LM"
       type: "OBJECT"
       nObs: 5

A single YAML file can contain multiple templates. They are executed in order.

Template Fields
^^^^^^^^^^^^^^^

``do.catg`` (required)
   The DO category name that becomes the FITS file-name prefix, e.g.
   ``LM_IMAGE_SCI_RAW``.

``mode`` (required)
   The ScopeSim instrument mode:

   ========  ==========================
   Mode      Description
   ========  ==========================
   img_lm    LM-band imaging
   img_n     N-band imaging
   lss_l     L-band long-slit spectroscopy
   lss_m     M-band long-slit spectroscopy
   lss_n     N-band long-slit spectroscopy
   lms       IFU (integral field unit)
   ========  ==========================

``source`` (required)
   The astronomical or calibration source to use. Has two sub-fields:

   * ``name`` -- one of the source functions defined in ``sources.py``
   * ``kwargs`` -- keyword arguments passed to the source function (can be
     empty ``{}``)

   Available sources:

   =================  =====================================
   Source              Description
   =================  =====================================
   empty_sky           Blank sky (for sky / dark frames)
   flat_field          WCU lamp flat
   star_field          Fixed random 20-star field
   star_sky1           25-star sky field (calibration set 1)
   star_sky2           25-star sky field (calibration set 2)
   calib_star          Single centred point source
   simple_gal          Elliptical galaxy (SED + morphology)
   simple_gal1         Elliptical galaxy (variant)
   pinhole_mask        WCU pinhole mask
   laser_spectrum_lm   WCU laser spectrum, LM band
   laser_spectrum_n    WCU laser spectrum, N band
   =================  =====================================

``properties`` (required)
   Observation parameters:

   ``dit`` *(float)*
      Detector integration time in seconds.

   ``ndit`` *(int)*
      Number of integrations per exposure.

   ``filter_name`` *(str)*
      Filter wheel selection. Common values:

      * LM band: ``Lp``, ``short-L``, ``Mp``, ``L_spec``, ``M_spec``,
        ``HCI_L_short``, ``HCI_L_long``, ``HCI_M``, ``Br_alpha``,
        ``PAH_3.3``, ``CO_1-0_ice``, ``H2O-ice``, ``IB_4.05``, ``open``,
        ``closed``
      * N band: ``N1``, ``N2``, ``N3``, ``N_spec``, ``PAH_8.6``,
        ``PAH_11.25``, ``Ne_II``, ``S_IV``, ``open``, ``closed``

   ``ndfilter_name`` *(str, optional)*
      Neutral density filter: ``open``, ``ND_OD1`` ... ``ND_OD5``.

   ``catg`` *(str)*
      DPR category: ``SCIENCE``, ``CALIB``, or ``TECHNICAL``.

   ``tech`` *(str)*
      DPR technique: ``IMAGE,LM``, ``IMAGE,N``, ``LMS``, ``LSS,LM``,
      ``LSS,N``, ``PUP,M``, ``PUP,N``, ``APP,LM``, ``RAVC,LM``,
      ``RAVC,IFU``.

   ``type`` *(str)*
      DPR type: ``OBJECT``, ``SKY``, ``STD``, ``DARK``, ``FLAT,LAMP``,
      ``FLAT,TWILIGHT``, ``DETLIN``, ``DISTORTION``, ``WAVE``,
      ``PSF,OFFAXIS``, ``PUPIL``, ``CHOPHOME``, ``DARK,WCUOFF``,
      ``SLITLOSS``, ``PERSIST``.

   ``nObs`` *(int)*
      How many exposures of this template to generate.

   ``dateobs`` *(str, optional)*
      Explicit date in ``YYYY-MM-DD HH:MM:SS`` format. Only used when
      ``sequence=False``.

   ``tplname`` *(str, optional)*
      ESO template name string for the FITS header.

``wcu`` (optional)
   Wavefront Control Unit parameters for internal calibrations:

   .. code-block:: yaml

      wcu:
        current_lamp: "bb"          # bb (blackbody) or laser
        current_fpmask: "open"      # open, grid_lm, grid_n
        bb_aperture: 0.5            # blackbody aperture size
        bb_temp: 8000               # blackbody temperature (K)
        is_temp: 300                # integrating sphere temperature
        wcu_temp: 300               # WCU enclosure temperature
        xshift: 0                   # pinhole mask X offset
        yshift: 0                   # pinhole mask Y offset


Adding a New Source
-------------------

Sources are defined in ``Simulations/python/sources.py``. Each source is a
function that returns a ScopeSim-compatible source object.

Example -- adding a bright point source:

.. code-block:: python

   def bright_star(**kwargs):
       """Single bright star at field centre."""
       return sim_tp.star(
           flux=1e4,        # photons/s/m2
           filter_curve="Ks",
           spec_type="A0V",
       )

After adding the function, you can reference it in YAML templates:

.. code-block:: yaml

   source:
     name: bright_star
     kwargs: {}


Creating a Small Variant
-------------------------

For CI testing, create a ``_small.py`` variant of your script that sets
``small=True``. This generates 32x32 pixel images that run quickly:

.. code-block:: python

   # myWorkflow_small.py
   import runSimulationBlock as rs

   if __name__ == "__main__":

       params = {
           "outputDir":  "output/myWorkflow",
           "small":      True,         # <-- small images
           "doStatic":   True,
           "doCalib":    1,            # fewer calibrations
           "sequence":   True,
           "startMJD":   "2027-03-15 00:00:00",
           "calibFile":  None,
           "nCores":     4,
           "testRun":    False,
       }

       yamlFiles = [
           "YAML/scienceLM.yaml",
           "YAML/stdLM.yaml",
       ]

       rs.runSimulationBlock(yamlFiles, params)

Then add a call to it in ``testAll.py`` so CI picks it up.


Tips
----

* **Reuse existing YAML files** where possible. Most calibration templates
  (darks, detector linearity, distortion) are shared across workflows.
* **Start with a copy** of the most similar existing workflow and modify it.
* **Use** ``testRun=True`` to validate your YAML files without running ScopeSim.
* **Use** ``small=True`` during development to iterate quickly.
* The ``doCalib`` mechanism inspects your templates and auto-generates matching
  darks and flats -- you rarely need to write dark/flat YAML by hand.
* Run ``python/generateSummary.py output/myWorkflow`` after a run to get a
  CSV summary of all generated FITS files.
