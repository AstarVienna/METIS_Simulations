Repository Structure
====================

This page gives a high-level overview of how the METIS Simulations repository
is organised, what each module does, and how data flows through the system.

Directory Layout
----------------

::

   METIS_Simulations/
   ├── .github/workflows/          CI pipelines (daily build + PR checks)
   ├── docs/                       This documentation (Sphinx / ReadTheDocs)
   ├── fitsWrangler/               Legacy FITS manipulation utilities (kept for reference)
   ├── ScienceCases/               Notebooks for science-case prototyping
   ├── Simulations/                Main simulation framework
   │   ├── python/                 All Python source code
   │   ├── YAML/                   Observation template definitions (~40 files)
   │   ├── sofFiles/               Set-of-frames files for pipeline recipes
   │   ├── sofTemplates/           SOF file templates
   │   ├── runESO.sh               Full ESO production run (all modes)
   │   └── runESOsmall.sh          Small/CI run (32x32 px images)
   ├── pyproject.toml              Poetry project & dependency definition
   └── README.md


The ``Simulations/`` Directory
------------------------------

Almost all relevant code lives under ``Simulations/``.

``Simulations/python/`` -- Python Modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Core framework
""""""""""""""

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Purpose
   * - ``setupSimulations.py``
     - Central orchestrator. Loads YAML templates, runs ScopeSim for each
       template, generates calibrations, and post-processes FITS headers.
   * - ``scopesimWrapper.py``
     - Thin wrapper around ScopeSim. Configures ``UserCommands``,
       ``OpticalTrain``, sources, and calls ``observe()`` / ``readout()``.
   * - ``simulationDefinitions.py``
     - Defines valid parameter values (categories, technologies, types, modes,
       filters, ND filters) and calibration frame templates.
   * - ``sources.py``
     - Catalogue of astronomical and calibration sources (star fields,
       galaxies, flat fields, pinhole mask, laser spectra, etc.).
   * - ``runSimulationBlock.py``
     - High-level function that runs a list of YAML files in sequence with
       shared parameters and sequential timestamps.
   * - ``makeCalibPrototypes.py``
     - Generates prototype FITS files for static/external calibrations
       (pinhole table, laser table, distortion solution, etc.).

Simulation block scripts
""""""""""""""""""""""""

Each script defines a complete *simulation block* -- the set of YAML files and
parameters needed to produce all raw + calibration files for a given instrument
mode. See :doc:`workflows` for details.

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Script
     - Small variant
     - Mode
   * - ``imgLM.py``
     - ``imgLM_small.py``
     - LM-band imaging
   * - ``imgN.py``
     - ``imgN_small.py``
     - N-band imaging
   * - ``lssLM.py``
     - ``lssLM_small.py``
     - LM-band long-slit spectroscopy
   * - ``lssN.py``
     - ``lssN_small.py``
     - N-band long-slit spectroscopy
   * - ``ifu.py``
     - ``ifu_small.py``
     - IFU (LMS) spectroscopy
   * - ``calib.py``
     - ``calib_small.py``
     - Standalone calibrations (chopper home, pupil, slit loss)
   * - ``hciRavcLM.py``
     - ``hciRavcLM_small.py``
     - High-contrast imaging -- RAVC coronagraph (LM)
   * - ``hciAppLm.py``
     - ``hciAppLm_small.py``
     - High-contrast imaging -- APP coronagraph (LM)
   * - ``hciRavcIfu.py``
     - ``hciRavcIfu_small.py``
     - High-contrast imaging -- RAVC coronagraph (IFU)

