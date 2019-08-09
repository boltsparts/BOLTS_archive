# **************************************************************************************
# *                                                                                    *
# *    BOLTS - Open Library of Technical Specifications                                *
# *                                                                                    *
# *    Copyright (c) 2014 Fabrizio Pollastri <f.pollastri@inrim.it>                    *
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


from FreeCAD import Base
import Part


def plate_flange(params, document):
    d1 = params["d1"]
    k = params["k"]
    D = params["D"]
    b = params["b"]
    d2 = params["d2"]
    bn = params["bn"]
    name = params["name"]

    part = document.addObject("Part::Feature", "BOLTS_part")
    part.Label = name

    flange(d1, k, D, b, d2, bn, False, part)


def blind_flange(params, document):
    d1 = params["d1"]
    k = params["k"]
    D = params["D"]
    b = params["b"]
    d2 = params["d2"]
    bn = params["bn"]
    name = params["name"]

    part = document.addObject("Part::Feature", "BOLTS_part")
    part.Label = name

    flange(d1, k, D, b, d2, bn, True, part)


def flange(d1, k, D, b, d2, bn, blind, part):

    # ********** flange disk **********
    p0 = Base.Vector(0.0, 0.0, 0.0)
    caxis = Base.Vector(0.0, 0.0, 1)
    disk = Part.makeCylinder(0.5 * D, b, p0, caxis)

    # if not a blind flange, make the inner hole.
    if not blind:
        hole = Part.makeCylinder(0.5 * d1, b, p0, caxis)
        disk = disk.cut(hole).removeSplitter()

    # ********** bolts holes **********
    h0 = Base.Vector(0.5 * k, 0.0, 0.0)
    hole = Part.makeCylinder(0.5 * d2, b, h0, caxis)
    holes = hole.copy()
    for i in range(1, int(bn)):
        nhole = hole.copy()
        nhole.rotate(p0, caxis, i * 360.0 / bn)
        holes = holes.fuse(nhole)
    # drill holes
    flange = disk.cut(holes).removeSplitter()

    # ********** chamfer all edges **********
    part.Shape = flange.makeChamfer(0.05 * b, flange.Edges)
