FITS Wrangler
=============

The ``fitsWrangler/`` directory contains a standalone utility library for
creating and reformatting FITS files into formats compatible with the METIS
pipeline. It is **largely superseded** by the main simulation framework in
``Simulations/``, but is kept for reference and may still be useful for
one-off file manipulation tasks.

.. note::

   For new simulation work, use the ``Simulations/`` framework instead.
   The fitsWrangler is retained as a lower-level utility for cases where you
   need to build FITS files by hand, outside of the ScopeSim pipeline.


Purpose
-------

The fitsWrangler decouples the *format* of METIS FITS files from the code
that *generates* the pixel data. It can:

* Create minimal, empty FITS files with the correct extensions and header
  keywords for any METIS pipeline recipe.
* Take ScopeSim output (or any other source), copy data and headers, add
  ESO-compliant extension names and ``HDUCLASS`` keywords, and write a new
  file.
* Take data and headers from multiple sources, combine them, and produce a
  single pipeline-compliant FITS file.
* Create *processed* FITS files with science, error, and quality extensions.


Module Reference
----------------

The module lives at ``fitsWrangler/fitsWrangler.py`` and exposes three
functions.


``makeBasicParameters(mode, instrument)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a parameter structure that describes the FITS file to be produced.
This structure is passed to ``createImage()`` to actually write the file.

**Arguments:**

``mode`` *(str)* -- one of:

.. list-table::
   :widths: 20 80

   * - ``"raw"``
     - Raw data: one science extension per detector.
   * - ``"processed"``
     - Processed data: science + error + quality extensions per detector.

``instrument`` *(str)* -- one of:

.. list-table::
   :widths: 20 20 60

   * - ``"lm"``
     - 2048x2048
     - Single 2D image (LM-band detector).
   * - ``"n"``
     - 2048x2048
     - Single 2D image (N-band detector).
   * - ``"lss"``
     - 2048x2048
     - Single 2D spectral image (long-slit).
   * - ``"ifu"``
     - 2048x2048
     - Four 2D images (one per IFU detector).
   * - ``"ifu_cube"``
     - 2048x2048x500
     - Four 3D cubes (one per IFU detector).
   * - ``"lss_spectrum"``
     - 2048
     - Single 1D spectrum.

**Returns:** a ``dict`` with the following structure::

   parms = {
       "instrument":  [str, ...],    # detector name(s)
       "defaultSize": [int, ...],    # numpy array shape for empty data
       "primary": {
           "header":   None or fits.Header,
           "keywords": None or dict,
       },
       "data": [                     # list of 1 (imaging) or 4 (IFU)
           {
               "data":     None or np.ndarray,
               "header":   None or fits.Header,
               "keywords": None or dict,
           },
           ...
       ],
       "error":   None or [...],     # same structure as data (processed only)
       "quality": None or [...],     # same structure as data (processed only)
   }

For **raw** mode, ``error`` and ``quality`` are ``None``.
For **processed** mode, they mirror the ``data`` list.


``createImage(outFile, parms)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Write a FITS file to disk based on the parameter structure.

**Arguments:**

* ``outFile`` *(str)* -- output file path.
* ``parms`` *(dict)* -- parameter structure from ``makeBasicParameters()``,
  optionally modified.

**Behaviour:**

1. Creates a ``PrimaryHDU`` and applies headers/keywords from
   ``parms["primary"]``.
2. For each entry in ``parms["data"]``:

   a. If ``data`` is ``None``, creates a zero-filled array of shape
      ``parms["defaultSize"]``.
   b. Otherwise uses the provided numpy array.
   c. Copies any provided header, then applies keyword overrides.
   d. Forces ESO-compliant extension metadata (see
      :ref:`extension-keywords` below).

3. For processed files (``error`` and ``quality`` not ``None``), appends
   matching error and quality extensions with appropriate ``HDUCLASS``
   values.
4. Writes the assembled ``HDUList`` to ``outFile``, overwriting if it exists.


``updateHeader(HDU, parms)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Internal helper. Copies keywords from a provided header, then overlays any
keywords from the ``keywords`` dict onto the HDU.

**Arguments:**

* ``HDU`` -- an ``astropy.io.fits`` HDU object.
* ``parms`` *(dict)* -- a single entry from the parameter structure
  (e.g. ``parms["data"][0]``), containing ``header`` and ``keywords`` fields.


.. _extension-keywords:

Extension Keywords Set by fitsWrangler
--------------------------------------

