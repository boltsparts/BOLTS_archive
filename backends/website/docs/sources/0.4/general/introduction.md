---
  title: A short introduction to BOLTS
  audience: contributors
---

The aim of BOLTS is to build a free and open-source standard parts library that
is not tied to a specific CAD applications. For this reason all the data
necessary to make the parts available is structured in a certain way: There is
backend independent data and backend specific data, where backend refers to the
different CAD applications (for now FreeCAD and OpenSCAD). By making this
separation, if a part is available in one CAD application, the only thing that
is required to make it available in another one is to add the necessary backend
specific data.

### Backend independent data

Very often there exist several similar or even identical standards for one
part, issued by different organisations. For this reason, BOLTS has the concept
of a class of parts, where one class can cover several identical standards. To
specify a class of parts, we have to specify information about the various
dimensions of the part, tables with values for these dimensions, a description,
the standards that this class covers, a drawing of the part and so on. The way
in which the geometry of the part is specified is different for different CAD
applications and therefore belongs to the backend specific data.

BOLTS provides another level of organisation, the collection. A collection
contains several classes, so that similar but not identical classes can be
grouped together. All the information about the classes in a collection is
stored in a blt file.

### Backend specific data

There is also data required to create a 3D representation of a part in a CAD
tool. For OpenSCAD we use a module definition in a scad file, for FreeCAD a
python function. These are also called base modules or base functions, or base
geometries when referring to any of them. Together with a base file containing
metadata this forms the backend specific data.

### Synergy

Very often several classes can share the base geometry. For example BOLTS nows
about 18 different standards for washers. These are covered by 5 different
classes, which only need 2 different base geometries.

A picture says more than thousand words. The two boxes on the left (Standards
and Classes) are backend independent. The backend specific part is just 2 base
geometries for each applications:


[<img alt="Washer collection" src="{{ static(washer.png) }}" />]({{ static(washer.png) }})

### Summary

To summarize again:
 - The data in BOLTS is either backend independent or backend specific.
 - A class covers zero or more standards, a collection contains one or more classes
 - For a class to be usable in an application, BOLTS must have a suitable base geometry for that class.
