###############################
BOLTS Specification Version 0.4
###############################

The BOLTS library consists of several different components, processes and
conventions and a number of precisely defined concepts. The purpose of this
document is to specify them in detail.

*****************************************
Parts, Classes, Standards and Collections
*****************************************


In this section some concepts are defined, that will be used later in the
specification of the blt-file_.

.. _part:

Parts
=====

A BOLTS repository_ contains a various sorts of data about objects, that are in
some way useful in CAD. A part is an object that can be described by a set of
parameters. E.g. a piece of paper is described by its width of 210mm and its
height of 297mm.

.. _class:

Classes
=======

However, one often encounters parts that are very similar to each other, for
example just differing in their dimensions. These parts can then be more
efficiently described as a class of parts. To continue with the paper example,
a class describing pieces class could also contain a part with width 100mm and
height 100mm.

In a blt-file_ only classes of parts are described, because this case is so
frequent.  Some parts are one of a kind, so it is not uncommon to have classes
that contain just a single part.


The classes of technical parts that BOLTS deals with are often specified by
standards issued by standardization bodies. This can be specified for a class
in the blt-file_. Within BOLTS, a class is referred to by its unique class id,
but for the user a class may be known under multiple names or specified in
multiple identical standards. To reflect this, classes can contain one or
several  class-name-element_ and class-standard-element_ constructs.

.. _collection:

Collections
===========

It turns out to be convenient to organize the classes of a BOLTS repository in
collections. A collection usually has one or few authors, the parts contained
are in some sense related to each other and all the data of a collection is
under the same licence.

Each collection has a one word identifier, the collection id. The collection id
is the filename (without extension) of the blt-file_ with the information about
the collection, and also explicitly specified in the blt-file_. For more
details see there.

.. _repository:

**************
The repository
**************

A BOLTS repository is directory structure with a certain layout. It contains
all the data and metadata. The root directory contains at least a "data"
directory with the backend independent data in blt-file_, plus optionally a
number of database directories with additional data that can be used by a
backend_. See list-of-databases_ for details.

The data directory
==================

The data directory contains a number of blt-file_, one for each collection_.
These files contain the general, backend independent information about the
classes in the repository.

.. _database:

The databases
=============

A database directory is a directory that contains data about certain aspects of
the parts or data in a specific form. Backends can access this data to
transform the parts data into specific forms or collect informations.

In contrast to the data in the blt-file_, the data in the database directories
is optional. If for a class_ this data is not available, the backend_ has to be
able to deal with it in an appropriate manner, for example by not processing
this class.


**************************************
Backends, Processing and Distributions
**************************************

In BOLTS the general, backend independent data and metadata is separated from
the backend specific data for e.g. a particular CAD system. The former is held
in blt-file_, the latter in database_ directories.

.. _backend:

Backend
=======

.. _distribution:

A backend is a process that uses backend independent data and data from
database_, transforms this data and outputs a set of files. This output is called
the distribution of this backend.

.. image:: processing.png
   :width: 100%


An example for a backend would be a process that uses the backend indepent data
about parts, their geometries and dimensions together with a number of
templates and stylesheets and produces a set of HTML pages with a nicely
rendered, browsable description of the parts. Other backends could produce data
that is suitable for use in specific CAD applications.

Backends are not specified in detail by this specification.

.. _blt-file:

Backend independent data - the blt file
=======================================

The backend independent data is stored in files with the extension .blt
containing `yaml <http://yaml.org/>`_ markup. These files contain exactly one
YAML document consisting of an associative array with the following keys:

- id: mandatory, string. The id of the collection. Must be identical to the
  filename of the blt file without the extenstion.
- name: optional, string. A name for the collection.
- description: optional, string. A description of the contents of this
  collection.
- author: mandatory, string or list of strings. The author of this collection
  with e-mail in <>. If multiple authors contributed significantly to this collection
  a list of authors may be given.
- license: mandatory, string. The name of the license for this collection and a
  URL pointing to the full text of the license enclosed in <>. Must be one of
  the supported-licenses_.