``createImage()`` forces the following keywords on every image extension it
writes, ensuring the output conforms to the ESO FITS standard for METIS:

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Keyword
     - Example value
     - Description
   * - ``EXTNAME``
     - ``lm.sci``
     - Extension name, format ``{instrument}.sci``.
   * - ``HDUCLAS1``
     - ``IMAGE``
     - HDU class: always ``IMAGE``.
   * - ``HDUCLAS2``
     - ``DATA``
     - Flavour of the extension: ``DATA``, ``ERROR``, or ``QUALITY``.
   * - ``HDUCLAS3``
     - *(empty)*
     - Sub-flavour. Set to ``RMSE`` for error extensions, ``FLAG32BIT`` for
       quality extensions, empty for data extensions.

For **processed** files, the additional error and quality extensions use:

.. list-table::
   :header-rows: 1
   :widths: 15 25 25 35

   * - Extension
     - ``HDUCLAS2``
     - ``HDUCLAS3``
     - ``EXTNAME``
   * - Science
     - ``DATA``
     - *(empty)*
     - ``{instrument}.sci``
   * - Error
     - ``ERROR``
     - ``RMSE``
     - ``{instrument}.err``
   * - Quality
     - ``QUALITY``
     - ``FLAG32BIT``
     - ``{instrument}.dq``


.. _fits-keyword-reference:

Complete FITS Keyword Reference
-------------------------------

This section catalogues **every FITS header keyword** referenced across the
simulation framework -- both in the fitsWrangler and in the main
``Simulations/`` code.  Keywords use the ESO HIERARCH convention where the
full HIERARCH path is shown; aliases (shorthand names used in YAML templates
or internally) are noted.

Observation Metadata
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - FITS Keyword
     - YAML / Internal Alias
     - Description
   * - ``MJD-OBS``
     - ``MJD-OBS``
     - Modified Julian Date of the observation. Written by
       ``setupSimulations.updateHeaders()``.
   * - ``INSTRUME``
     - --
     - Instrument name (``METIS``). Set in static calibration files.
   * - ``OBJECT``
     - --
     - Target name. Set in static calibration files.
   * - ``RA``
     - --
     - Right ascension of target.
   * - ``DEC``
     - --
     - Declination of target.

Data Product Classification (DPR)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These keywords classify every FITS file by category, technique, and type.
They are the primary keywords used by the ESO Data Processing System (EDPS)
to route files to the correct pipeline recipe.

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - FITS Keyword
     - YAML Alias
     - Description
   * - ``HIERARCH ESO DPR CATG``
     - ``catg``
     - Data product category. Values: ``SCIENCE``, ``CALIB``, ``TECHNICAL``.
   * - ``HIERARCH ESO DPR TECH``
     - ``tech``
     - Observation technique. Values: ``IMAGE,LM``, ``IMAGE,N``, ``IFU``,
       ``LSS,LM``, ``LSS,N``, ``PUP,LM``, ``PUP,N``, ``APP,LM``,
       ``RAVC,LM``, ``RAVC,IFU``. Note: the internal alias ``LMS`` is
       rewritten to ``IFU`` by ``updateHeaders()``.
   * - ``HIERARCH ESO DPR TYPE``
     - ``type``
     - Observation type. Values: ``OBJECT``, ``SKY``, ``STD``, ``DARK``,
       ``DARK,WCUOFF``, ``FLAT,LAMP``, ``FLAT,TWILIGHT``, ``DETLIN``,
       ``DISTORTION``, ``WAVE``, ``PSF,OFFAXIS``, ``PUPIL``, ``CHOPHOME``,
       ``SLITLOSS``, ``PERSIST``.

