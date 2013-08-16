BLT Format 0.1
##############

A BOLT library consists of a directory containing a number of mandatory and optional subdirectories. The mandatory ones are

-blt: Contains the metadata files for the collections
-drawings: Contains the svg files for the individual parts

In addition to them, there may be present a number of directories each containing files necessary for one backend. The following directories are supported:

-scad: Contains the OpenSCAD base files.

blt
===

A blt file is a yaml file with a single document containing one associative array with the following keys:

-collection: mandatory. The Collection Header.
-scad: optional. The OpenSCAD Header.
-parts: mandatory. A list of Parts.

These structures are specified below.

Collection Header
-----------------

The collection header is an associative array that contains general informations regarding the Collection. It contains the following keys:

- name: optional. A name for the collection.
- description: optional. A description of the contents of this collection.
- author: mandatory. The author of this collection with e-mail. If multiple authors contributed significantly to this collection a list of authors may be given.
- license: mandatory. A short form of the license of this file and a URL with more information
- blt-version: mandatory. The version of the blt format this collection follows.

OpenSCAD Header
---------------

The OpenSCAD header is an associative array that contains information regarding the output of this collection via the OpenSCAD backend. Required if the OpenSCAD backend is used. It contains the following keys:

- base-file: mandatory. The name of the file containing the OpenSCAD base modules. If these are distributed over more than one file, a list of filenames may also be given. All these files must be present in the scad folder.
- base-functions: mandatory. An associate array. The keys are the names of the base module names, the values are the names of the parameters of the base module. The parameters are looked up in the tables by their name. The names of the parameters is arbitrary, only "standard" is an invalid parameter name.

Parts List
----------

The parts list is a list of associative arrays, each describing a part. A part can contain the following keys:

-standard: mandatory. The name of the standard. In the case of several identical standards, a list of names can be given.
-status: optional. This can be used to indicate the status of the standard. Possible values are active, withdrawn. If not specified, active is assumed.
-replaces: optional. The name or a list of names of standards that are replaced by this standard.
-description: optional. A short description of the part.
-base: mandatory. The base to use for this part.
-target-args: mandatory. The remaining parameters of the part.
-literal-args: optional. A associative array with parameters and their literal values.
-name: mandatory. A naming definition
-url: optional. For standard parts the URL where the official standard can be bought.
-table: optional. A table of dimensions.
-notes: optional. Notes for this part. This can be used to mention confusions, contradicting informations or missing data.

Names
-----

A name is a associative array with one mandatory key:
- template: mandatory. A string that may contain placeholders (%s, %d, %f, ...)
- parameters: optional. A list of parameters that gets inserted into the template string. Parameters may be "standard", or arbitrary base function parameters.

Tables
------

A table is a associative array with two mandatory keys:

-columns: mandatory. A list of short column names. These names are used in measure lookup. Each name is usually one or few characters long and the abbreviation of a measure of the part.
-data: mandatory. The table as associative array with a key and a list of values. This list must have the same length as the list of columns. Unspecified values are given as None.

