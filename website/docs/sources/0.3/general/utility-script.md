---
  title: How to use a development checkout
  audience: contributors
---

This assumes that you have obtained a git checkout by cloning either the
official BOLTS git or a fork. You need to have python, pyYAML and optionally
FreeCAD and OpenSCAD installed. This tutorial makes heavy use of the
commandline.

There are several tasks that are so common in BOLTS development that they have
been put into a script called bolts.py. This tutorial describes how to use this
script to perform these tasks. Some information about the available subcommands
and options is available by typing

    ./bolts.py --help

### Exporting backends

After making some changes, one might want to rebuild the output of a backend,
so that one can inspect it. This can be done using the `export` subcommand. The
results of this operation can be found in the respective subdirectory of the
output directory.

For example to regenerate the OpenSCAD distribution one uses

    ./bolts.py export openscad

To build a OpenSCAD library that is restricted to content compatible with a
certain license, one can supply an additional argument:

    ./bolts.py export openscad --license lgpl2.1+

One can also regenerate the HTML output, which is useful when creating drawings
or adding new collections

    ./bolts.py export html


### Running automatic checks

BOLTS can run some automatic checks and detect a few common errors, problems
and inconsistencies.

To do so, execute

    ./bolts.py check

A report is displayed with all the problems found and a short explanation.

### Listing tasks

BOLTS can also look for missing bits and pieces and other small jobs that make
BOLTS more complete or consistent.

To show a list of such tasks use

    ./bolts.py tasks

If there are tasks available, they are displayed together with a short
explanation.


### Testing CAD applications

Manual inspection and automatic checks are good, but some errors can only be
found when working in the CAD application. The utility script allows to fire up
instances of OpenSCAD or FreeCAD with all necessary paths setup such that one
can test freshly exported distributions.

This is done with the `test` subcommand. To test for FreeCAD type

    ./bolts.py export freecad
    ./bolts.py test freecad

This exports a FreeCAD distribution and starts an instance of FreeCAD with the
module search paths set up correctly. You can now start BOLTS by typing

    import BOLTS

into the FreeCAD Python console and then test your changes.

To test for OpenSCAD type

    ./bolts.py export openscad
    ./bolts.py test openscad

This exports a OpenSCAD distribution and starts an instance of OpenSCAD so that
it finds the exported distribution. You can now include BOLTS by entering

    include <BOLTS.scad>;

in the editor. It should now be possible to invoke BOLTS modules to test
whether everything works.

### Creating releases

The utility script also automates the process of preparing archives of released
versions of BOLTS, by using the `release` subcommand. This is usually only used
by the maintainer.
