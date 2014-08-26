---
  title: BOLTS Version 0.2 released
  author: Johannes <jreinhardt@ist-dein-freund.de>
---

I am happy to officially announce the first public release of BOLTS. The aim of
BOLTS is to build a free and open-source standard parts library for CAD
applications. It does so by providing a common database that can be utilized by
many different CAD applications.

<!-- more -->

The main features provided by this release are:

- Has support for [OpenSCAD](http://www.openscad.org/) and [FreeCAD](http://freecadweb.org/).
- Uses a flexible, human- and machine-readable [data format]({{ doc_version(0.3,general,blt-files)}}) to encode information about commonly used parts.
- Allows to represent the geometry of the parts either as [OpenSCAD modules]({{ doc_version(0.3,openscad,basemodule) }}) for OpenSCAD or [Python functions]({{ doc_version(0.3,freecad,basefunction) }}) or [FCstd files]({{ doc_version(0.3,freecad,basefcstd) }}) for FreeCAD.
- Automatically generates [HTML Documentation]({{ url(parts.index) }}), an [OpenSCAD Library]({{ doc_version(0.3,openscad,usage) }}) and a [FreeCAD widget]({{ doc_version(0.3,freecad,usage) }}) that can make use of this information.
- Has extensive [Documentation]({{ url(docs.index) }}) that describes how to [contribute]({{ url(main.contribute) }}) new parts.
- Includes a integrated [license management system]({{ doc_version(0.3,general,licensing) }}) that allows to reuse existing code while ensuring license compliance.
- Provides standard parts for 135 different standards by 8 different standardisation organisations and also some parts that are not standardized.

[<img alt="FreeCAD Widget and bearing" src="{{ static(freecad-bearing.png) }}" />]({{ static(freecad-bearing.png) }})

[<img alt="OpenSCAD and bolt" src="{{ static(openscad-bolt.png) }}" />]({{ static(openscad-bolt.png) }})

However BOLTS is still at the very beginning of its development and should be
considered beta software. I invite people to
[contribute to BOLTS]({{ url(main.contribute) }}) by trying it and providing
feedback and ideas for improvement or by adding more parts.

Have fun with [this release]({{ url(main.downloads) }})
