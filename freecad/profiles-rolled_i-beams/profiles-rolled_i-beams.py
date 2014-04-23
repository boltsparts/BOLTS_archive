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
import Part, Arch
from math import sin,cos,fabs

def ibeam_parallel_flange(params,document):
        key = params['type']
        h = params['h']
        b = params['b']
        tf = params['tf']
        tw = params['tw']
        r = params ['r']
        l = params['l']
        name = params['name']



        # lower flange, starting at the left web fillet, going against clockwise
        Vlf1 = Vector((-tw/2-r),(-h/2+tf),0)
        Vlf2 = Vector(-b/2,(-h/2+tf),0)
        Vlf3 = Vector(-b/2,-h/2,0)
        Vlf4 = Vector(b/2,-h/2,0)
        Vlf5 = Vector(b/2,(-h/2+tf),0)
        Vlf6 = Vector((tw/2+r),(-h/2+tf),0)
        Llf1 = makeLine(Vlf1,Vlf2)
        Llf2 = makeLine(Vlf2,Vlf3)
        Llf3 = makeLine(Vlf3,Vlf4)
        Llf4 = makeLine(Vlf4,Vlf5)
        Llf5 = makeLine(Vlf5,Vlf6)

        # upper flange, starting at the rigth web fillet, going clockwise
        Vuf1 = Vector(tw/2+r,(h/2-tf),0)
        Vuf2 = Vector(b/2,(h/2-tf),0)
        Vuf3 = Vector(b/2,h/2,0)
        Vuf4 = Vector(-b/2,h/2,0)
        Vuf5 = Vector(-b/2,(h/2-tf),0)
        Vuf6 = Vector((-tw/2-r),(h/2-tf),0)
        Luf1 = makeLine(Vuf1,Vuf2)
        Luf2 = makeLine(Vuf2,Vuf3)
        Luf3 = makeLine(Vuf3,Vuf4)
        Luf4 = makeLine(Vuf4,Vuf5)
        Luf5 = makeLine(Vuf5,Vuf6)

        # web, starting rigth bottom, going against clockwise
        Vw1 = Vector(tw/2,(-h/2+tf+r),0)
        Vw2 = Vector(tw/2,(h/2-tf-r),0)
        Vw3 = Vector(-tw/2,(h/2-tf-r),0)
        Vw4 = Vector(-tw/2,(-h/2+tf+r),0)
        Lw1 = makeLine(Vw1,Vw2)
        Lw2 = makeLine(Vw3,Vw4)

        # center of the fillets, starting right bottom, going against clockwise
        Vfc1 = Vector((tw/2+r),(-h/2+tf+r),0)
        Vfc2 = Vector((tw/2+r),(h/2-tf-r),0)
        Vfc3 = Vector((-tw/2-r),(h/2-tf-r),0)
        Vfc4 = Vector((-tw/2-r),(-h/2+tf+r),0)
        normal = Vector(0,0,1)
        Cfc1 = makeCircle(r,Vfc1,normal,180,270)
        Cfc2 = makeCircle(r,Vfc2,normal, 90,180)
        Cfc3 = makeCircle(r,Vfc3,normal,  0, 90)
        Cfc4 = makeCircle(r,Vfc4,normal,270,  0)

        # putting the segments together make a wire, a face and extrude it
        W = Part.Wire([Llf1,Llf2,Llf3,Llf4,Llf5,Cfc1,Lw1,Cfc2,Luf1,Luf2,Luf3,Luf4,Luf5,Cfc3,Lw2,Cfc4])
        F = Part.Face(W)


        if params['arch']:
                part = Arch.makeStructure(name=name)

                prof = document.addObject("Part::Feature","Profile")
                prof.Shape = F
                part.Base = prof

                part.Height = l
        else:
                part = document.addObject("Part::Feature","BOLTS_part")
                part.Label = name

                beam = F.extrude(Vector(0,0,l))
                part.Shape = beam



def ibeam_angled_flange(params,document):
    h = params['h']
    b = params['b']
    tf = params['tf']
    tw = params['tw']
    hw = params ['hw']
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
        Vector((0.5*tw,0,0)),
        Vector((0.5*tw,f,0)),
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
            if fabs(fabs(v.Point[0]) - 0.5*tw) > 1e-8 or fabs(fabs(v.Point[1]) - f) > 1e-8:
                break
        else:
            inner_fillets.append(edge)
        for v in edge.Vertexes:
            if fabs(fabs(v.Point[0]) - 0.5*b) > 1e-8 or fabs(fabs(v.Point[1]) - (0.5*h-g)) > 1e-8:
                break
        else:
            outer_fillets.append(edge)

    part.Shape = beam.makeFillet(r1,inner_fillets).makeFillet(r2,outer_fillets).removeSplitter()
