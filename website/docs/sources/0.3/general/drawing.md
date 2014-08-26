---
  title: How to make a nice drawing for BOLTS
  audience: contributors
---

### Prerequisites

You need to have installed [FreeCAD](http://freecadweb.org/) and [BOLTS for
FreeCAD]({{ doc(freecad,installation) }}) and the free Vector Graphics Editor
[Inkscape](http://inkscape.org/).

If the part for which you want to create the drawing is not in BOLTS for
FreeCAD, you also need [OpenSCAD](http://www.openscad.org/) and [BOLTS for
OpenSCAD]({{ doc(openscad,installation) }}).

### Follow this guide and contribute

There is a [list of classes]({{ url(main.tasks) }}) for which no drawing is
available. You are invited to pick one, follow this guide and contribute the
result.

### Scope

The main purpose of drawings in BOLTS is to give a quick visual explanation of
the meaning of the parameters of the class. It is not a full-fledged technical
drawing, whose purpose is to provide all the informations necessary to produce
the part. Nevertheless we borrow some conventions and techniques from technical
drawings.

### Loading a part

Depending on whether the part for your drawing is available in BOLTS for
FreeCAD or BOLTS for OpenSCAD, the first steps of this process differ.

It is a bit easier to work with parts from BOLTS for FreeCAD, because the
drawing is mostly created in FreeCAD.

If your part is available in BOLTS for FreeCAD, you have to start with the next
step.

If your part is only in BOLTS for OpenSCAD, you have to skip the next step and
continue at "Loading a part from BOLTS for OpenSCAD".

### Loading a part from BOLTS for FreeCAD

You can skip this step if you want to create a drawing for a part that is only
in BOLTS for OpenSCAD.

Start FreeCAD. Add a part of the class for which you want to create the
drawing, as described [here]({{ doc(freecad,usage) }}). The value of the
parameters does not matter too much, the default values will be usually fine.


### Exporting a part from BOLTS for OpenSCAD

You can skip this step if you have executed the previous step.

FreeCAD has the ability to load a part from a CSG file created by OpenSCAD. To
create such a file, fire up OpenSCAD, and type in the following short piece of
code

    include <BOLTS.scad>
    ISO7089();

The first line includes the BOLTS library. The second line creates a
part, in this case [a washer]({{ standard_url(ISO7089) }}).

If you hit F5, or select Design->Compile, the part should appear in the preview
window. You can now export the part to a CSG file by choosing Design->Export as
CSG....

[<img alt="Part from BOLTS in OpenSCAD" src="{{ static(openscad_drawing2.png) }}" />]({{ static(openscad_drawing2.png) }})

Save the file to some place where you can find it again, it is only temporary
and you can remove it afterwards.

You can close OpenSCAD now.

### Loading a CSG file into FreeCAD

Start FreeCAD. Then select File->Open and select the CSG file that you created in the previous step.

[<img alt="Loading a CSG file into FreeCAD" src="{{ static(openscad_drawing3.png) }}" />]({{ static(openscad_drawing3.png) }})

The part should now be visible in the preview window.

### Create a drawing

You should now have a document with the part for which you want to create the
drawing, and this should be the active object in this document (the one shown
in boldface letters in the combo view).

Now we can use the python console in FreeCAD to create a drawing:

    import BOLTS
    obj = FreeCAD.ActiveDocument.ActiveObject
    BOLTS.make_drawing(4.5,obj)

The first line starts BOLTS for FreeCAD (see also
[here]({{ doc(freecad,usage) }}), the second one creates a variable containing
the part and the third line calls a helper function from the BOLTS module.

This helper function has two parameters, a scaling factor and the object, and
it creates a new drawing from the BOLTS template and inserts various views on
the object.

Now an additional object should have vanished in the combo view, a page. 

[<img alt="Finished drawing of washer" src="{{ static(drawing1.png) }}" />]({{ static(drawing1.png) }})

You can open it in a new drawing viewer by double clicking on it. There will be
nothing visible, because the drawing needs to be recomputed, which you can do
by pressing the keys Ctrl-r.

Now you should see a page with the BOLTS logo in the lower right corner, and
different views on the object. If the scaling factor that you used was too big
or too small, you notice now. It is good to have a bit of space between the
different views to add dimensions, but the part should be not too tiny.

If the scaling factor was not good, you can close the Drawing Viewer, delete
the Page Object from the Combo View and type the last line again, with an
adjusted scaling factor.

[<img alt="Finished drawing of washer" src="{{ static(drawing2.png) }}" />]({{ static(drawing2.png) }})

When you are happy with the drawing, change to the Drawing Workbench, make sure
the page object is selected in the Combo View and then choose Drawing->Export
Page (or use the button in the Drawing toolbar).

Save it somewhere where you can find it again.

### Post processing in Inkscape

Now we need to add dimensions to the drawing, this is best done in Inkscape.
Open the svg file from the previous step in Inkscape.

In the case of the washer, there are three dimensions: the inner and outer
diameters and the thickness.

Now it is convenient to add a few guidelines by left-clicking on the rulers at
the sides and dragging into the picture. Depending on where you click you can
get horizontal (top), vertical (left) and diagonal (corner) guidelines.

The guidelines are added in such way that they are convenient for the
dimensions. The image below shows a possible choice: The inner diameter will be
indicated on the left side of the front view, the outer below. The thickness
will be indicated on the left side view.

[<img alt="Guidelines" src="{{ static(drawing3.png) }}" />]({{ static(drawing3.png) }})

Select the bezier line tool (Shift-F6 or the corresponding icon). Then click on
one of the guidelines, press Ctrl to lock in the angle to vertical or
horizontal and then click on the other guideline. The cursor should snap to the
guideline. Now finish the path by pressing Enter. Repeat for all dimensions.

[<img alt="Raw dimension lines" src="{{ static(drawing4.png) }}" />]({{ static(drawing4.png) }})

To convert these lines into nice dimensions open the fill and stroke dialog
using Object->Fill and Stroke and select the Stroke Style tab. Change to the
selection cursor (arrow icon in the toolbar), select one of your lines and do
the following three things:

1. Change the width to 0.4 px
2. For Start Markers select DistanceStart
3. For End Markers select DistanceEnd

If the Markers go in the wrong direction (away from the object), choose
Object->Flip Horizontal or Object->Flip Vertical, depending on the orientation
of your dimension.

If the dimension is very small (like the thickness of the washer), put
DistanceEnd as Start Marker and DistanceStart as End Marker.

Repeat for all lines.

[<img alt="Dimension lines" src="{{ static(drawing5.png) }}" />]({{ static(drawing5.png) }})

Then choose the text tool in the toolbar on the left and add the dimension
names. You can look them up on the
[Specification page]({{ standard_url(ISO7089) }}) by following
the source url or by checking the blt file.

In the case of the washer we have inner diameter d1, outer diameter d2 and
thickness s.

[<img alt="Dimension lines with labels" src="{{ static(drawing6.png) }}" />]({{ static(drawing6.png) }})

Now remove the guidelines by hovering over them until they change color and
then pressing delete.

### Filenames and PNG export

Now we can save-as the svg to its final destination. The filename is arbitrary
in principle, but follows a few conventions:

* The drawing goes in the drawings directory, in a subfolder named like the id of
  the collection to which the part belongs. If the same drawing can be used for
  parts from different collections, save the same file multiple times.
* If the drawing applies to more than one class, then the filename should
  follow the (function/file/module) name of the base. This can be looked up in
  the base files. Be careful that also the parameter names have to be the same
  across all classes.
* Otherwise the filename should follow the class id, which can be looked
  up on the specification page.

For the washer, the collection id is `washer`, and the drawing applies to
multiple classes of the collection, so we choose the name of the base, which is
`washer1`.

So the filename for the svg file is `drawings/washer/washer1.svg`.

We also want a png version of the drawing, so we choose `File->Export Bitmap`,
select Page for the export area and set the resolution to 300dpi. The filename
is the same as the one for the svg, just with extension `.png`. Clicking on
export exports the file, but does not close the dialog, which must be closed
manually.

Now we are done and can close Inkscape again.

### update the base file

The last step is to tell BOLTS about the drawing in the base file of the
drawing directory by adding an entry of the form:

    - filename: washer1
      author: Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
      license: CC0 1.0 <http://creativecommons.org/publicdomain/zero/1.0/>
      type: drawing-dimensions
      source: own work
      classids: [plainwasher1, plainwasher2, plainwasherforcheesehead, heavydutyplainwasher]

where classids is a list of classes that are covered by this drawing. The
filename is relative to the subdirectory of the collection and given without
extension to cover both svg and png versions. The type field distinguishes
drawings that explain the parameters and dimensions of a part from other images
that e.g. show [the location of connectors]({{ doc(openscad,basemodule) }}#adding_connectors)