- blt-version: mandatory, number. The version of the blt format this collection
  follows.
- classes: mandatory. A list of class-element_.

The filename without the .blt extension is called the collection id. For
consistency they are repeated in the id field. Collection ids are one word
identifiers, which must be unique within the repository.  They should contain
only letters, numbers and underscores, and should be descriptive.

.. _class-element:

Class element
-------------

A class element is an associative array that holds information about a
class_. It has the following keys:

- id: mandatory, string. The id of the class. Class ids are one word
  identifiers, which must be unique within the repository. This class id is
  used as a way to refer to the class, when the standard field is not set.
  They must contain only letters, numbers and underscores.
- names: optional, class-name-element_ or list of class-name-element_ . One or
  several names for this class.
- standards: optional, class-standard-element_ or list of
  class-standard-element_ . One or several standards, in which the parts of this
  class are specified.
- parameters: optional, parameter-element_: Parameters for this class.
- url: optional, string or list of strings. A url with relevant information
  regarding the parts of this class. For example a link to a vendor, or to the
  specifying standard.  In the case of several identical standards, a list of
  urls has to be given.
- notes: optional, string. Notes for this class. Can be used to keep questions
  or additional information.
- source: mandatory, string. A short description where the informations for this
  class originate. Should contain a URL if possible.

.. _class-name-element:

Class Name Element
------------------

A class name element is a way to assign a name to a class. A class element
should be used for general names, like "Hex head screws" and for names that are
not derived from a standard issued by a standardisation body. For names that
are derived from a standard, a class-standard-element_ is more appropriate.

A class name element is an associative array with the following keys:

- name: mandatory, string or identifier-element_. The name for the class. If
  given as a string, this is interpreted as the nice name of the identifier
  element.
- group: optional, string or identifier-element_. Can be used to group class
  names together, similar to the group in a class-standard-element_. Useful
  for parts that are not standardized by a standardisation body, but by e.g. a
  vendor. If given as a string is taken as the nice name of the identifier
  element.
- labeling: mandatory, string or substitution-element_. A template for the name
  of a part from this class, e.g. for a BOM. If given as string is taken to be
  the nice name.
- description: optional, string. A short description of the class.

The safe name of this class must be unique within the repository and provides a
way to refer to this class.

.. Maybe tag, vendor info, order url

.. _class-standard-element:

Class Standard Element
----------------------

A class standard element is similar to a class-name-element_, but is used
specifically to associate a class with a formal standard, and allows to
expresses additional facts about this standard.

a class standard element is an associative array with the following keys:

- standard: mandatory, string or identifier-element_. The name of the standard.
  If given as a string is taken as the nice name of an identifier element.
- group: optional, string or identifier-element_. If a single standard
  specifies multiple classes of parts, the group can be used to collect the
  substandards together. If the group is given as a string is taken as the nice
  name of the identifier element.
- labeling: mandatory, string or substitution-element_. A template for the name
  of a part from this class, e.g. for a BOM. If given as a string is taken as
  the nice name.
- body: mandatory, string. The standardisation body that issued the standard.
- year: optional, integer. The year in which the standard was issued.
- status: optional, string. This can be used to indicate the status of the
  standard.  Possible values are "active" and "withdrawn", if absent, "active"
  is assumed.
- replaces: optional, string. Names of ths standards that are superseded by
  this standard.
- description: optional, string. A short description of the class.

If a group field is specified it has to be identical in all standards that
belong to this group. In this case the standard fields have to contain a suffix
or similar to distinguish them from the group, while still being unique.  If
several classes are specified in the same standard, the safe and nice names of
the corresponding class standard elements must be the same in all classes.
.. not sure I still understand this last sentence.

.. _identifier-element:

Identifier element
------------------

To be able to uniquely refer to class in different circumstances, it is
necessary to have both a safe and a nice name. The former is used in file names
or as function or variable name in a script, and therefore has to obey certain
constraints. The latter is used in places, where no such constraints apply,
like GUIs or web pages.

