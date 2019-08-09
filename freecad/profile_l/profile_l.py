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
from BOLTS.freecad.profile_l.profile_l import lbeam_parallel_flange_equal as equallnp
# to test copy the def in python konsole and run the following code
my_test_params = {
    "type" : "LNP100x10",
    "a" : 100,
    "t" : 10,
    "r1" : 12,
    "r2" : 6,
    "l" : 500,
    "name" : "MyTestProfile",
    "arch" : False
}
equallnp(my_test_params, App.ActiveDocument)

"""


def lbeam_parallel_flange_equal(params, document):
    # use unequal method for equals too
    # we just need te define params["b"], which equal to params["a"] for equals LNP
    params["b"] = params["a"]
    lbeam_parallel_flange_unequal(params, document)


# ************************************************************************************************
"""
from BOLTS.freecad.profile_l.profile_l import lbeam_parallel_flange_unequal as nonequallnp
# to test copy the def in python konsole and run the following code
my_test_params = {
    "type" : "LNP100x10",
    "a" : 200,
    "b" : 100,
    "t" : 10,
    "r1" : 12,
    "r2" : 6,
    "l" : 500,
    "name" : "MyTestProfile",
    "arch" : False
}
nonequallnp(my_test_params, App.ActiveDocument)

"""


def lbeam_parallel_flange_unequal(params, document):
    # key = params["type"]
    a = params["a"]
    b = params["b"]
    t = params["t"]
    ri = params["r1"]
    ro = params["r2"]
    le = params["l"]
    name = params["name"]

    # points, starting at the left upper corner, going counter-clockwise
    V1 = Vector(0, 0, 0)
    V2 = Vector(b, 0, 0)
    V3 = Vector(b, t - ro, 0)
    V4 = Vector(b - ro, t, 0)
    V5 = Vector(t + ri, t, 0)
    V6 = Vector(t, t + ri, 0)
    V7 = Vector(t, a - ro, 0)
    V8 = Vector(t - ro, a, 0)
    V9 = Vector(0, a, 0)

    # circle center of the fillets, starting right bottom, going counter-clockwise
    Vc1 = Vector(b - ro, t - ro, 0)
    Vc2 = Vector(t + ri, t + ri, 0)
    Vc3 = Vector(t - ro, a - ro, 0)
    normal = Vector(0, 0, 1)

    # edges
    E1 = makeLine(V1, V2)
    E2 = makeLine(V2, V3)
    E3 = makeCircle(ro, Vc1, normal, 0, 90)
    E4 = makeLine(V4, V5)
    E5 = makeCircle(ri, Vc2, normal, 180, 270)
    E6 = makeLine(V6, V7)
    E7 = makeCircle(ro, Vc3, normal, 0, 90)
    E8 = makeLine(V8, V9)
    E9 = makeLine(V9, V1)

    # putting the segments together make a wire, a face and extrude it
    W = Part.Wire([E1, E2, E3, E4, E5, E6, E7, E8, E9])
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
