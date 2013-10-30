---
  layout: post
  title: BOLTS Version 0.2 released
---

I am happy to officially announce the first public release of BOLTS. The aim of
BOLTS is to build a free and open-source standard parts library for CAD
applications. It does so by providing a common database that can be utilized by
many different CAD applications.

<!-- more -->

The main features provided by this release are:
- Has support for <a href="http://www.openscad.org/">OpenSCAD</a> and <a href="http://freecadweb.org/">FreeCAD</a>.
- Uses a flexible, human- and machine-readable [data format]({{site.baseurl}}/doc/general/blt-files.html) to encode information about commonly used parts.
- Allows to represent the geometry of the parts either as [OpenSCAD modules]({{site.baseurl}}/doc/openscad/basemodule.html) for OpenSCAD or [Python functions]({{site.baseurl}}/doc/freecad/basefunction.html) or [FCstd files]({{site.baseurl}}/doc/freecad/basefcstd.html) for FreeCAD.
- Automatically generates [HTML Documentation]({{site.baseurl}}/html/index.html), an [OpenSCAD Library]({{site.baseurl}}/doc/openscad/usage.html) and a [FreeCAD widget]({{site.baseurl}}/doc/freecad/usage.html) that can make use of this information.
- Has extensive [Documentation]({{site.baseurl}}/doc/index.html) that describes how to [contribute]({{site.baseurl}}/contribute.html) new parts.
- Includes a integrated [license management system]({{site.baseurl}}/doc/general/licensing.html) that allows to reuse existing code while ensuring license compliance.
- Provides standard parts for 135 different standards by 8 different standardisation organisations.

However BOLTS is still at the very beginning of its development and should be
considered beta software. I invite people to
[contribute to BOLTS]({{site.baseurl}}/contribute.html) by trying it and
providing feedback and ideas for improvement or by adding more parts.

Have fun with [this release]({{site.baseurl}}/downloads.html)
