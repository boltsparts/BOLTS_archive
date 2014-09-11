---
  title: How to add connectors
  audience: contributors
---

This page shows you how to add connectors for a part, for which a OpenSCAD
[basemodule]({{ doc(openscad,basemodule) }}) exists. It continues the example
from the [basemodule guide]({{ doc(openscad,basemodule) }})

[Connectors]({{ doc(openscad,usage) }})
simplify the positioning of parts in OpenSCAD, but require a bit of
preparation. Three things need to be added: 

- a function for the connectors in the scad file
- a entry in the base file
- drawings for the documentation.

### Adding a connector function in the scad file

The function is added to the `.scad` file, and calculates the position and
orientation for the various connector locations from the parameters of the
model. It returns a list containing as first element the origin of the
coordinate system in terms of global coordinates, as second element a list with
two directions for the first and second direction of the connector. In case the
direction is unknown, the function should return "Error".

For the pipes ths function could look like this:

    function pipeConn(l,location) =
    	(location == "front-in")  ? [[0,0,-l/2],[[0,0,1],[1,0,0]]] :
    	(location == "front-out") ? [[0,0,-l/2],[[0,0,-1],[-1,0,0]]] :
    	(location == "back-in")   ? [[0,0,+l/2],[[0,0,-1],[-1,0,0]]] :
    	(location == "back-out")  ? [[0,0,+l/2],[[0,0,1],[1,0,0]]] :
    	"Error";

Here only the origin of the connector depends on the length of the pipe, but
for other locations other parameters might be required. The function can make
use of all parameters that are available to the geometry modules in addition to
the location, and the order in which these are passed to the function is not
relevant.

### Add an entry in the base file

To tell BOLTS about this and things like the available selection of locations
available. This is done by a additional field in the base file (see also 
[the basemodule documentation]({{ doc(openscad,basemodule) }})). The entries are
selfexplanatory, so here is the content of the base file with the connector
infos:

    ---
    - filename: pipe.scad
      type: module
      author: Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
      license: LGPL 2.1+ <http://www.gnu.org/licenses/lgpl-2.1>
      modules:
        - name: pipe
          arguments: [id, od, l]
          classids: [genericpipe, din11850range2]
          connectors:
            name: pipeConn
            arguments: [l,location]
            locations: [front-in, front-out, back-in, back-out]
      source: own work
    ...

This is a good time to test again. You can use the utility script like shown
[in the basemodule guide]({{ doc(openscad,basemodule) }}). Make sure all
connectors are where they should be and that this remains the case when you use
a range of parameters.

### Create drawings

The final thing to do is create drawings for the connectors to visually show
their location for easy reference. The utility script can do most of the heavy
lifting, by creating OpenSCAD scripts for each location that shows the part
together with the connector there.

    ./bolts.py connectors

This results in a directory called `connectordrawings` in the output directory.
It contains BOLTS for OpenSCAD and a directory called scad that contains scad
files for all classes with connectors that have no drawings.  All that remains
to do is to load these scripts into OpenSCAD, find a good angle and export a
png using `Design->export as image...`. Make sure that it is easy to understand
from the picture where the connector is located on the part, and how it is
oriented.The images go into the `pipes` subdirectory of the `drawings` folder.

[<img alt="Finding a good angle" src="{{ static(openscad-connectordrawings.png) }}" />]({{ static(openscad-connectordrawings.png) }})

The final step is to add entries to the base file in this folder to tell BOLTS
about all the drawings. Here is an example how it looks for the `front-in`
connector:

    - filename: pipe-back-in
      author: Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
      license: CC0 1.0 <http://creativecommons.org/publicdomain/zero/1.0/>
      type: drawing-connector
      location: back-in
      source: own work
      classids: [genericpipe,din11850range2]

You should add your name as author. The license should be chosen to CC0, as
this makes things easier. `type` must be `drawing-connector`.

### Check everything again

To check that everything went fine, you can use

    ./bolts.py tasks

and make sure that the classes you have been working on are not listed anymore
with `Missing Connectors` and `Missing Drawings`.

### Next steps

You might want to [contribute]({{ doc(general,development) }}) this part to
BOLTS, so that every user can profit from your efforts.