These two names are bundled up in a identifier-element_, an associative array
with the following keys:

- nice: mandatory, string. A nice name for the class.
- safe: optional, string. A safe name for the class. This means, it contains
  only alphanumerical characters and underscores. Defaults to a sanitized
  version of the nice name.

.. _substitution-element:

Substitution element
--------------------

One also wants to have name or labels for a part derived from a class. This
name usually depends on the value of the parameters and, like with the
identifier-element_, must be available in a safe and nice form for use in
different situations. The restrictions on the safe name are a bit weaker than
with the identifier-element_.

To insert the value of a parameter into this name, a placeholder of the form
`%(parameter)s` can be inserted.

- nice: mandatory, string. A nice name for the part.
- safe: mandatory, string. A safe name for the class. This means they must be
  ASCII printable with no forward or backward slashes, no question marks, no
  asterisk, no colon, no pipe, no quotes, no lesser or greater than signs, no
  whitespace.  Defaults to a sanitized version of the nice name.


.. _parameter-element:

Parameter element
-----------------

A parameter element is an associative array that holds information about the
parameters of a part. This information is used when doing
parameter-collection_. Parameters are often dimensions, but are not
restricted to be. The following keys are contained in a parameter element.

- literal: optional, associative array. This array has as its key the parameter
  names of the literal parameters, as values the corresponding values. Literal
  parameters are rarely used.
- free: optional, list. This list contains the names of the parameters for
  which the user will provide this value.
- tables: optional, table-element_ or list of table-elements. This array
  contains tabular data. Usually the table index will be a free variable, for
  details see table-element_ and parameter-collection_.
- tables2d: optional, table2d-element_ or list of table2d-elements. This array
  contains tabular data. Usually row and column indices will be free variables,
  for details see table2d-element_ and parameter-collection_.
- types: mandatory, associative array. Contains as keys parameter names, as
  values their respective types. Possible types are: "Length (mm)", Length
  (in)", "Number", "Bool", "Table Index", "String", "Angle (deg)".
- defaults: optional, associative array. This array contains a default value
  for every free parameter. If absent, the default value defaults to the type
  specific values given in the table below.
- description: optional, associative array. This array contains short a short
  text for each parameter clarifying the meaning of the parameter in plain
  language.
- common: optional, list of lists of (lists or strings). This field contains a
  list of tuples that contain valaues for all free parameters in the order in
  which they are given in the free field. These tuples are  represented by a
  YAML list and contain common combinations of parameters. For more compact
  notation, every element of the tuple actually is a list of values, so the
  tuple represents all possible combinations of values for the parameters. A
  tuple element can also be ":" if the free variable is discrete (see table
  below), the being a shorthand for all possible values. Defaults to the empty
  list, if at least one free variable is not discrete. If all free variables
  are discrete, the default is the tuple with all possible parameter
  combinations.

============  ==============  =========
Type          Default Value   Discrete
============  ==============  =========
Length (mm)   10              no
Length (in)   1               no
Number        1               no
Bool          False           yes
Table Index   ""              yes
String        ""              no
Angle (deg)   0               no
============  ==============  =========

The two values of the type Bool are true and false (lowercase). Table index
values (keys) are strings, and must be ASCII with no forward or backward
slashes, no question marks, no asterisk, no colon, no pipe, no quotes, no
lesser or greater than signs.


.. _table-element:

Table element
-------------

Tables of data are very common in standards and very useful for specifying a
class_ of parts. A table element describes a table of values, where the row is
specified by the value of an index parameter, and each column contains the value
for a parameter. A table element is an associative array that has the following
keys:

- index: mandatory, string: name of the index parameter. Has to specified to be
  of type "Table Index" in the parameter-element_.
- columns: mandatory, list of strings: list of parameter names corresponding to the
  columns of the table.
- data: mandatory, associative array: The keys are possible values of the index
  parameter, the values a list of values compatible with the types of the
  parameters specified in columns. Note the restriction on the keys described
  in parameter-element_.

.. _table2d-element:

Table2D element
---------------

