---
  title: How to setup a base function
  audience: contributors
---

You need to have FreeCAD and [FreeCAD for BOLTS installed]({{ doc(freecad, installation) }}).

This assumes that the [blt file]({{ doc(general, blt-files) }})  for this part
is already created, and you have a python function that creates the part that
you want to add to BOLTS. For more information on part scripting in FreeCAD see
the [FreeCAD documentation on this topic](http://freecadweb.org/wiki/index.php?title=Power_users_hub).


### The function

As an example we  use the follwing function to create washers:

    import Part

    def washer1(params,document):
        key = params['key']
        d1 = params['d1']
        d2 = params['d2']
        s = params['s']
        name = params['name']

        part = document.addObject("Part::Feature",name)
        outer = Part.makeCylinder(d2,s)
        inner = Part.makeCylinder(d1,s)
        part.Shape = outer.cut(inner).removeSplitter()

This function uses the CSG facilities of FreeCAD, but it is equally possible to
use BRep scripting.

It is necessary to write the function such that it is a function of two
parameters, a dict of parameter names and values, and a FreeCAD document. The
keys of this dict will be the names of the parameters of the part, as described
in the blt file. There is an additional parameter `name` that holds the name of
the part.

In the first part of the function, we are assigning local variables with the
parameter values as a shortcut. In the second part of the function, we add a
new object to the document, create the geometry and assign it to the part.
`removeSplitter` cleans up artifacts resulting from CSG operation under certain
circumstances.

### Put it to the right place

This function should reside in a file (in this case called `washer.py`) with
extension `.py` in a subdirectory of the freecad directory which is named after
the collection to which the part belongs (in this case `washer`). This
directory must contain a empty file called `__init__.py` and the base file for
this collection (in this case `washer.base`).

### Write the base file

The base file provides BOLTS with all the informations it needs to know about
the files in a collection directory, it is a kind of manifest file. It contains
a list of sections (more precisely 
[base file elements]({{ spec(base-file-element) }}))
, each describing one file:

    ---
    - filename: washer.py
      author: Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
      license: LGPL 2.1+ <http://www.gnu.org/licenses/lgpl-2.1>
      type: function
      functions:
        - name: washer1
          classids: [plainwasher1, plainwasher2, plainwasherforcheesehead, heavydutyplainwasher]
    ...

The hyphens and dots on the first and the last line indicate the begin and
end of the metadata (a base file is a [YAML file](http://yaml.org/). Between
those two markers follows a list of base file elements, one for each file.
The begin of a new element is indicated by a hyphen. If there are more than
one file in the collection directory, there would be more elements, but here
it is only one.

The base file element gives informations about the file like the filename,
the author and the license under which it is published.

The line `type: function` indicates that it contains python functions for
FreeCAD. As a file can contain more than one function, a list of elements
follows, that describe the individual functions. In our case there is only
one, called washer1.

There is the possibility to add an optional `source` field which allows to give
informations about the origin of the file. If there is a URL from which this
file was downloaded, this can be included here.

The `classids` field contains a list of classids to which this function
applies.  BOLTS contains four different classes that describe washers, so in
this case this list is rather long, but in other cases it might only contain
a single entry. Be careful, that the parameter names for all classes in this
list must be the same, otherwise the parameter dict contains unexpected
entries or names can not be found.

When working on base files, pay attention to whitespace and identation and do
not use tabs.

### Testing

You should now test the newly added part. This is most easily done on the
command line by typing

    ./bolts.py export freecad
    ./bolts.py test freecad

in the repo directory. This will fire up a FreeCAD instance with the module
search path set appropriately, so that typing

    import BOLTS

on the FreeCAD python console should do the trick.

If BOLTS is started successfully, try adding the newly added part to the
current document with different combinations of parameters.

If nothing happens when you try to add the file, there is probably an error
occuring during the execution of the function. Such errors are suppressed by
the gui system, so that no error messages are displayed. You can circumvent
this by activating the `Add part` button manually. To do this type

    BOLTS.widget.ui.addButton.clicked.emit(True)

in the FreeCAD python console. This should display exceptions if they occur and
also the output from `print` statements.

When fixing a bug, you have to close FreeCAD, and repeat this step from the
beginning. This is a rather tedious development cycle, so taking care when
writing the function pays off in this case.

### Next steps

You might want to [contribute]({{ doc(general, development) }}) this part to
BOLTS, so that every user can profit from your efforts.