Utilities
"""""""""

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Purpose
   * - ``testAll.py``
     - CI entry-point: runs every ``*_small.py`` block.
   * - ``generateSummary.py``
     - Extracts a CSV summary from generated FITS files.
   * - ``check_headers.py``
     - Validates FITS header keywords.
   * - ``check_sof_files.py``
     - Validates SOF file contents.
   * - ``downloadPackages.py``
     - Downloads IRDB instrument data packages.
   * - ``makeSOF.py``
     - Generates SOF files from simulation output.
   * - ``grabHeaders.py``
     - Extracts headers from existing FITS files.

``Simulations/YAML/`` -- Observation Templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each YAML file defines one or more observation templates. Templates are grouped
by purpose:

**Science observations** -- ``scienceLM.yaml``, ``scienceN.yaml``,
``scienceLSSLM.yaml``, ``scienceLSSN.yaml``, ``scienceIFU.yaml``

**Standard stars** -- ``stdLM.yaml``, ``stdN.yaml``, ``stdLSSLM.yaml``,
``stdLSSN.yaml``, ``stdIFU.yaml``

**Detector calibrations** -- ``detlinLM.yaml``, ``detlinN.yaml``,
``detlinIFU.yaml`` (linearity); ``darkLM.yaml``, ``darkN.yaml``,
``darkIFU.yaml`` (darks)

**Flat fields** -- ``flatLampLM.yaml``, ``flatLampN.yaml``,
``flatTwilightLM.yaml``, ``flatTwilightN.yaml``

**Spectral response** -- ``rsrfLSSLM.yaml``, ``rsrfLSSN.yaml``,
``rsrfIFU.yaml``, ``rsrfPinhLSSLM.yaml``, ``rsrfPinhLSSN.yaml``,
``rsrfPinhIFU.yaml``

**Wavelength calibration** -- ``wavecalLSSLM.yaml``, ``wavecalLSSN.yaml``,
``wavecalIFU.yaml``

**Distortion** -- ``distortionLM.yaml``, ``distortionN.yaml``,
``distortionIFU.yaml``

**High-contrast imaging** -- ``hciRavcLM.yaml``, ``hciAppLM.yaml``,
``hciRavcIfu.yaml``, ``offAxisLM.yaml``

**Technical** -- ``chophomeLM.yaml``, ``pupilLM.yaml``, ``pupilN.yaml``,
``slitlossLSSLM.yaml``, ``slitlossLSSN.yaml``, ``persistLM.yaml``, etc.


Data Flow
---------

The following diagram shows how data moves through the framework, from YAML
templates to final FITS output::

   YAML template files
         │
         ▼
   setupSimulations.loadYAML()      parse & validate templates
         │
         ▼
   simulationDefinitions            check valid parameter values
         │
         ▼
   scopesimWrapper.simulate()       configure & run ScopeSim
         │
         ├──▶ sources.py            look up source definition
         ├──▶ ScopeSim OpticalTrain
         └──▶ METIS IRDB            instrument reference data
         │
         ▼
   Raw FITS files                   direct ScopeSim output
         │
         ▼
   setupSimulations.updateHeaders() add/fix ESO-compliant keywords
         │
         ▼
   makeCalibPrototypes              generate static calibration files
         │
         ▼
   Final FITS output                ready for pipeline recipes

Key concepts:

1. **Observation template** -- a single YAML block describing one type of
   observation (e.g. a science exposure, a dark frame, a flat field).
2. **Simulation block** -- a Python script that bundles several YAML files and
   a parameter dict into a self-contained dataset for one instrument mode.
3. **Static calibrations** -- external calibration FITS files (pinhole table,
   laser table, distortion solution, etc.) generated by
   ``makeCalibPrototypes.py``.
4. **Sequential timestamps** -- when ``sequence=True``, each exposure in a
   block gets a unique, incrementing ``MJD-OBS`` to mimic a real observing
   night.


Dependencies
------------

The framework depends on the ScopeSim simulation stack:

* `ScopeSim <https://github.com/AstarVienna/ScopeSim>`_ -- core optical
  simulation engine.
* `ScopeSim_Templates <https://github.com/AstarVienna/ScopeSim_Templates>`_ --
  pre-built source templates.
* `IRDB <https://github.com/AstarVienna/irdb>`_ -- Instrument Reference
  Database containing the METIS instrument model.

Plus standard astronomy Python packages: ``numpy``, ``astropy``,
``matplotlib``, ``astar-utils``.


CI / Automation
---------------

Two GitHub Actions workflows exist:

``run_recipes.yml``
   Triggered on PRs and pushes to ``main``. Runs ``testAll.py`` which
   executes every simulation block in *small* mode (32x32 px images) to verify
   ScopeSim integration.

``daily_build.yaml``
   Nightly build on a self-hosted runner. Runs the full ``runESO.sh``
   production script and archives output to ``/data/<date>/``.
