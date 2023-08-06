
**pPXF: Full Spectrum and SED Fitting of Galactic and Stellar Spectra**

.. image:: http://www-astro.physics.ox.ac.uk/~cappellari/software/ppxf_logo.svg
    :target: https://www-astro.physics.ox.ac.uk/~cappellari/software/#ppxf
    :width: 100
.. image:: https://img.shields.io/pypi/v/ppxf.svg
    :target: https://pypi.org/project/ppxf/
.. image:: https://img.shields.io/badge/arXiv-1607.08538-orange.svg
    :target: https://arxiv.org/abs/1607.08538
.. image:: https://img.shields.io/badge/DOI-10.1093/mnras/stw3020-green.svg
        :target: https://doi.org/10.1093/mnras/stw3020

This ``pPXF`` package contains a Python implementation of the Penalized
PiXel-Fitting (``pPXF``) method to fit the stellar and gas kinematics,
as well as the stellar population and the photometry (SED) of galaxies.
The method was originally described in `Cappellari & Emsellem (2004)
<https://ui.adsabs.harvard.edu/abs/2004PASP..116..138C>`_
and was substantially upgraded in subsequent years and particularly in
`Cappellari (2017) <https://ui.adsabs.harvard.edu/abs/2017MNRAS.466..798C>`_.

.. contents:: :depth: 1

Attribution
-----------

If you use this software for your research, please cite at least
`Cappellari (2017) <https://ui.adsabs.harvard.edu/abs/2017MNRAS.466..798C>`_,
or both ``pPXF`` papers above.
The BibTeX entry for the paper is::

    @ARTICLE{Cappellari2017,
        author = {{Cappellari}, M.},
        title = "{Improving the full spectrum fitting method:
            accurate convolution with Gauss-Hermite functions}",
        journal = {MNRAS},
        eprint = {1607.08538},
        year = 2017,
        volume = 466,
        pages = {798-811},
        doi = {10.1093/mnras/stw3020}
    }

Installation
------------

install with::

    pip install ppxf

Without write access to the global ``site-packages`` directory, use::

    pip install --user ppxf

To upgrade ``pPXF`` to the latest version use::

    pip install --upgrade ppxf

Usage Examples
--------------

To learn how to use the ``pPXF`` package, copy, modify and run
the example programs in the ``ppxf/examples`` directory. 
It can be found within the main ``ppxf`` package installation folder 
inside `site-packages <https://stackoverflow.com/a/46071447>`_. 
The detailed documentation is contained in the docstring of the file 
``ppxf.py``, or on `PyPi <https://pypi.org/project/ppxf/>`_ or as PDF 
from `<https://purl.org/cappellari/software>`_.

.. image:: http://www-astro.physics.ox.ac.uk/~cappellari/software/jupyter_logo.svg
    :target: https://github.com/micappe/ppxf_examples
    :width: 100
    :alt: Jupyter Notebook

Examples as `Jupyter Notebooks <https://jupyter.org/>`_ are also available
on my `GitHub repository <https://github.com/micappe/ppxf_examples>`_.

###########################################################################
