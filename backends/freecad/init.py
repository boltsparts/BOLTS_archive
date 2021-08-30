# BOLTS - Open Library of Technical Specifications
# Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
# Copyright (C) 2021 Bernd Hahnebach <bernd@bimstatik.org>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from os import listdir
from os.path import dirname
from os.path import exists
from os.path import join

import FreeCAD
import FreeCADGui
# TODO check if Gui is up, in FreeCADCmd mode importing by Python should be possible
import Part

from .bolttools import blt
from .bolttools import freecad


try:
    from PySide import QtCore
except ImportError:
    FreeCAD.Console.PrintError(
        "uic import failed. Make sure that the pyside tools are installed"
    )
    raise
# test if method FreeCADGui.PySideUic.loadUiType works
try:
    a_widget_path = join(dirname(__file__), "gui", "value_widget.ui")
    from FreeCADGui import PySideUic as uic
    Ui_ValueWidget, QValueWidget = uic.loadUiType(a_widget_path)
except ImportError:
    FreeCAD.Console.PrintError(
        "The ui import failed. Make sure that the 'loadUiType' "
        "method from FreeCADGui.PySideUic works proper."
    )
    raise


from .gui import freecad_bolts as boltsgui
# import repo
rootpath = dirname(__file__)
repo = blt.Repository(rootpath)
# print(repo)
freecad_db = freecad.FreeCADData(repo)
widget = None


def show_widget():
    global widget
    if widget is None:
        widget = boltsgui.BoltsWidget(repo,freecad_db)

        mw = FreeCADGui.getMainWindow()
        mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, widget)
    else:
        widget.show()


def make_drawing(scale,obj):
    doc = FreeCAD.ActiveDocument
    page = doc.addObject("Drawing::FeaturePage","Page")
    page.Template = join(rootpath,"assets","template.svg")

    # front, side right, side left, rear, top, bottom, iso
    directions = [(0.,0.,1.),(1.,0.,0.),(-1.,0.,0.),(0.,0.,-1.),(0.,-1.,0.),(0.,1.,0.),(1.,1.,1.)]
    # x center positions
    positions = [(110.,100.),(40.,100.),(180.,100.),(250.,100.),(110.,35.),(110.,165.),(215.,35.)]
    rotations = [0,0,0,0,270,270,0]
    for i in range(7):
        view = doc.addObject("Drawing::FeatureViewPart","View%d" % i)
        view.Source = obj
        view.Direction = directions[i]
        view.X = positions[i][0]
        view.Y = positions[i][1]
        view.Rotation = rotations[i]
        view.Scale = scale
        page.addObject(view)


def list_names(doc):
    print("Label   Name")
    print("------------")
    for part in doc.findObjects():
        if isinstance(part,Part.Feature):
            print("%s    %s" % (part.Label, part.Name))


def add_name(id,in_params=None):
    name = repo.names[id]
    cl = repo.class_names.get_src(name)
    if not in_params:
        in_params = get_free_in_params(cl)

    params = cl.parameters.collect(in_params)
    params['name'] = name.labeling.get_nice(params)

    #add part
    base = freecad_db.base_classes.get_src(cl)
    coll = repo.collection_classes.get_src(cl)
    boltsgui.add_part(coll,base,params,FreeCAD.ActiveDocument)


def add_standard(id,in_params=None):
    standard = repo.standards[id]
    cl = repo.class_standards.get_src(standard)
    if not in_params:
        in_params = get_free_in_params(cl)

    params = cl.parameters.collect(in_params)
    params['name'] = standard.labeling.get_nice(params)

    # add part
    base = freecad_db.base_classes.get_src(cl)
    coll = repo.collection_classes.get_src(cl)
    boltsgui.add_part(coll,base,params,FreeCAD.ActiveDocument)


def get_free_in_params(cl):
    base = freecad_db.base_classes.get_src(cl)
    params = cl.parameters.union(base.parameters)
    free_params = params.free

    in_params = {}
    for p in free_params:
        # p_type = params.types[p]  # not used
        default_value = params.defaults[p]
        in_params[p] = default_value
    return in_params
