---
  layout: docs
  title: How to use BOLTS for OpenSCAD
---

You need to have [installed BOLTS for OpenSCAD](installation.html).

### Inserting parts

Using parts from BOLTS works exactly like
[using modules](http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#Modules)
that you defined yourself in your scad file.

The most difficult part is to find the right module. Modules are named after
the standard that specifies the dimensions of a part. If a part is not
standardized, the module has a descriptive name.

It might seem a bit awkward to refer to a simple bolt as DIN931 or ISO4014, but
by using this naming scheme, the part is uniquely specified, and this
information is useful when assembling a bill of materials or shopping for all
required parts for a design.

But most people do not know the standard numbers for the parts that they want
to use. For this reason BOLTS offers on its webpage a
[browsable overview]({{site.baseurl}}/html/index.html)
over all parts that it provides. There one can browse through the different
collections and check out which standards of a standardization body are
available in BOLTS.

Each part has a dedicated page, where one can find more detailed informations
about this part, a drawing and tables with dimensions. The information that is
most interesting for our purposes can be found in the section OpenSCAD. There
it says either that the part is not available for OpenSCAD (in which case you
might consider [to help making it available]({{site.baseurl}}/contribute.html)),
or gives details how to use it.

The hexagon bolt [ISO4014]({{site.baseurl}}/html/classes/ISO4014.html) is
available, and in the subsection `Incantations` the first tells us how to
insert it in our scad code. The module name is ISO4014, it takes two
parameters, a key (default value "M3"), and the length l (default value 20).
The meaning of the parameters can be checked in the drawing and the tables on
he page.

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

For example for a M4 washer according to DIN125A:

    dims = DIN125A_dims("M4");

dims is now a list of lists with the content

     [["s", 0.8], ["d2", 9], ["key", "M4"], ["d1", 4.3]]

A specific dimension (like the inner diameter) can now either be accessed using list indices

    echo(dims[3][0]);

or by using a convenience function provided by BOLTS

    echo(get_dim(dims,"d1"));

If you need only a single parameter, it is even shorter to avoid the dims variable and write

    echo(get_dims(DIN125A_dims("M4"),"d1"));


By using dimensions this way, your code avoids magic numbers and becomes more
readable and can be modified easily.

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

Or if you use a standard, that is not used anymore (like [DIN931]({{site.baseurl}}/html/classes/DIN931.html)):

    DIN931("M4",20);

BOLTS will inform you that

    Warning: The standard DIN931 is withdrawn. Although withdrawn standards are often still in use, it might be better to use its successor DINEN24014 instead