In some cases, a table-element_ is not powerful enough to represent the
relationship between the values of free parameters and other parameters, for
example if the value of a parameter depends on two free parameters at once.
This case is covered by a table2d element. A table2d-element allows to lookup
the value of the result parameter for a row given by a rowindex and a column
given by a colindex.

A table2d element  is an associative array with the following keys:

- rowindex: mandatory, string: name of the parameter that is used to select a
  row. Has to be specified to be of type "Table Index" in the
  parameter-element_. Note the restriction on the keys described in
  parameter-element_.
- colindex: mandatory, string: name of the parameter that is used to select a
  column. Has to be specified to be of type "Table Index" in the
  parameter-element_. Note the restriction on the keys described in
  parameter-element_.
- columns: mandatory, list of strings. The possible values for the colindex.
- result: mandatory, string. The name of the parameter whose value is
  determined with this table.
- data: mandatory, associative array: The keys are possible values of the
  rowindex parameter, the values a list of values for the columns from which
  one is selected by the colindex.

.. _parameter-collection:

Parameter Collection
====================

Parameter Collection is the process of assigning a value to each parameter. The
set of all parameters is found by collecting parameter names from the fields of
one or more parameter-element_:

- The keys of the literal field.
- The items of the free field.
- The index field of the table-element_ s in the tables field.
- The columns field of the table-element_ s in the tables field.
- The rowindex field of the table2d-element_ s in the tables2d field
- The colindex field of the table2d-element_ s in the tables2d field
- The result field of the table2d-element_ s in the tables2d field

It is an error condition if there is a parameter name present as a key in the
types field, that is not in the set of all parameters.

Then a value is assigned to each parameter. This can happen by:

- A literal value given in the literal field
- User or external input for parameters listed in the free field
- Table lookup for parameters listed in the columns field of a table-element_
- Table2d lookup for parameters listed in the result field of a table2d-element_

It is an error condition if a parameter is not assigned a value or if there is
more than one way to assign a value.

The parameter values collected  in this way are for example used (among other
things) to populate the template given in the substitution-element_.


.. _base-file:

Base File
=========

Base files are `yaml <http://yaml.org/>`_ files, in which informations about
the files for a collection in a database_ directory are stored. They consist of
a list of base-file-element_, one for each file they describe.

.. _base-file-element:

Base file element
-----------------

A base file element is an associative array containing informations about a
file. Depending on the type of the file the contained keys are different.
However, there are some keys that are present in every base file element:

- filename: mandatory, string. The filename of the file
- author: mandatory, string or list of strings. The author of the file with
  e-mail adress in <> or a list of several authors.
- license: mandatory, string. The license of the file. Must be one of the
  supported-licenses_.
- type: mandatory, string. A string describing the type of the file.
- source: optional, string. A string describing the origin of the file.

Different data bases contain different base-file-types, for a list see list-of-base-file-types_.

.. _list-of-databases:

#################
List of Databases
#################

********
Drawings
********

The drawings directory contains a number of subdirectories, one for
each collection. In each of these directories, drawings of the parts can be
stored, that illustrate the geometries of the parts and the meaning of the
parameters.

In each directory there is a .base file with the same name as the directory. It
contains metadata in form of a list of base-file-element_ of type
"drawing-dimensions" or "drawing-connector" for the files in this directory.
See base-file-type-drawing-dimensions_ and base-file-type-drawing-connectors_.


********
OpenSCAD
********

The files containing all the informations necessary to build a geometrical
representation of a class in OpenSCAD  reside in the "openscad" directory. This
database directory contains a folder for each collection_ which contains files
related to this collection, and the folder is named like the collection-id.

One ingredient for this are base modules,  OpenSCAD modules that take as
parameters a subset of the parameters of the part (see parameter-collection_),
and construct the part according to these dimensions. These modules are stored
in one or several files residing in the respective collection directory within
the openscad database directory

In order to integrate the base modules properly, BOLTS needs informations about
them. These informations are stored in the base-file_ of a collection, in form
of one base-file-element_ of type "modules" (see base-file-type-module_) for
every file with one or more modules.



