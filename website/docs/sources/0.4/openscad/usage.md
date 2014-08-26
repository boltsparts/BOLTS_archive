---
  title: How to use BOLTS for OpenSCAD
  audience: user
---

You need to have [installed BOLTS for OpenSCAD]({{ doc(openscad,installation) }}).

### Inserting parts

Using parts from BOLTS works exactly like
[using modules](http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#Modules)
that you defined yourself in your scad file.

The most difficult part is to find the right module. Modules are named after
the standard that specifies the dimensions of a part. If a part is not
standardized, the module has a descriptive name.

It might seem a bit awkward to refer to a simple bolt as {{ standard(DIN931) }}
or {{ standard(ISO4014) }}, but by using this naming scheme, the part is
uniquely specified, and this information is useful when assembling a bill of
materials or shopping for all required parts for a design.

But most people do not know the standard numbers for the parts that they want
to use. For this reason BOLTS offers on its webpage a
[browsable overview]({{ url(parts.index) }})
over all parts that it provides. There one can browse through the different
collections and check out which standards of a standardization body are
available in BOLTS.

Each part has a dedicated page, where one can find more detailed informations
about this part, a drawing and tables with dimensions. The information that is
most interesting for our purposes can be found in the section OpenSCAD. There
it says either that the part is not available for OpenSCAD (in which case you
might consider [to help making it available]({{ url(main.contribute) }})),
or gives details how to use it.

The hexagon bolt {{ standard(ISO4014) }} is available, and in the subsection
`Incantations` the first tells us how to insert it in our scad code. The module
name is `ISO4014`, it takes two parameters, a key (default value "M3"), and the
length l (default value 20).  The meaning of the parameters can be checked in
the drawing and the tables on he page.

So to insert a M3x20 hexagon bolt into our design, we just write

    ISO4014();

for an M8x40, we use

    ISO4014("M8",40);

and so on.

### Using dimensions

You probably need to translate and rotate the bolt in your design to have it
exactly where you want it. For that it is useful to know the dimensions of the
part. One could look them up in the tables and insert the numbers in the scad
file by hand, but BOLTS offers a more flexible way: On can obtain a list of all
parameters of the part using the second line listes in the `Incantation`
section of the part page.

For example for a M4 washer according to {{ standard(DIN125A) }}:

    dims = DIN125A_dims("M4");

dims is now a list of lists with the content

     [["s", 0.8], ["d2", 9], ["key", "M4"], ["d1", 4.3]]

A specific dimension (like the inner diameter) can now either be accessed using
list indices

    echo(dims[3][0]);

or by using a convenience function provided by BOLTS

    echo(get_dim(dims,"d1"));

If you need only a single parameter, it is even shorter to avoid the dims variable and write

    echo(get_dim(DIN125A_dims("M4"),"d1"));


By using dimensions this way, your code avoids magic numbers and becomes more
readable and can be modified easily.

### Using connectors

To make the positioning of BOLTS part easier, BOLTS includes
[local.scad](https://github.com/jreinhardt/local-scad), an improved version of
the [attach library](http://www.thingiverse.com/thing:30136).

Instead of having complicated nested `translate` and `rotate` calls, this
library allows to specify the position and orientation of a portion of a design
using so called connectors. A connector is a data type that contains
informations about both position and orientation.

A connector is created with the `new_cs` function, which takes two arguments: a
vector with three values specifying the origin of the connector and a list of
two vectors specifying one main and one additional direction.

Connectors are actually like local coordinate systems with a origin and three
axes, but the third direction does not need to be specified, but is calculated
from the other two direction.

Connectors can be displayed using the `show_cs` module, which takes a connector
as argument. The resulting object has a size of one unit, so it might be
difficult to spot in big designs.

Positioning is done with the `align` module, which takes two connectors as
arguments. It then translates and rotates the child of the module such that the
first connector is aligned with the second connector. Optionally, a
displacement in the connector coordinate system can be specified.

Many parts in BOLTS already have connectors connectors defined, to check what a
specific part provides, check the part page in the
[online reference]({{ url(parts.index) }}). For parts with connectors
a function is available with the same name as the part, but with a `_conn`
appended. This function takes the name of the connector as first argument and
the same arguments as the part as further arguments and returns the connector.

The general workflow is to create a connector which specifies where the BOLTS
part should end up in your design. Then a connector of the BOLTS part is
chosen, depending on what point of the part should end up there. Finally the
align module is used to position the part.

This structure is illustrated again by the following example:

### Example: Bolted connection

    include <BOLTS.scad>
    
    $fn=50;
    
    % cube([10,40,50]);
    
    //target connector
    cube_cs = new_cs(origin = [10,20,20], axes = [[-1,0,0],[0,-1,0]]);

    //BOLTS part connectors
    washer_cs = ISO7089_conn("top","M4");
    bolt_cs = ISO4017_conn("root","M4",20);
    nut_cs = ISO4035_conn("bottom","M4");
    
    //connectors can be displayed with
    //show_cs(cube_cs);
    
    //thickness of washer
    s = get_dim(ISO7089_dims("M4"),"s");
    
    //position washer and bolt at the location specified by cube_cs
    align(washer_cs,cube_cs) ISO7089("M4");
    align(bolt_cs,cube_cs,[-s,0,0]) ISO4017("M4",20);
    align(washer_cs,cube_cs,[10+s,0,0]) ISO7089("M4");
    align(nut_cs,cube_cs,[10+s,0,0]) ISO4035("M4");

This results in

[<img alt="Bolted connection example" src="{{ static(openscad-positioningexample.png) }}" />]({{ static(openscad-positioningexample.png) }})


### Check for errors

The modules provided by BOLTS perform a number of sanity checks. If there is a
problem, it will output a warning on the console, so you should check that
after compiling.

For example, if you mix up the parameters

    ISO4014(40,"M8");

BOLTS will tell you

    Error: Expected a Table Index as parameter key for ISO4014, but 40 is not a string
    Error: Expected a Length (mm) as parameter l for ISO4014, but M8 is not numerical
    TableLookUpError in ISO4014, table 0

Or if you accidentally give a negative length

    ISO4014("M8",-40);

BOLTS will tell you

    Error: Expected a Length (mm) as parameter l for ISO4014, but -40 is negative

Or if you use a standard, that is not used anymore (like {{ standard(DIN931) }}):

    DIN931("M4",20);

BOLTS will inform you that

    Warning: The standard DIN931 is withdrawn. Although withdrawn standards are often still in use, it might be better to use its successor DINEN24014 instead

### Checking for the version

BOLTS provides version information to allow a scad file to complain when a
unsuitable version of BOLTS is used. This is especially important for scad
files that are published on the internet. Version information comes in two
flavours: the number of the release, and a date.

The number of the release can be accessed by calling the function

    BOLTS_version()

For a stable release it returns a list with the major and minor version as
integers. For a development release the string "development" is returned.

The date can be accessed using the function

    BOLTS_date()

and is returned as a list with three integers for the year, the month and the
day at which the distribution was exported.

The final ingredient to uniquely identify the version of BOLTS is the license.
Distributions conforming to different licenses can differ in the selection of
parts offered. To query the license of the distribution one can use the function

    BOLTS_license()

which returns a string with the license.
