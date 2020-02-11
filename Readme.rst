BOLTS
=====

BOLTS is an Open Library for Technical Specifications.

This repository contains all the tools and data that are required to build the
different distributions and the website. You only need to get the content of
this repository if you want to contribute content to BOLTS or want to develop
the tools that are used to manage it.

**If you just want to use BOLTS, then you should get the BOLTS distribution
for the CAD tool of your choice from the**
`download section <http://www.bolts-library.org/en/downloads.html>`_
**of the webpage instead. Instructions on how to use the distributions can be
found in the**
`documentation section <http://www.bolts-library.org/en/docs/index.html>`_.

The webpage contains a lot of general infos, a 
`list of all parts <http://www.bolts-library.org/en/parts/index.html>`_ 
contained in BOLTS and quite a bit of
`documentation <http://www.bolts-library.org/en/docs/index.html>`_.
So if you have more questions, the chances to find answers on the webpage

http://www.bolts-library.org (redirect to https://boltsparts.github.io)

are much higher than to find them here.

Use
===

You should check out the 
`documentation <http://www.bolts-library.org/en/docs/index.html>`_.
on the `webpage <http://www.bolts-library.org/>`_ for more information on how
to get and use BOLTS.

Dependencies for use
--------------------

To use BOLTS for OpenSCAD

* OpenSCAD (http://www.openscad.org/)

is required.

To use BOLTS for FreeCAD

* FreeCAD (http://freecadweb.org/)
* python 2.6 or 2.7 as well as 3.6
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
* PyQt5

For BOLTS for SolidWorks

* python-xlwt (http://python-excel.org/)

To work on the website it is recommended to use a virtualenv for the python
dependencies, see
`the documentation <http://www.bolts-library.org/en/docs/index.html>`_ for more
details. If you don't want to use a virtualenv, you can install the python
requirements listed in `requirements.txt`. In addition you need

* node-less
* cleancss

To run the  bolts.py utility script (for development)

* python 2.7 (because of argparse) or 3.6
* pyyaml (http://pyyaml.org/)
