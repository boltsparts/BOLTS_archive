Important Information
=====================

The repository was renamed a new repository was created. For the new repository
some not needed data was stripped and the history rewritten. Reposize went down
from 166 MB to 46 MB. See https://github.com/boltsparts/BOLTS_archive/issues/163
and https://github.com/boltsparts/boltsparts

BOLTS
=====

BOLTS is an Open Library for Technical Specifications.

This repository contains all the tools and data that are required to build the
different distributions and the website. You only need to get the content of
this repository if you want to contribute content to BOLTS or want to develop
the tools that are used to manage it.

**If you just want to use BOLTS, then you should get the BOLTS distribution
for the CAD tool of your choice from the**
`download section <https://boltsparts.github.io/en/downloads.html>`_
**of the webpage instead. Instructions on how to use the distributions can be
found in the**
`documentation section <https://boltsparts.github.io/en/docs/index.html>`_.

The webpage contains a lot of general infos, a 
`list of all parts <https://boltsparts.github.io/en/parts/index.html>`_ 
contained in BOLTS and quite a bit of
`documentation <https://boltsparts.github.io/en/docs/index.html>`_.
So if you have more questions, the chances to find answers on the webpage

https://boltsparts.github.io

are much higher than to find them here.

Use
===

You should check out the 
`documentation <https://boltsparts.github.io/en/docs/index.html>`_.
on the `webpage <https://boltsparts.github.io/>`_ for more information on how
to get and use BOLTS.

Dependencies for use
--------------------

To use BOLTS for OpenSCAD

* OpenSCAD (http://www.openscad.org/)

is required.

To use BOLTS for FreeCAD

* FreeCAD (http://freecadweb.org/)
* python 3.6
* pyyaml (http://pyyaml.org/)
* importlib (https://pypi.python.org/pypi/importlib/1.0.2) (only for python 2.6)

is required.

Development
===========

Dependencies for development
----------------------------

In any case you should have

* git
* python 3.6
* pyyaml (http://pyyaml.org/)

installed.

Depending on the target system you want to develop for additional dependencies
are required.

For BOLTS for OpenSCAD:

* OpenSCAD (http://www.openscad.org/)

For BOLTS for FreeCAD

* FreeCAD (http://freecadweb.org/)
* PySide

For BOLTS for SolidWorks

* python-xlwt (http://python-excel.org/)

To work on the website it is recommended to use a virtualenv for the python
dependencies, see
`the documentation <https://boltsparts.github.io/en/docs/index.html>`_ for more
details. If you don't want to use a virtualenv, you can install the python
requirements listed in `requirements.txt`. In addition you need

* node-less
* cleancss

To run the  bolts.py utility script (for development)

* python 3.6
* pyyaml (http://pyyaml.org/)