Instrument Configuration (INS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - FITS Keyword
     - YAML Alias
     - Description
   * - ``HIERARCH ESO INS MODE``
     - --
     - Instrument mode string. Derived from ``tech`` by
       ``updateHeaders()``. See the tech-to-mode mapping table below.
   * - ``HIERARCH ESO INS OPTI1 NAME``
     - --
     - Optical element 1 (apodizer). Set for HCI modes (e.g. ``RAP-LM``).
   * - ``HIERARCH ESO INS OPTI3 NAME``
     - --
     - Optical element 3 (vortex / slit). Set for HCI and LSS modes. For
       LSS, contains the slit name.
   * - ``HIERARCH ESO INS OPTI5 NAME``
     - --
     - Optical element 5 (Lyot stop / APP). Set for HCI modes
       (e.g. ``RLS-LMS``, ``APP-LMS``).
   * - ``HIERARCH ESO INS OPTI6 NAME``
     - --
     - Optical element 6 (IFU filter). Set for RAVC IFU mode.
   * - ``HIERARCH ESO INS OPTI15 NAME``
     - --
     - Optical element 15 (pupil mask). Set for pupil imaging modes
       (``PUPIL1`` for LM, ``PUPIL2`` for N).

.. _ins-mode-mapping:

The ``tech`` to ``INS MODE`` mapping applied by ``updateHeaders()``:

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - ``tech`` value
     - ``INS MODE`` value
     - Notes
   * - ``IMAGE,LM``
     - ``IMG_LM``
     -
   * - ``IMAGE,N``
     - ``IMG_N``
     -
   * - ``LSS,LM``
     - ``SPEC_LM``
     -
   * - ``LSS,N``
     - ``SPEC_N_LOW``
     -
   * - ``LMS``
     - ``IFU_nominal``
     - ``DPR TECH`` also rewritten to ``IFU``
   * - ``RAVC,LM``
     - ``IMG_LM_RAVC``
     - ``DPR TECH`` rewritten to ``IMAGE,LM``
   * - ``APP,LM``
     - ``IMG_LM_APP``
     - ``DPR TECH`` rewritten to ``IMAGE,LM``
   * - ``RAVC,IFU``
     - ``IFU_nominal_RAVC``
     - ``DPR TECH`` rewritten to ``IFU``
   * - ``PUP,LM``
     - ``IMG_LM``
     -
   * - ``PUP,N``
     - ``IMG_N``
     -

Derived Keywords (DRS)
^^^^^^^^^^^^^^^^^^^^^^

DRS keywords are *derived aliases* used by the EDPS to match and organise
files without parsing complex HIERARCH trees. They are set by ScopeSim and/or
``updateHeaders()``.

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - FITS Keyword
     - YAML Alias
     - Description
   * - ``HIERARCH ESO DRS FILTER``
     - ``filter_name``
     - Active filter name (e.g. ``Lp``, ``N2``, ``open``).
   * - ``HIERARCH ESO DRS NDFILTER``
     - ``ndfilter_name``
     - Active ND filter (e.g. ``open``, ``ND_OD1`` ... ``ND_OD5``).
   * - ``HIERARCH ESO DRS SLIT``
     - ``slit_name``
     - Slit identifier for LSS modes. Copied from ``INS OPTI3 NAME`` by
       ``updateHeaders()`` for LSS,LM and LSS,N.
   * - ``HIERARCH ESO DRS IFU``
     - --
     - IFU filter/grating. Set for IFU and RAVC,IFU modes by
       ``updateHeaders()``.
   * - ``HIERARCH ESO DRS MASK``
     - --
     - Coronagraph mask string. Composite value set for HCI modes, e.g.
       ``VPM-L,RAP-LM,RLS-LMS`` (RAVC) or ``VPM-L,RAP-LM,APP-LMS`` (APP).

Detector Keywords (DET)
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - FITS Keyword
     - YAML Alias
     - Description
   * - ``HIERARCH ESO DET DIT``
     - ``dit``
     - Detector integration time in seconds (float).
   * - ``HIERARCH ESO DET NDIT``
     - ``ndit``
     - Number of integrations per exposure (int).

Observation Block / Template Keywords
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - FITS Keyword
     - YAML / Internal Alias
     - Description
   * - ``HIERARCH ESO OBS TPLNAME``
     - ``tplname``
     - Template name (e.g. ``METIS_img_lm_obs``).
   * - ``HIERARCH ESO OBS TPLEXPNO``
     - ``tplexpno``
     - Exposure number within the template (auto-incremented).
   * - ``HIERARCH ESO OBS TPLSTART``
     - ``tplstart``
     - Start time of the template.

WCU / Sequence Keywords
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - FITS Keyword
     - YAML Alias
     - Description
   * - ``HIERARCH ESO SEQ WCU LASER1 NAME``
     - --
     - Set to ``LASER1`` for wavelength calibration frames
       (``DPR TYPE = WAVE``).

Product Classification (PRO) -- Static Calibrations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These keywords appear in the static calibration files generated by
``makeCalibPrototypes.py``. ``PRO CATG`` identifies the product; ``PRO TECH``
and ``PRO TYPE`` further classify it.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ``PRO CATG`` Value
     - Description
   * - ``REF_STD_CAT``
     - Reference standard star spectrum catalogue.
   * - ``FLUXSTD_CATALOG``
     - Multi-star flux standard catalogue.
   * - ``LM_SYNTH_TRANS``
     - Synthetic transmission curve (LM band).
   * - ``N_SYNTH_TRANS``
     - Synthetic transmission curve (N band).
   * - ``AO_PSF_MODEL``
     - Adaptive optics PSF model (30x30 image).
   * - ``ATM_LINE_CAT``
     - Atmospheric line catalogue (HITRAN-based).
   * - ``ATM_PROFILE``
     - Atmospheric profile (height, pressure, temperature, molecular
       mixing ratios).
   * - ``LM_LSS_DIST_SOL``
     - LM-band distortion solution (polynomial coefficients).
   * - ``N_LSS_DIST_SOL``
     - N-band distortion solution (polynomial coefficients).
   * - ``LM_LSS_WAVE_GUESS``
     - LM-band initial wavelength guess (polynomial coefficients).
   * - ``N_LSS_WAVE_GUESS``
     - N-band initial wavelength guess (polynomial coefficients).
   * - ``LSF_KERNEL``
     - Line Spread Function kernel (pixel vs intensity).
   * - ``LASER_TAB``
     - WCU laser frequency table.
   * - ``PINHOLE_TABLE``
     - WCU pinhole mask position table (x, y).
   * - ``PERSISTENCE_MAP``
     - Detector persistence map (per-band: LM, N, IFU).

Additional static calibration keywords on persistence map files:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Keyword
     - Example / Description
   * - ``HIERARCH ESO PRO TECH``
     - ``IMAGE,LM``, ``IMAGE,N``, or ``LMS``.
   * - ``HIERARCH ESO PRO TYPE``
     - ``PERSISTENCE`` or ``REDUCED``.
   * - ``HIERARCH ESO INS MODE``
     - ``img_lm``, ``img_n``, or ``Nominal``.
   * - ``HIERARCH ESO DRS FILTER``
     - ``OPEN``.
   * - ``HIERARCH ESO DRS NDFILTER``
     - ``OPEN``.

HDU Extension Keywords (all files)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Keyword
     - Description
   * - ``EXTNAME``
     - Extension name. For raw: ``{instrument}.sci``. For processed:
       ``.sci``, ``.err``, ``.dq``. For static calibrations: the product
       name or ``DETn.DATA`` (IFU persistence).
   * - ``HDUCLAS1``
     - Always ``IMAGE``.
   * - ``HDUCLAS2``
     - ``DATA``, ``ERROR``, or ``QUALITY``.
   * - ``HDUCLAS3``
     - Empty, ``RMSE`` (error), or ``FLAG32BIT`` (quality).

DO Category (``do.catg``)
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``do.catg`` field in YAML templates maps to the output filename prefix and
is used to classify raw data files. It is not a FITS keyword itself but
determines the filename pattern ``METIS.{do.catg}.{date}.fits``. See
:doc:`workflows` for a complete list of DO categories per workflow.


Usage Examples
--------------

Creating an empty LM raw image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from fitsWrangler import fitsWrangler as fw

   parms = fw.makeBasicParameters("raw", "lm")
   parms["data"][0]["keywords"]["filter"] = "Mp"
   fw.createImage("lm_empty.fits", parms)

Converting ScopeSim output
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from astropy.io import fits
   from fitsWrangler import fitsWrangler as fw

   hdul = fits.open("scopesim_output.fits")

   parms = fw.makeBasicParameters("raw", "lss")
   parms["primary"]["header"] = hdul[0].header
   parms["data"][0]["header"] = hdul[1].header
   parms["data"][0]["data"] = hdul[1].data

   fw.createImage("lss_raw.fits", parms)

Creating a processed file with error and quality
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import numpy as np
   from astropy.io import fits
   from fitsWrangler import fitsWrangler as fw

   hdul = fits.open("scopesim_output.fits")

   parms = fw.makeBasicParameters("processed", "lss")
   parms["primary"]["header"] = hdul[0].header

   parms["data"][0]["header"] = hdul[1].header
   parms["data"][0]["data"] = hdul[1].data

   parms["error"][0]["header"] = hdul[1].header
   parms["error"][0]["data"] = np.sqrt(np.abs(hdul[1].data))

   parms["quality"][0]["header"] = hdul[1].header
   parms["quality"][0]["data"] = (hdul[1].data * 0.0 + 1).astype(int)

   fw.createImage("lss_processed.fits", parms)
