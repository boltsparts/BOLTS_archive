---
  title: PySide and 2D tables
  date: 2014-01-13 17:25:00
  author: Johannes <jreinhardt@ist-dein-freund.de>
---

BOLTS has transitioned to PySide as Qt bindings and has support for 2D tables.

<!-- more -->

### PySide

Because of license considerations, [FreeCAD](http://freecadweb.org) migrates
from [PyQt](http://www.riverbankcomputing.com/software/pyqt/intro) to
[PySide](http://qt-project.org/wiki/PySide) as Python bindings for Qt.

There is a [long thread](http://forum.freecadweb.org/viewtopic.php?f=10&t=5303&start=50)
on the details of the transition in the [FreeCAD Forums](http://forum.freecadweb.org).

For BOLTS this was a bit difficult, because I want it to be compatible with all
Versions of FreeCAD on all systems, but in the end it worked out. At least I
hope. I do not have access to a Windows Computer, so I could not test that. If
you do and run FreeCAD 0.13 or 0.14, it would be great if you could test
whether the latest [development snapshot]({{ url(main.downloads) }}) works for you.

### 2D Tables

BOLTS needs to provide a way to express the relationship between the parameters
of parts. As an example, the dimensions of the head of a
[hexagon head screw]({{ standard_url(ISO4017) }}) are determined by the
diameter of the shaft.

These relationships are usually expressed by tables. For most parameters these
tables are 1D, i.e. they only depend only on one other quantity. BOLTS can
handle tables of this type for a long time.

However, sometimes a parameter depends on two other quantities at once. For
example, the wall thickness of 
[NPS Pipes](http://www.engineersedge.com/pipe_schedules.htm)
depends both on the diameter and the schedule.

Since today, BOLTS can also handle this kind of tables. I used NPS pipes as
test case while developing this feature, so they are now also contained in
BOLTS.

### Next steps

There are a few things left that I want to do before releasing BOLTS 0.3:

* I want to add the possibility to share parameter relations between several classes to avoids duplication.
* BOLTS for SolidWorks is progressing thanks to the help of Dale Dunn.
* I need to write and improve documentation for a few features.
* I want to add more parts to BOLTS.

So stay tuned

