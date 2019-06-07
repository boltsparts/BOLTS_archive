---
  title: BLT file progress
  author: Johannes <jreinhardt@ist-dein-freund.de>
---

This post should now appear on [Planet RepRap](http://planet.arcol.hu/), hi everybody reading this from there. This is the development blog for [BOLTS]({{ url(main.index) }}). BOLTS tries to build an open standard parts library for a number of CAD applications.

BOLTS is a rather young project, but is already useable with [OpenSCAD](http://www.openscad.org/) and [FreeCAD](http://freecadweb.org/). Its youth is noticeable by the still relatively [small number of parts]({{ url(parts.index) }})), though. It is not difficult to add more parts and [well documented]({{ url(docs.index) }}), so if you are missing a part in BOLTS, or just think BOLTS is a good idea, [please help out with improving it]({{ url(main.contribute) }}).

If you want to try out BOLTS or learn more about it, you should head to its [webpage]({{ url(main.index) }}).

The rest of this post reports on recent developments of one of the important components

<!-- more -->

### Improvements to the blt file format

Most of the data for parts (dimensions, naming schemas, metadata, ...) is stored in human- and machine-readable plain text files called blt files. This data is shared between all target CAD tools and is the basis for the generation of the standard libraries. The files are marked up in [YAML](http://yaml.org/) which not only looks and feels nice, but also allows to automate many processes. The plain text nature of these files makes it easy to keep them under version control.

The user usually does not get in contact with these files, but to add new parts, blt files have to be created or edited. An example for such a blt file can be found [here](https://github.com/jreinhardt/BOLTS/blob/master/data/nut.blt).

At the moment, the format of these files is the area where most of the developments happen. On one hand the format must be flexible and expressive enough to be able to describe all the aspects of the different kinds of parts that might end up in BOLTS. On the other hand, it should be structured and consistent enough to be processable by humans and computers without being annoying. There are quite a few things left that I want to incorporate [before the next release](https://github.com/jreinhardt/BOLTS/issues?milestone=3&state=open).

One thing that I already implemented is the possibility to markup common parameter combinations. During the work on what will become [BOLTS for SolidWorks]({{ blog(2013/11/14/Marketing) }}), it became evident that the current format was not able to express all the things that are necessary to automatically generate a standard library for SolidWorks.

A part can have parameters that are discrete choices (like the thread for a bolt: M3, M4, ...) or continuous (like the length of the bolt). For FreeCAD and OpenSCAD BOLTS handles the continuous parameters by letting the user specify the value, and then constructing the part. But for SolidWorks (and also for a future STEP backend), one is restricted to a discrete set of combinations.

These sets can be quite big, for a single kind hex bolt there are hundreds of combinations of thread size and length that are available (here only for sizes M3 up to M6):

    [M3,8],  [M3,10], [M3,12], [M3,14], [M3,16], [M3,18], [M3,20], [M3,22],
    [M3,25], [M4,6],  [M4,8],  [M4,10], [M4,12], [M4,14], [M4,16], [M4,18],
    [M4,20], [M4,22], [M4,25], [M4,30], [M4,35], [M4,40], [M4,45], [M4,50],
    [M4,55], [M4,60], [M5,6],  [M5,8],  [M5,10], [M5,12], [M5,14], [M5,16],
    [M5,18], [M5,20], [M5,22], [M5,25], [M5,30], [M5,35], [M5,40], [M6,8],
    [M6,10], [M6,12], [M6,14], [M6,16], [M6,18], [M6,20], [M6,22], [M6,25],
    [M6,30], [M6,35], [M6,40], [M6,45], [M6,50], [M6,55], [M6,60], [M6,65],
    [M6,70]

Instead of writing out a list of tuples with possible combinations of lengths and thread size I chose to represent the set of combinations by a union of cartesian products of parameter values:

    - [[M3,M6], [8,10,12,14,16,18,20,22,25]]
    - [[M4, M5], [6,8,10,12,14,16,18,20,22,25,30,35,40]]
    - [[M4], [45,50,55,60]]
    - [[M6], [30,35,40,45,50,55,60,65,70]]

Each line represents all combinations of values in the first list with values of the second list. This is usually much more compact and readable. It is easy to express that no combinations of parameters should be considered:

    - [[],[]]

Also the case when the possible choices for the parameters are independent of each other, like for the size and material of a nut, is covered elegantly:

    - [[list of sizes],[list of materials]]

While this aspect is finished, there are other parts of the SolidWorks backend that are not ready yet, so for now there are no development snapshots. If you are interested in testing unfinished stuff, discussions and helping out with the development of BOLTS for Solidworks, you should head over to [this thread](http://forums.reprap.org/read.php?80,264283) in the RepRap Forums.
