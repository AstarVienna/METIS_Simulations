METIS Simulations
=================

**METIS Simulations** is a Python framework for generating simulated
`METIS <https://elt.eso.org/instrument/METIS/>`_ instrument data using
`ScopeSim <https://scopesim.readthedocs.io/>`_.
It produces realistic FITS files with ESO-compliant headers and formats for
pipeline development and testing.

.. important::

   The generated files contain instrumentally and scientifically
   **approximate** data. They are intended for pipeline development, not for
   evaluating METIS instrument performance.

Use cases:

* Generate test data for METIS pipeline (METIS-PIP) development and validation.
* Create self-contained simulation blocks with science, calibration, and static
  calibration files.
* Run nightly CI builds to verify ScopeSim integration.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   structure
   workflows
   writing_workflows
   fitswrangler
