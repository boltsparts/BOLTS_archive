BOLTS
=====

BOLTS is an Open Library for Technical Specifications.

This repository contains all the tools and data that are required to build the
different distributions and the website. You only need to get the content of
this repository if you want to contribute content to BOLTS or want to develop
the tools that are used to manage it.

**If you just want to use BOLTS, then you should get the BOLTS distribution
for the CAD tool of your choice from the**
`download section <http://jreinhardt.github.io/BOLTS/downloads.html>`_
**of the webpage instead. Instructions on how to use the distributions can be
found in the**
`documentation section <http://jreinhardt.github.io/BOLTS/doc/index.html>`_.

The webpage contains a lot of general infos, an overview over the
`specifications <http://jreinhardt.github.io/BOLTS/html/index.html>`_ of all
parts contained in BOLTS and quite a bit of
`documentation <http://jreinhardt.github.io/BOLTS/doc/index.html>`_.
So if you have more questions, the chances to find answers on the webpage

http://jreinhardt.github.io/BOLTS/index.html

are much higher than to find them here.


Development
===========

The git version of BOLTS uses submodules, so after cloning, you will need to run

git submodule init
git submodule update

to get the correct states for the submodules. For more informations about
submodules, see http://git-scm.com/book/en/Git-Tools-Submodules.

Dependencies
============

To use BOLTS for OpenSCAD

* OpenSCAD (http://www.openscad.org/)

is required.

To use BOLTS for FreeCAD

* FreeCAD (http://freecadweb.org/)
* python 2.6
* pyyaml (http://pyyaml.org/)
* importlib (https://pypi.python.org/pypi/importlib/1.0.2) (only for python 2.6)

is required.

To run the  bolts.py utility script (for development)

* python 2.7 (because of argparse)
* pyyaml (http://pyyaml.org/)

is required.