*******
FreeCAD
*******

The "freecad" directory contains files that allow to build a geometrical
representation of a class in FreeCAD. This directory contains a folder for each
collection_, containing the files related to classes in this collection.

The geometrical representation for a part is obtained from a python function
that constructs the part using the scripting facilities of FreeCAD. The
base-file_ contains a base-file-element_ of type "function" for every python
module with one or more of these functions (see base-file-type-function_).


**********
SolidWorks
**********

The "solidworks" directory contains files necessary to build "design tables"
for use with the `SolidWorks software <http://www.solidworks.com/>`_. The
directory contains a folder for each collection_ with the files related to
classes in this collection.

The geometrical representation of the parts is supplied in the form of
parametrized models. Together with "design tables" these models allow to easily
obtain different sizes and variations of a part.

All the information necessary to build the design table is contained in the
base-file_ , which contain a list of base-file-element_ of type "solidworks"
(see base-file-type-solidworks_ ).


.. _list-of-base-file-types:

#######################
List of base file types
#######################

.. _base-file-type-drawing-dimensions:

******************
Drawing Dimensions
******************

This kind of base-file-element_ describes a drawing showing the dimensional
parameters of a part. It is an associative array with the following keys:

- filename: mandatory, string. The filename of the file without the extension.
  Files with the same basename but different extensions are taken to be
  conversions to different file formats.
- author: mandatory, string or list of strings. The author of the file with
  e-mail adress in <> or a list of several authors.
- license: mandatory, string. The license of the file. Must be one of the
  supported-licenses_.
- type: "drawing-dimensions"
- source: optional, string. A string describing the origin of the file.
- classids: mandatory, list of strings. The class_ ids to which this drawing applies.


.. _base-file-type-drawing-connectors:

******************
Drawing Connectors
******************

This kind of base-file-element_ describes a drawing showing the location of one
or several connectors (see base-module-cs_). It is an associative array with
the following keys:

- filename: mandatory, string. The filename of the file without the extension.
  Files with the same basename but different extensions are taken to be
  conversions to different file formats.
- author: mandatory, string or list of strings. The author of the file with
  e-mail adress in <> or a list of several authors.
- license: mandatory, string. The license of the file. Must be one of the
  supported-licenses_.
- type: "drawing-connectors"
- location: mandatory, string. Gives the name of the connector location that
  this drawing shows.
- source: optional, string. A string describing the origin of the file.
- classids: mandatory, list of strings. The class_ ids to which this drawing applies.

.. _base-file-type-module:

******
Module
******

This kind of base-file-element_ describes a file containing OpenSCAD modules.
It is an associative array that contains the following keys:

- filename: mandatory, string. The filename of the file
- author: mandatory, string or list of strings. The author of the file with
  e-mail adress in <> or a list of several authors.
- license: mandatory, string. The license of the file. Must be one of the
  supported-licenses_
- type: "module"
- modules: mandatory, list of base-module-element_. A list of base module
  elements describing the modules in the file.


.. _base-module-element:

Base module element
===================

A base module element is a associative array describing an OpenSCAD module with
the following keys:

- name: mandatory, string. The name of the module.
- arguments: mandatory, list of strings. A list with the arguments that need to
  be supplied to the module, in the correct order.  Is a subset of the
  parameters of the class, see parameter-collection_.
- classids: mandatory, list of string. A list of class ids for which this base
  module should be used.
- parameters: optional, parameter-element_: Additional basespecific parameters.
  These parameters allow to represent additional paramters, which are not
  specific to the class, but to the base. This allows e.g. to let the user
  choose  between a detailed and a schematic representation of the part.
- connectors: optional, base-module-cs_. Informations about the connectors
  attached to the part.

.. _base-module-cs:

Base module connectors
======================

