# **************************************************************************************
# *                                                                                    *
# *    BOLTS - Open Library of Technical Specifications                                *
# *                                                                                    *
# *    Copyright (C) 2017 Bernd Hahnebach <bernd@bimstatik.org>                        *
# *                                                                                    *
# *    This library is free software; you can redistribute it and/or                   *
# *    modify it under the terms of the GNU Lesser General Public                      *
# *    License as published by the Free Software Foundation; either                    *
# *    version 2.1 of the License, or any later version.                               *
# *                                                                                    *
# *    This library is distributed in the hope that it will be useful,                 *
# *    but WITHOUT ANY WARRANTY; without even the implied warranty of                  *
# *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU                *
# *    Lesser General Public License for more details.                                 *
# *                                                                                    *
# *    You should have received a copy of the GNU Lesser General Public                *
# *    License along with this library; if not, write to the Free Software             *
# *    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA    *
# *                                                                                    *
# **************************************************************************************


import Part
from FreeCAD import Vector
from Part import makeCircle, makeLine


# ************************************************************************************************
"""
# to test copy the def in python konsole and run the following code
my_test_params = {
    'type' : 'ZNP100',
    'h' : 100,
    'c1' : 55,
    'tw' : 6.5,
    'tf' : 8,
    'l' : 500,
    'name' : 'MyTestProfile',
    'arch' : False,
}
zbeam(my_test_params, App.ActiveDocument)

"""


def zbeam(params, document):
    # key = params['type']
    h = params["h"]
    c1 = params["c1"]
    tw = params["tw"]
    tf = params["tf"]
    le = params["l"]
    name = params["name"]

    rf = tf / 2.0
    rw = tw

    # points, starting at the left upper corner, going counter-clockwise
    V1 = Vector(-0.5 * tw, 0, 0)
    V2 = Vector(-0.5 * tw + c1, 0, 0)
    V3 = Vector(-0.5 * tw + c1, tf - rf, 0)
    V4 = Vector(-0.5 * tw + c1 - rf, tf, 0)
    V5 = Vector(0.5 * tw + rw, tf, 0)
    V6 = Vector(0.5 * tw, tf + rw, 0)
    V7 = Vector(0.5 * tw, h, 0)
    V8 = Vector(0.5 * tw - c1, h, 0)
    V9 = Vector(0.5 * tw - c1, h - tf + rf, 0)
    V10 = Vector(0.5 * tw - c1 + rf, h - tf, 0)
    V11 = Vector(-0.5 * tw - rw, h - tf, 0)
    V12 = Vector(-0.5 * tw, h - tf - rw, 0)

    # circle center of the fillets, starting right bottom, going counter-clockwise
    Vc1 = Vector(-0.5 * tw + c1 - rf, tf - rf, 0)
    Vc2 = Vector(0.5 * tw + rw, tf + rw, 0)
    Vc3 = Vector(0.5 * tw - c1 + rf, h - tf + rf, 0)
    Vc4 = Vector(-0.5 * tw - rw, h - tf - rw, 0)
    normal = Vector(0, 0, 1)

    # edges
    E1 = makeLine(V1, V2)
    E2 = makeLine(V2, V3)
    E3 = makeCircle(rf, Vc1, normal, 0, 90)
    E4 = makeLine(V4, V5)
    E5 = makeCircle(rw, Vc2, normal, 180, 270)
    E6 = makeLine(V6, V7)
    E7 = makeLine(V7, V8)
    E8 = makeLine(V8, V9)
    E9 = makeCircle(rf, Vc3, normal, 180, 270)
    E10 = makeLine(V10, V11)
    E11 = makeCircle(rw, Vc4, normal, 0, 90)
    E12 = makeLine(V12, V1)

    # putting the segments together make a wire, a face and extrude it
    W = Part.Wire([E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12])
    F = Part.Face(W)

    if params["arch"]:
        from ArchStructure import makeStructure

        part = makeStructure(name=name)

        prof = document.addObject("Part::Feature", "Profile")
        prof.Shape = F
        part.Base = prof

        part.Height = le
    else:
        part = document.addObject("Part::Feature", "BOLTS_part")
        part.Label = name

        beam = F.extrude(Vector(0, 0, le))
        part.Shape = beam
