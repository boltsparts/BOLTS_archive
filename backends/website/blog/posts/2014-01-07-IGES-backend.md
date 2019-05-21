---
  title: IGES Backend
  date: 2014-01-07 12:30:00
  author: Johannes <jreinhardt@ist-dein-freund.de>
---

I recently merged a bit of code that allows to export all the parts available
in BOLTS for FreeCAD to [IGES](http://en.wikipedia.org/wiki/IGES). IGES is a
standardized file format for CAD data that is widely supported. Now BOLTS can
be used by users of CAD applications besides FreeCAD and OpenSCAD.

<!-- more -->

In contrast to BOLTS for FreeCAD and OpenSCAD, where a certain size or
variation of a part is created from a parametric model, the IGES distribution
contains one file for each size and variation of a part. This results in a lot
of files (about 1000), and forces us to choose which sizes should be included
at export time.

This choice is codified in the blt files in form of common parameter
combinations, I have [blogged about this]({{ blog(2013/11/29/BLT-file-progress) }})
a while ago. I have not yet specified common parameters for all classes of
parts, and BOLTS can not guess them in some cases. These parts are then ignored
and not exported to IGES. A list of parts that miss common parameter
information can be found on the [tasks page]({{ url(main.tasks) }}). One
only has to lookup a few vendor sites on the internet and find the most common
sizes and variations of parameters for the part and enter them into the blt
file.

### What about STEP?

STEP is a more recent and more powerful exchange format for CAD data. It is
also widely supported by CAD applications. However, FreeCAD has a few issues
with STEP, which cause problems when exporting the BOLTS parts. There is a bit
of discussion around these issues and how to resolve them in the
[BOLTS github issue](https://github.com/jreinhardt/BOLTS/issues/4)
 and in the [FreeCAD forum](http://forum.freecadweb.org/viewtopic.php?f=10&t=5086).

I decided to postpone export to STEP, and go with IGES instead, as this works
without problems.

### File size and compression

As mentioned earlier, the IGES distribution consists of a lot of files, many of
which are very similar. It currently has around 1600 files with a total size of
around 120 MByte. These files are compressed into a single file which can then
be downloaded from the [download section]({{ url(main.downloads) }}).

In contrast to the FreeCAD and OpenSCAD distributions of BOLTS, which are
available both as zip and tar.gz, the IGES distribution is only available as
tar.xz, because this format achieves significantly better compression for this
kind of content. The 120 MByte of IGES files result in a 12 MByte zip file, but
only in a 2 MByte tar.xz file.

On Windows, tar.xz files can be decompressed using the [7z tool](http://www.7-zip.org/). 
On most Linux distributions the common tools to work with compressed data can
handle tar.xz, or at least packages are available for xz-tools.
