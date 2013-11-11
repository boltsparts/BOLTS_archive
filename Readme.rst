BOLTS
=====

BOLTS is an Open Library for Technical Specifications.

For more information check the BOLTS webpage:

http://jreinhardt.github.io/BOLTS/index.html

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
