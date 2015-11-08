---
  title: Installing BOLTS for FreeCAD
  audience: user
---

### Download a BOLTS for FreeCAD release

You can find the most recent BOLTS for FreeCAD release at the [Downloads Page]({{ url(main.downloads) }}).

There are different archive types available, if you are unsure, which to choose use the zip.

### Extract it to your macro folder

You can look up the location of the macro folder in the preferences: Choose
Edit->Preferences, in the dialog select the macro tab. The macro path is listed
there. On linux the macro folder is usually located at `~/.FreeCAD`.

When you are done the macro folder should contain a subfolder called BOLTS and
a file called start_bolts.FCMacro

The installation is now complete.

### Try it

Start FreeCAD and choose <code>Macros</code> from the <code>Macro</code> menu.
In the dialog that pops up select <code>start_bolts.FCMacro</code> and click on
execute.

### Troubleshooting

If you get an error that says something like:

    No module named yaml

then this is because the yaml library for python is not installed. If you are
using Linux, then you can usually get it using your package manager. If you are
on windows you can get an installer [here](http://pyyaml.org/wiki/PyYAML); you
have to install YAML for the version of Python (first two digits) that is
bundled with FreeCAD. You can find out which version that is from the first
line of the python console in FreeCAD. If it is not opened, you can make it
visible by checking it in the Menu View under point Views.

If you get an error that says something like:

    No module named importlib

then you are using a older version of python where the importlib library is not
included. You can get it [here](https://pypi.python.org/pypi/importlib/1.0.2).
For importlib no convenient installer is available for windows. Instructions on
how to install a python module without an installer can be found
[here](http://docs.python.org/2/install/index.html). Again you should use the
version for the python version bundled with FreeCAD.

If you get a message that says

    uic import failed. Make sure that the pyside tools are installed
    
or an error message that says

    ImportError: No module named pysideuic

then there is a part of the PySide Qt bindings missing. For Debian and Ubuntu
this is contained in the package pyside-tools.

### Windows

On Windows it is sometimes necessary to copy the python dependencies to

    <path to FreeCAD installation>\bin\Lib\site-packages

so that they are picked up by the python version shipped with FreeCAD. See also
[this
thread](http://forum.freecadweb.org/viewtopic.php?f=8&t=4549&start=240#p80010)
in the FreeCAD forums.

If you get different errors, than please try the latest development snapshot.
If it still does not work, please report that problem, and help me figure it
out. The simplest way to do so is to use the comments below, but there is a
number of of other places where you can report problems, a list can be found
[on the contribute page]({{ url(main.contribute) }}).

### Next steps

If you want, you can [set up a toolbar button]({{ doc(freecad,toolbar) }}), or
you can read [how to use BOLTS for FreeCAD]({{ doc(freecad,usage) }}).
