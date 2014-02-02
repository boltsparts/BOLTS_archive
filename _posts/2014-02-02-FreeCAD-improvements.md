---
  layout: post
  title: News Digest
  date: 2014-02-02 23:15:00
---

Since the last post a bunch of fixes, additions and smaller improvements happened.

<!-- more -->

None of these changes are spectacular enough to justify a own blog post. But I have been so quiet on this blog and wanted to show a sign of life, so I decided to write a post with a recap of the last weeks developments. I will just list them with short explanations:

* I reintegrated bolttools in the BOLTS git repo. This avoids submodules and all the problems and confusions they cause.
* Types for parameters in blt files files are now mandatory. I got bitten too often by strange errors that were caused by forgotten types. blt files get a bit more verbose by that, though.
* [OpenSCAD connectors]({{site.baseurl}}/2013/12/27/OpenSCAD-positioning.html) are now documented on the specification pages, see for example [here]({{site.baseurl}}/html/classes/ISO4017.html). For every connector a picture is shown that shows the position and orientation of the connector with respect to the part. I also created a bit of infrastructure to semi-automate the creation of these pictures.

[<img alt="Connector position documentation" src="{{ site.baseurl }}/images/openscad-connectors-documentation.png" style="width: 60%;"/>]({{ site.baseurl }}/images/openscad-connectors-documentation.png)

* Fabrizio Pollastri started a collection for [connecting bars]({{site.baseurl}}/html/collections/connecting_bars.html). He also uncovered a problem with FreeCAD drawings module, so drawings are still missing for this collection.
* Some users had problems connected with the [PySide Migration]({{site.baseurl}}/2014/01/13/PySide-and-Tables.html), that I could not reproduce. In the [development thread](http://forum.freecadweb.org/viewtopic.php?f=8&t=4549) on the FreeCAD forum, arcol found the solution. One needs to have the pyside-tools package installed, otherwise BOLTS would fail with a cryptic error message. Now the error message should be more informative.
* In the same thread the idea of coloring faces of parts to indicate threads was discussed, and I implemented it

[<img alt="Color coded threads" src="{{ site.baseurl }}/images/freecad-color-threads.png" style="width: 100%;"/>]({{ site.baseurl }}/images/freecad-color-threads.png)

* I added a new parameter type for angles specified in degrees. This allows to have more checks and better output for the online documentation. I also refactored the code that is responsible for that and simplified it a lot.
* In FreeCAD, parts now set the label instead of the object name. This makes BOLTS parts in the treeview nicer, as spapces are not converted to underscores.
* The Python functions that create the parts for FreeCAD can now throw ValueErrors to indicate invalid parameter combinations. The user is presented with a ErrorDialog with details about the problem.

All these improvements are available in the most current [development snapshot]({{site.baseurl}}/downloads.html).
