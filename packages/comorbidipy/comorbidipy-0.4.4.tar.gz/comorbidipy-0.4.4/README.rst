===========
comorbidipy
===========


.. image:: https://img.shields.io/pypi/v/comorbidipy.svg
        :target: https://pypi.python.org/pypi/comorbidipy

.. image:: https://img.shields.io/travis/vvcb/comorbidipy.svg
        :target: https://travis-ci.com/vvcb/comorbidipy

.. image:: https://readthedocs.org/projects/comorbidipy/badge/?version=latest
        :target: https://comorbidipy.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

Python package to calculate comorbidity scores including Charlson Comorbidity Score and Elixhauser Score and their weighted variants as well as other clinical risk scores.

The `comorbidity` function of this library is effectively a rewrite of the excellent R library `comorbidity` (<https://github.com/ellessenne/comorbidity/>) by Alessandro Gasparini (<https://www.ellessenne.xyz/>).
Please check out his work and the excellent documentation he has produced.
The Python API has been modified slightly to allow adjusting for age. 
Only the `comorbidity` function from that library has been reproduced here at present.

Comorbidipy also includes additional clinical risk calculators listed under *Features*.

List of Risk Scores
-------------------

- Charlson Comorbidity index
- Elixhauser index
- Hospital Frailty Risk Score

License and Documentation
-------------------------

* Free software: MIT license
* Documentation: https://comorbidipy.readthedocs.io. (TODO)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
