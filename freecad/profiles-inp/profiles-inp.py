#BOLTS - Open Library of Technical Specifications
#Copyright (C) 2014 Bernd Hahnebach <bernd@bimstatik.org>
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA


from FreeCAD import Vector
from Part import makeCircle, makeLine
import Part
from math import sin,cos,fabs

def ibeam_angled_flange(params,document):
    h = params['h']
    b = params['b']
    t = params['t']
    s = params['s']
    d = params ['d']
    f = params ['f']
    g = params ['g']
    r1 = params ['r1']
    r2 = params ['r2']
    l = params['l']
    name = params['name']

    part = document.addObject("Part::Feature","BOLTS_part")
    part.Label = name

    #The profile is symmetric, we store the positions relative to the
    #origin for upper right quarter
    vertices = [
        Vector((0.5*s,0,0)),
        Vector((0.5*s,f,0)),
        Vector((0.5*b,0.5*h-g,0)),
        Vector((+0.5*b,0.5*h,0)),
        Vector((0,0.5*h,0)),
    ]
    lines = []

    plast = None
    pcur = vertices[0]

    #upper right quadrant
    for i in range(1,len(vertices)):
        plast = pcur
        pcur = Vector(vertices[i])
        lines.append(makeLine(pcur,plast))

    #upper left quadrant
    for i in range(len(vertices)-2,-1,-1):
        plast = pcur
        pcur = Vector(vertices[i])
        pcur[0] *= -1
        lines.append(makeLine(pcur,plast))

    #lower left quadrant
    for i in range(1,len(vertices)):
        plast = pcur
        pcur = Vector(vertices[i])
        pcur[0] *= -1
        pcur[1] *= -1
        lines.append(makeLine(pcur,plast))

    #lower right quadrant
    for i in range(len(vertices)-2,-1,-1):
        plast = pcur
        pcur = Vector(vertices[i])
        pcur[1] *= -1
        lines.append(makeLine(pcur,plast))

    beam  = Part.Face(Part.Wire(lines)).extrude(Vector(0,0,l))

    inner_fillets = []
    outer_fillets = []

    for edge in beam.Edges:
        for v in edge.Vertexes:
            if fabs(fabs(v.Point[0]) - 0.5*s) > 1e-8 or fabs(fabs(v.Point[1]) - f) > 1e-8:
                break
        else:
            inner_fillets.append(edge)
        for v in edge.Vertexes:
            if fabs(fabs(v.Point[0]) - 0.5*b) > 1e-8 or fabs(fabs(v.Point[1]) - (0.5*h-g)) > 1e-8:
                break
        else:
            outer_fillets.append(edge)

    part.Shape = beam.makeFillet(r1,inner_fillets).makeFillet(r2,outer_fillets).removeSplitter()