A base-module-cs_ describes a set of local coordinate systems or connectors
that are attached to specific points of the part to allow easy positioning.
This is implemented by a OpenSCAD function that returns a coordinate system
structure. This function has all the arguments of the module in which the
base-module-cs_ is contained, and an additional argument "location" as the last
argument. A base-module-cs_ is an associative array with the following keys:

- name: mandatory, string. The name of the function that returns the
  connectors.
- arguments: mandatory, list of strings. A list with arguments that need to be
  supplied to the connector function in the right order. Is a subset of the
  parameters of the class and "location", the latter of which must be present.
- locations: mandatory, list of strings. A list of possible values that can be
  supplied for the argument "location" of the function.

.. _base-file-type-function:

********
Function
********
This kind of base-file-element_ describes a python file containing geometrical
data in form of functions that build a part in a FreeCAD Document. It is an
associative array with the following keys:

- filename: mandatory, string. The filename of the file
- author: mandatory, string or list of strings. The author of the file with
  e-mail adress in <> or a list of several authors.
- license: mandatory, string. The license of the file. Must be one of the
  supported-licenses_.
- type: "function"
- functions: mandatory, list of base-function-element_.

.. _base-function-element:

Base function element
=====================

A base function element is a associative array describing a python function
with the following keys:

- name: mandatory, string. The name of the function.
- classids: mandatory, list of string. A list of class ids for which this base
  module should be used.
- parameters: optional, parameter-element_: Additional basespecific parameters.
  These parameters allow to represent additional paramters, which are not
  specific to the class, but to the base. This allows e.g. to let the user
  choose  between a detailed and a schematic representation of the part.

.. _base-file-type-solidworks:

**********
Solidworks
**********

This kind of base-file-element_ contains all the information necessary to
create a design table that can be used together with a model file to create a
"configuration". It is an associative array with the following keys:

- filename: mandatory, string. The filename of the SolidWorks model file
- author: mandatory, string or list of strings. The author of the model file
  with e-mail adress in <> or a list of several authors.
- license: mandatory, string. The license of the file. Must be one of the
  supported-licenses_.
- type: "solidworks"
- suffix: mandatory, string. A descriptive suffix that can be used as part of
  a filename. Gets appended to the model filename to construct the filename
  for the design table.
- params: mandatory, associative array. This describes the mapping from the
  parameters in the model files to the BOLTS parameter names. This has to
  apply to all classes that will be included in this table.
- metadata: optional, associative array. This describes the mapping from
  metadata fields to BOLTS parameter names. This has to apply to all classes
  that will be included in this table.
- source: optional, string. A string describing the origin of the file.
- classes: mandatory, list of base-designtable-class-element_.

.. _base-designtable-class-element:

Base designtable class element
==============================

A designtable class element specifies the classes that should be included in a designtable.

- classid: mandatory, string. A classid that should be included in
  this designtable.
- naming: mandatory, substitution-element_. This describes the form of the
  configuration names in the design table.

.. _supported-licenses:

###########################
Supported Licenses in BOLTS
###########################

The license of a file contained in BOLTS must be one of the following:

* `CC0 1.0 <http://creativecommons.org/publicdomain/zero/1.0/>`_
* `Public Domain <http://jreinhardt.github.io/BOLTS/public_domain.html>`_
* `MIT <http://opensource.org/licenses/MIT>`_
* `BSD 3-clause <http://opensource.org/licenses/BSD-3-Clause>`_
* `Apache 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_
* `LGPL 2.1 <http://www.gnu.org/licenses/lgpl-2.1>`_
* `LGPL 2.1+ <http://www.gnu.org/licenses/lgpl-2.1>`_
* `LGPL 3.0 <http://www.gnu.org/licenses/lgpl-3.0>`_
* `LGPL 3.0+ <http://www.gnu.org/licenses/lgpl-3.0>`_
* `GPL 2.0+ <http://www.gnu.org/licenses/gpl-2.0>`_
* `GPL 3.0 <http://www.gnu.org/licenses/gpl-3.0>`_
* `GPL 3.0+ <http://www.gnu.org/licenses/gpl-3.0>`_

where a + indicates a clause that allows a later version of the license to be
used.

