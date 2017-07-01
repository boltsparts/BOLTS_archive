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
import math

def edge_fillet(edges,radius):
	"""
	when given a list of two lines connected lines, returns a list of three
	curves (line, arc, line) corresponding to a filleted edge
	"""
	l1 = edges[0]
	l2 = edges[1]
	assert(l1.Curve.EndPoint == l2.Curve.StartPoint)
	dir1 =l1.Curve.EndPoint - l1.Curve.StartPoint
	dir2 =l2.Curve.EndPoint - l2.Curve.StartPoint

	normal = dir1.cross(dir2)

	raw_angle = math.asin(normal[2]/dir1.Length/dir2.Length)
	#This is the smaller angle enclosed by the two lines in radians
	angle = math.pi - abs(raw_angle)

	#to find the transition points of the fillet, we consider a rectangular
	#triangle with one kathete equal to the radius and the other one lying on
	#one of the input lines with length a
	a = radius/math.tan(0.5*angle)
	#parameter per length
	ppl1 = (l1.Curve.LastParameter-l1.Curve.FirstParameter)/l1.Curve.length()
	ppl2 = (l2.Curve.LastParameter-l2.Curve.FirstParameter)/l2.Curve.length()

	t1 = l1.Curve.value(l1.Curve.LastParameter - a*ppl1)
	t2 = l2.Curve.value(l1.Curve.FirstParameter + a*ppl2)

	#to fine the center of the fillet radius, we construct the angle bisector
	#between the two input lines, and get the distance of the center from the
	#common point by a trigonometric consideration
	bis = Part.makeLine(l1.Curve.EndPoint,(t1+t2).scale(0.5,0.5,0.5))
	pplb = (bis.Curve.LastParameter-bis.Curve.FirstParameter)/bis.Curve.length()
	d = radius/math.sin(0.5*angle)
	center = bis.Curve.value(bis.Curve.FirstParameter + d*pplb)

	#to construct the circle we need start and end angles
	r1 = t1 - center
	r2 = t2 - center
	if raw_angle > 0:
		alpha1 = math.atan2(r1[1],r1[0])*180/math.pi
		alpha2 = math.atan2(r2[1],r2[0])*180/math.pi
	else:
		alpha2 = math.atan2(r1[1],r1[0])*180/math.pi
		alpha1 = math.atan2(r2[1],r2[0])*180/math.pi
		normal *= -1

	return [Part.makeLine(l1.Curve.StartPoint,t1),
		Part.makeCircle(radius,center,normal,alpha1,alpha2),
		Part.makeLine(t2,l2.Curve.EndPoint)]


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
        lines.append(makeLine(plast,pcur))

    #upper left quadrant
    for i in range(len(vertices)-2,-1,-1):
        plast = pcur
        pcur = Vector(vertices[i])
        pcur[0] *= -1
        lines.append(makeLine(plast,pcur))

    #lower left quadrant
    for i in range(1,len(vertices)):
        plast = pcur
        pcur = Vector(vertices[i])
        pcur[0] *= -1
        pcur[1] *= -1
        lines.append(makeLine(plast,pcur))

    #lower right quadrant
    for i in range(len(vertices)-2,-1,-1):
        plast = pcur
        pcur = Vector(vertices[i])
        pcur[1] *= -1
        lines.append(makeLine(plast,pcur))

    fillets = [
        (slice(0,2), r1), (slice(1,3), r2), (slice(5,7),  r2), (slice(6,8),  r1),
        (slice(8,10),r1), (slice(9,11),r2), (slice(13,15),r1), (slice(14,16),r2)
    ]
    #add fillets in reverse order to not disturb the counting, as edges are added
    fillets.reverse()
    for fillet,r in fillets:
        lines[fillet] = edge_fillet(lines[fillet],r)

    F = Part.Face(Part.Wire(lines))

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
            part.Shape = beam.removeSplitter()
