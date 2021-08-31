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

from PySide import QtCore
from PySide import QtGui

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
        "PySide import failed. Make sure that the pyside tools are installed"
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
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        mw = FreeCADGui.getMainWindow()
        widget = QtGui.QDockWidget("BOLTS Parts Selector", mw)
        widget.setWidget(boltsgui.BoltsWidget(repo, freecad_db))
        mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, widget)
        QtGui.QApplication.restoreOverrideCursor()
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
    """
    doc: FreeCAD document object
    BOLTS.list_names(document)
        lists object Labels and object Names
        off all Part and Part.Feature document objects
    """
    print("Label   Name")
    print("------------")
    for part in doc.findObjects():
        if isinstance(part, Part.Feature):
            print("%s    %s" % (part.Label, part.Name))


# ************************************************************************************************
# add BOLTS parts by Python
def add_part_by_classid(classid, in_params=None):
    """
    BOLTS.add_part_by_name(classid, [in_params])

        Add a BOLTS part by Python according the classid

        classid:
            - get the classid from *.blt file

        in_params:
            - dictionary of all free Parameters
            - if ommited, the default parameters are taken (see Default in *.blt file)
            - if a key is missing in Parameter, the default is added
            - get the default parameters by BOLTS.get_default_params(SaveClassName)
            - if the key "name" is given, this will be used as FreeCAD object name

        Examples:
            BOLTS.add_part_by_classid("ibeam_heb")
            BOLTS.add_part_by_classid("ibeam_heb", {"type": "HEB500", "name": "my_profile"})
            BOLTS.add_part_by_classid("ibeam_heb", {"type": "HEB500", "l" : 50, "arch" : True})
            BOLTS.add_part_by_classid("tslot20x20", {"l": 5})
            BOLTS.add_part_by_classid("vslot20x60", {"l": 5, "finish": "Clear anodized"})
    """
    name = repo.names[get_name(classid)]
    cl = repo.class_names.get_src(name)

    # get params and add part
    _add_part(cl, in_params)


def add_part_by_name(save_class_name, in_params=None):
    """
    BOLTS.add_part_by_name(save_class_name, [in_params])

        Add a BOLTS part by Python according the class name

        in_params:
            - dictionary of all free Parameters
            - if ommited, the default parameters are taken (see Default in *.blt file)
            - if a key is missing in Parameter, the default is added
            - get the default parameters by BOLTS.get_default_params(SaveClassName)
            - if the key "name" is given, this will be used as FreeCAD object name

        Examples:
            BOLTS.add_part_by_name("HEBProfile")
            BOLTS.add_part_by_name("HEAProfile", {"type": "HEA300", "name": "my_profile"})
            BOLTS.add_part_by_name("HEBProfile", {"type": "HEB500", "l" : 50, "arch" : True})
            BOLTS.add_part_by_name("TSlotExtrusion20x20", {"l": 5})
            BOLTS.add_part_by_name("V_slot20x60mm", {"l": 5, "finish": "Clear anodized"})
    """
    name = repo.names[save_class_name]
    cl = repo.class_names.get_src(name)

    # get params and add part
    _add_part(cl, in_params)


def add_part_by_standard(save_standard_name, in_params=None):
    """
    BOLTS.add_part_by_standard(save_standard_name, [in_params])

        Add a BOLTS part by Python according the national standard name

        in_params:
            - dictionary of all free Parameters
            - if ommited, the default parameters are taken (see Default in *.blt file)
            - if a key is missing in Parameter, the default is added
            - get the default parameters by BOLTS.get_default_params(SaveClassName)
            - if the key "name" is given, this will be used as FreeCAD object name

        Examples:
            BOLTS.add_part_by_standard("DIN1025_2")
            BOLTS.add_part_by_standard("DIN1025_2", {"type": "HEB500", "name": "my_profile"})
            BOLTS.add_part_by_standard("DIN1025_2", {"type": "HEB500", "l" : 50, "arch" : True})
            BOLTS.add_part_by_standard("DINENISO4017")
            BOLTS.add_part_by_standard("DIN933", {"name": "my_profile"})
            BOLTS.add_part_by_standard("DIN933", {"key": "M10", "l": 120, "name": "my_profile"})
    """
    standard = repo.standards[save_standard_name]
    cl = repo.class_standards.get_src(standard)

    # get params and add part
    _add_part(cl, in_params)


"""
# TODO:
# the following has errors, FIXME
BOLTS.add_part_by_standard("DIN933")
"""


# ************************************************************************************************
# helper
def _get_default_params(cl):

    base = freecad_db.base_classes.get_src(cl)
    params = cl.parameters.union(base.parameters)
    free_params = params.free

    default_params = {}
    for p in free_params:
        # p_type = params.types[p]  # not used
        default_value = params.defaults[p]
        default_params[p] = default_value
    return default_params


def _add_missing_inparams(cl, params):

    # print(cl.id)
    # print(params)
    default_params = _get_default_params(cl)
    for def_key in default_params:
        if def_key not in params:
            params[def_key] = default_params[def_key]
            print(
                "Added default parameter: {}: {}"
                .format(def_key, default_params[def_key])
            )
    return params


def _add_part(cl, in_params):

    # params
    if not in_params:
        in_params = _get_default_params(cl)
    all_params = _add_missing_inparams(cl, in_params)
    all_params = cl.parameters.collect(in_params)

    # add name to all_params
    if "name" not in all_params:
        name = repo.names[get_name(cl.id)]
        all_params["name"] = name.labeling.get_nice(all_params)

    # add part
    base = freecad_db.base_classes.get_src(cl)
    coll = repo.collection_classes.get_src(cl)
    boltsgui.add_part(
        coll,
        base,
        all_params,
        FreeCAD.ActiveDocument
    )
