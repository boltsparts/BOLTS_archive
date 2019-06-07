---
  title: How to work with blt files
  audience: contributors
---

blt files contain most of the backend independent data. There is one blt file
for each each collection, which provides the information about all the classes
of the collection.

### Creating a new collection

To create a new collection a new file with extension blt needs to be created in
the `data` directory of the BOLTS repository. This file is a
[YAML](http://yaml.org/) file and contains a license header, a collection
header and a list of class descriptions.

So for example, to create a collection that contains the dimension of the most
common types of pipes, one creates a file called `pipes.blt` in the `data`
directory of the BOLTS repository. The filename without the extension is called
the collection id.

The file should begin with a license header that specifies the license of the
file. BOLTS can work with a number of free licenses, a list and detailed
explanation can be found [here](licensing.html). If you are unsure what to choose,
[LGPL 2.1 or later](http://www.gnu.org/licenses/lgpl-2.1) or a more liberal license like
[MIT](http://opensource.org/licenses/MIT) are usually a good choice.

After the license header follows the collection header. It contains general
details about the collection. A list of possible fields can be found in the
[specification]({{ spec(collection-header) }}), but
alternatively looking at
[the other collections](https://github.com/jreinhardt/BOLTS/tree/master/data)
should show you how this works.

The field blt-version gives the version of the blt file format, which is not
the necessarily identical to the version of BOLTS. Which version is the current
one can be found in the
[specification]({{ spec(collection-header) }})

For the pipe collection the collection first part of the blt file looks like this:

    #BOLTS - Open Library of Technical Specifications
    #Copyright (c) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
    #
    #Permission is hereby granted, free of charge, to any person obtaining a copy
    #of this software and associated documentation files (the "Software"), to deal
    #in the Software without restriction, including without limitation the rights
    #to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    #copies of the Software, and to permit persons to whom the Software is
    #furnished to do so, subject to the following conditions:
    #
    #The above copyright notice and this permission notice shall be included in
    #all copies or substantial portions of the Software.
    #
    #THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    #IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    #FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    #AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    #LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    #OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    #THE SOFTWARE.
    ---
    collection:
        name: BOLTS pipes
        description: metric and imperial pipes
        author: Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
        license: MIT <http://opensource.org/licenses/MIT>
        blt-version: 0.2

As license I chose the MIT license. The description should be short and
descriptive and give the user an indication about what kind of parts to expect
here.

The license of the file as given by the license header should match the one in
the license field of the collection header.

A email address must be given for the author, to have a way of contacting the
author e.g. for licensing problems.  The license in the license field and the
license header must agree and be one of the [licenses that BOLTS
allows]({{ doc(general,licensing) }}). If more than one person contributed
significantly, then a list of authors can be given:

    author: [Johannes Reinhardt <jreinhardt@ist-dein-freund.de>, John Doe <doe@domain.tld>]


YAML uses indentation to mark up the structure of the document, so pay
attention to whitespace and do not use tabs. The amount of spaces for a
indentation level is arbitrary, but four spaces is recommended.

After the collection header follows the list of classes contained in the
collection. How to add a class is explained in the next section.

### Adding classes to a collection

After the header follows a list of class descriptions. If you are not sure that
you know what a class is in BOLTS, you can read a bit about it
[here]({{ doc(general,introduction) }}).

Much of the most important information that BOLTS needs to know about a class
concerns the different parameters of the part, their types, units and tables
that connect them.

To continue the pipe example from the first section, lets consider a pipe. To
fix its geometry completely, three dimensions are necessary: the inner
diameter, the outer diameter and the length.

However, some combinations of the three are more common than others, because there are
[standards](http://en.wikipedia.org/wiki/Pipe_%28fluid_conveyance%29#Sizes)
specify combinations of (some of) the parameters.

So another way to specify a pipe would be to specify a nominal pipe size and a
length. There are tables that one can use to look up the inner and outer
diameter for a given nominal pipe size. The length of a pipe is usually not
standardized.

There are different kinds of parameters in BOLTS. Free parameters are those
that the user has to choose when he inserts a part, like the length of a part.
BOLTS can also express tables, where a table index allows to lookup
combinations of other quantities, like the nominal pipe size allows to look up
the corresponding inner and outer diameter.

The parameters are used in various ways: they are handed to the CAD application
to build a 3D model of the part, or they are used to build a name for the part
that can be used to label the part or to create a BOM.

We will now add two classes: One for a completely general pipe where the user
can specify length and inner and outer diameter arbitrarily, and one class that
provides pipes following DIN11850 Range 1.

Again, more information and inspiration can be found in the
[specification]({{ spec(class-element) }}) or by looking
at other collections.

#### A generic pipe class

This is how the generic pipe class looks like

    classes:
      - id: genericpipe
        naming:
          template: Pipe OD %g mm ID %g mm length %g mm
          substitute: [od, id, l]
        description: a generic pipe
        parameters:
          free: [od, id, l]
          defaults: {od: 13, id: 10, l: 1000}
        source: No sources used

Each class needs a unique id. If the class is not covered by standards, then
this id is also exposed to the user, so choosing a descriptive name is a good
idea.

The naming field describes how to generate a name for the part. It consists of
a template with placeholders (the parts with the %), and the list of parameter
values that should be inserted there. The placeholders follow the rules of
[python string formatting](http://docs.python.org/2/library/stdtypes.html#string-formatting)

So a 1000mm long pipe with 12mm outer diameter and 10mm inner diameter would
get the name `Pipe OD 12 mm ID 10 mm length 1000 mm`, which completely
specifies the part. You can send someone shopping for that and he will come
back with the right part.

In the parameters field we specify that the part has three free parameters
called `od`, `id` and `l`. It is a good idea to use short but expressive
parameter names because they can also appear on drawings.

We also give sensible default values for the free parameters.

Finally, the source field should be used to explain where the informations come
from on which this class is built. In this case we do not really need it, but
this becomes very important when building classes for standards.

#### A class for pipes according to DIN11850

Before we can build the class for parts following a standard, a bit of research
is necessary. First we need to find out which standards exist that specify the
dimensions of the parts that we are interested in. Next we need to find out as
much about the specifications as possible. Usually the standards are not freely
available and rather expensive, but often vendors provide drawings or tables or
other technical information. Technical information is a good term to search
for. Usually you get a big table of dimensions.

In the case of pipes, it was very easy to find this information,
[Wikipedia got it (in German)](http://de.wikipedia.org/wiki/Rohr_%28Technik%29#Abmessungen).
A bit of search also reveals a
[vendor site with more tables](http://www.gillain.com/en/tubes-and-components/p/detail/food-tubes-din-11850).

The class for DIN11850 looks like this

      - id: din11850range2
        naming:
          template: DIN11850 Range 2 DN %d length %g
          substitute: [dn, l]
        description: pipe
        standard: DIN11850 Range 2
        parameters:
          free: [dn, l]
          types: {dn: Table Index}
          defaults: {dn: "10", l: 1000}
          tables:
            index: dn
            columns: [id, od]
            data:
              "6" : [6, 8]
              "8" : [8, 10]
              "10" : [10, 13]
              "15" : [16, 19]
              "20" : [20, 23]
              "25" : [26, 29]
              "32" : [32, 35]
              "40" : [38, 41]
              "50" : [50, 53]
              "65" : [66, 70]
              "80" : [81, 85]
              "100" : [100, 104]
              "125" : [125, 129]
              "150" : [150, 154]
              "200" : [200, 204]
        notes: More tables can be found here http://www.gillain.com/en/tubes-and-components/p/detail/food-tubes-din-11850. The data there contradicts the one in Wikipedia, e.g. for DN32.
        source: de.wikipedia.org/wiki/Rohr_(Technik)#Abmessungen

As this class follows a standard the id is not shown to the user, so unique but
slighly bulky id is used. The first new thing in this class is the standard
field. The reason why not the id is used to encode the standard is that very
often there are equivalent standards issued by different organisations. In this
case a list of standards can be given in the standard field, which saves you
from duplicating a class description several times.

Unlike the generic pipe class this class only has two free parameters, the
nominal diameter and the length. The inner and outer diameters will be obtained
from a table, which is why the parameter `dn` is indicated to be of type `Table
Index`. If the type of a parameter is not indicated, it defaults to `Length
(mm)`. Other choices for types for parameters can be found in the
[specification]({{ spec(parameter-element) }})

Then one or several tables can follow in the tables field. Here we have only
one, linking the nominal diameter to the inner and outer diameter. Table
Indices should always be strings in YAML, so when there is ambiguity (as it is
here), enclose it by quotes.

If there are confusions or open questions or other things that you feel should
be communicated to people that might to work on this informationn in the
future, it can be put in the notes field. We put a short notice that we found
more tables but with conflicting data.

Finally the source field should now contains the link to the Wikipedia page
where we got the data for the table from.


### Testing

To test whether you got it right, you can use the [utility
script]({{ doc(general,utility-script) }}) to regenerate the html
documentation. If there are any problems with your blt file, you should get a
error message.

### Further steps

A collection becomes really useful, when [base geometries]({{ doc(general,introduction) }})
for its classes exist. Maybe you want to implement a 
[base module for OpenSCAD]({{ doc(openscad,basemodule) }})
or a 
[base function for FreeCAD]({{ doc(freecad,basefunction) }})
for your newly created collection.

(Actually, the [base module tutorial]({{ doc(openscad,basemodule) }})
explains how to setup a base-module for the pipe collection.)
