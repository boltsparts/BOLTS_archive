---
  title: How to install BOLTS for OpenSCAD
  audience: user
---


### Download

You can download a stable release or development snapshot of BOLTS for OpenSCAD
from the [download page]({{ url(main.downloads) }}). There are different
archive types and licenses available, if you do not know which one you want,
you should be fine with the GPL 3.0 zip version.

### Local installation

Just extract all the files in the archive in a directory. You can now use BOLTS
for designs in this folder only. This is a good choice if you want to test
development snapshots.

### Global installation

To be able to use BOLTS everywhere, you need to install it globally. The best
way to do it is to extract all files from the archive into your user library
directory. The path for this directory depends on your system:

 - Windows: `My Documents\OpenSCAD\libraries`
 - Linux: `$HOME/.local/share/OpenSCAD/libraries`
 - MacOS: `$HOME/Documents/OpenSCAD/libraries`

### Test

To make sure that the installation succeeded, start OpenSCAD, type

    include <BOLTS.scad>
    DIN931();

and compile. If you installed locally, OpenSCAD needs to be started from the
directory, or you can save the two lines into a scad file in the directory.

The preview window should now show a hexagon bolt.

[<img alt="Successful installation" src="{{ static(openscad-installation.png) }}" />]({{ static(openscad-installation.png) }})

