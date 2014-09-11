---
  title: How to create a base module
  audience: contributors
---

This tutorial shows you the preferred way to make a class from a
[collection]({{ doc(general,blt-files) }}) available in OpenSCAD.

This assumes that you have already a module available that takes a number of
parameters as input and builds the part that the class describes.

If not you have two options. Either you learn
[OpenSCAD](http://www.openscad.org/documentation.html) and write such a module
yourself.

Or you try to find out if someone else has done this already. There are a number of sites where a lot of scad code is published:

 - [Thingiverse](http://www.thingiverse.com/)
 - [Youmagine](https://www.youmagine.com/)
 - [Cubehero](https://cubehero.com/)
 - [GitHub](https://github.com/)
 - [Bld3r](http://www.bld3r.com/)
 - [list with many more](http://reprap.org/wiki/Printable_part_sources)

However, to use code written by someone else, you need to make sure that there
are no licensing problems. I wrote about licensing in BOLTS
[here]({{ doc(general,licensing) }}). If the code has no licensing
information or is published under a incompatible license, you can try to
contact the author and ask him to dual-license with a license that allows
inclusion in BOLTS.

This tutorial will illustrate the process using the example of the pipe
collection with a pipe module that lives in a file called `pipe.scad`:

    /* Pipe module for OpenSCAD
     * Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
     *
     * This library is free software; you can redistribute it and/or
     * modify it under the terms of the GNU Lesser General Public
     * License as published by the Free Software Foundation; either
     * version 2.1 of the License, or (at your option) any later version.
     *
     * This library is distributed in the hope that it will be useful,
     * but WITHOUT ANY WARRANTY; without even the implied warranty of
     * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
     * Lesser General Public License for more details.
     *
     * You should have received a copy of the GNU Lesser General Public
     * License along with this library; if not, write to the Free Software
     * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
     */

    module pipe(id,od,l){
        difference(){
            cylinder(r=od/2,h=l,center=true);
            cylinder(r=id/2,h=l+1,center=true);
        }
    }


### Putting the scad file to the right place

The file with the module should be moved to a subdirectory of the openscad
directory which is named after the collection id to which the part belongs. If
this directory does not exist, create it.

So in the case of the pipes collection `pipe.scad` is now in the directory
`openscad/pipes` relative to the BOLTS root folder.

### Write the base file

This collection directory must also contain the base file for this directory.
The base file provides BOLTS with all the informations it needs to know about
the files in a collection directory, it is a kind of manifest file. It
contains a list of sections 
(more precisely [base file elements]({{ spec(base-file-element) }})),
each describing one file.

For the pipes collection the base file is `openscad/pipes/pipes.base` and has
the following content:

    ---
    - filename: pipe.scad
      type: module
      author: Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
      license: LGPL 2.1+ <http://www.gnu.org/licenses/lgpl-2.1>
      modules:
        - name: pipe
          arguments: [id, od, l]
          classids: [genericpipe, din11850range2]
      source: own work
    ...

The type field indicates, that this file contains one or more OpenSCAD
modules. The author field gives the author of `pipe.scad` and contact
information. In the license field the license of pipe.scad is indicated and
then follows the list of modules that are contained in the file.

In the case of `pipe.scad` there is only one module called `pipe`. The
arguments field gives the parameters that need to be supplied to the module.
The parameters must be a subset of the parameters of the class as it is
defined in the [blt file]({{ doc(general,blt-files) }}).

The `classids` field contains a list of classids which this module can
represent. Be careful, that the parameter names and meanings for all classes
in this list must be the same, otherwise the some parameters can not be found
for some classes.

There is the possibility to add an optional `source` field which allows to give
informations about the origin of the file. If there is a URL from which this
file was downloaded, this can be included here.

### Testing

Now it should be tested that the newly added part really works. This is most
conveniently done using the 
[utility script]({{ doc(general,utility-script) }}):

    ./bolts.py export openscad
    ./bolts.py test openscad

This will fire up a OpenSCAD instance with the module search path set
appropriately, so that typing

    include <BOLTS.scad>

    DIN11850_Range_2("10",1000);

should give you a pipe with nominal diameter 10 and 1m length.


### Next steps

You might want to [add connectors]({{ doc(openscad,connectors) }}) to simplify
the positioning of the part in OpenSCAD and/or
[contribute]({{ doc(general,development) }}) this part to BOLTS, so that every
user can profit from your efforts.
