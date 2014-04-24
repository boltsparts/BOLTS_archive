#BOLTS - Open Library of Technical Specifications
#Copyright (C) 2014 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
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

#the size of the inner square
d = 5.68 + 3/math.sqrt(2)
w = 20

#outline
vertices_corner = [
	(0.5*d,0,0),
	(0.5*d,0.5*5.68,0),
	(0.5*w - 1.8 - 1.64,0.5*w - 1.8 - 1.64 - 1.5/math.sqrt(2),0),
	(0.5*w - 1.8,0.5*w - 1.8 - 1.64 - 1.5/math.sqrt(2),0),
	(0.5*w - 1.8,0.5*5.68,0),
	(0.5*w,0.5*5.68+1.8,0),
	(0.5*w,0.5*w,0)
]

#big spaces
vertices_inner = [
	(0.5*d,0,0),
	(0.5*d,0.5*5.68,0),
	(0.5*w-2.7,0.5*w-1.8-1.96,0),
	(0.5*w-2.7,0.5*w-1.8,0),
	(0.5*w,0.5*w-1.8,0),
]

#corner holes
vertices_hole = [
	(0.5*w - 1.8,0.5*w - 1.8 - 1.64 - 1.5/math.sqrt(2)+1.07,0),
	(0.5*w - 1.8,0.5*w-1.8,0),
	(0.5*w - 1.8 - 1.64 - 1.5/math.sqrt(2)+1.07,0.5*w - 1.8,0),
	(0.5*w - 1.8,0.5*w - 1.8 - 1.64 - 1.5/math.sqrt(2)+1.07,0)
]

def vslot(outer_symmetry,fillets,corner_offset,circle_offsets,space_offsets):
	#build the outline
	lines = []

	vlast = None
	vcur = Vector(vertices_corner[0])

	for part in outer_symmetry:
		for i in range(part[0],part[1],part[2]):
			vlast = vcur
			vcur = Vector(vertices_corner[i])
			vcur[0],vcur[1] = part[4]*vcur[part[5]]+part[3],part[6]*vcur[part[7]]
			lines.append(makeLine(vlast,vcur))

	#add fillets
	for fillet in fillets:
		lines[fillet] = edge_fillet(lines[fillet],1.5)

	#build the holes
	holes = []

	#corner holes
	for sx,offset in zip([1,-1],[0,corner_offset]):
		for sy in [1,-1]:
			hole = []
			for i in range(1,len(vertices_hole)):
				v1 = Vector(vertices_hole[i-1]).scale(sx,sy,1) + Vector((offset,0,0))
				v2 = Vector(vertices_hole[i]).scale(sx,sy,1) + Vector((offset,0,0))
				hole.append(Part.makeLine(v1,v2))
			holes.append(Part.Wire(hole))
			if sx*sy > 0:
				holes[-1].reverse()

	#circular holes
	for offset in circle_offsets:
		holes.append(Part.Wire(Part.makeCircle(2.1,Vector(offset,0,0))))
		holes[-1].reverse()

	space_symmetry = [
		(+1,len(vertices_inner),  +1, 0,-1,0,+1,1),
		(len(vertices_inner)-2,-1,-1,-w,+1,0,+1,1),
		(+1,len(vertices_inner),  +1,-w,+1,0,-1,1),
		(len(vertices_inner)-2,-1,-1, 0,-1,0,-1,1),
	]

	#big space
	for offset in space_offsets:
		hole = []
		vcur = Vector(vertices_inner[0]).scale(-1,1,1) + Vector((offset,0,0))
		for part in space_symmetry:
			for i in range(part[0],part[1],part[2]):
				vlast = vcur
				vcur = Vector(vertices_inner[i])
				vcur[0],vcur[1] = part[4]*vcur[part[5]]+part[3],part[6]*vcur[part[7]]
				vcur += Vector((offset,0,0))
				hole.append(makeLine(vlast,vcur))
		holes.append(Part.Wire(hole))
		holes[-1].reverse()

	#put everything together
	return Part.Face([Part.Wire(lines)] + holes)

def vslot20x20(params,document):
	name = params["name"]
	l = params["l"]

	#due to symmetry this can be nicely decomposed
	#start iteration,end iteration, step, x offset, sign x, cmp x, sign y, cmp y
	symmetry = [
		(+1,len(vertices_corner),  +1,0,+1,0,+1,1),
		(len(vertices_corner)-2,-1,-1,0,+1,1,+1,0),
		(+1,len(vertices_corner),  +1,0,-1,1,+1,0),
		(len(vertices_corner)-2,-1,-1,0,-1,0,+1,1),
		(+1,len(vertices_corner),  +1,0,-1,0,-1,1),
		(len(vertices_corner)-2,-1,-1,0,-1,1,-1,0),
		(+1,len(vertices_corner),  +1,0,+1,1,-1,0),
		(len(vertices_corner)-2,-1,-1,0,+1,0,-1,1),
	]

	#add fillets in reverse order, as this inserts additional edges
	fillets = [slice(41,43),slice(29,31),slice(17,19),slice(5,7)]
	corner_offset = 0
	circle_offsets = [0]
	space_offsets = []

	face = vslot(symmetry,fillets,corner_offset,circle_offsets,space_offsets)

	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name

	part.Shape = face.extrude(Vector(0,0,l)).removeSplitter()

	#color
	if params['finish'] == "Black":
		part.ViewObject.DiffuseColor = (0.1,0.1,0.1)

def vslot20x40(params,document):
	name = params["name"]
	l = params["l"]

	#due to symmetry this can be nicely decomposed
	#start iteration,end iteration, step, x offset,sign x, cmp x, sign y, cmp y
	symmetry = [
		(+1,len(vertices_corner),  +1, 0,+1,0,+1,1),
		(len(vertices_corner)-2,-1,-1, 0,+1,1,+1,0),
		(+1,len(vertices_corner),  +1, 0,-1,1,+1,0),
		(len(vertices_corner)-2,-1,-1,-w,+1,1,+1,0),
		(+1,len(vertices_corner),  +1,-w,-1,1,+1,0),
		(len(vertices_corner)-2,-1,-1,-w,-1,0,+1,1),
		(+1,len(vertices_corner),  +1,-w,-1,0,-1,1),
		(len(vertices_corner)-2,-1,-1,-w,-1,1,-1,0),
		(+1,len(vertices_corner),  +1,-w,+1,1,-1,0),
		(len(vertices_corner)-2,-1,-1, 0,-1,1,-1,0),
		(+1,len(vertices_corner),  +1, 0,+1,1,-1,0),
		(len(vertices_corner)-2,-1,-1, 0,+1,0,-1,1),
	]

	#add fillets in reverse order, as this inserts additional edges
	fillets = [slice(65,67),slice(41,43),slice(29,31),slice(5,7)]
	corner_offset = -1*w
	circle_offsets = [0,-w]
	space_offsets = [0]

	face = vslot(symmetry,fillets,corner_offset,circle_offsets,space_offsets)

	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name

	part.Shape = face.extrude(Vector(0,0,l)).removeSplitter()

	#color
	if params['finish'] == "Black":
		part.ViewObject.DiffuseColor = (0.1,0.1,0.1)

def vslot20x60(params,document):
	name = params["name"]
	l = params["l"]

	#due to symmetry this can be nicely decomposed
	#start iteration,end iteration, step, x offset,sign x, cmp x, sign y, cmp y
	symmetry = [
		(+1,len(vertices_corner),  +1, 0,+1,0,+1,1),
		(len(vertices_corner)-2,-1,-1, 0,+1,1,+1,0),
		(+1,len(vertices_corner),  +1, 0,-1,1,+1,0),
		(len(vertices_corner)-2,-1,-1,-w,+1,1,+1,0),
		(+1,len(vertices_corner),  +1,-w,-1,1,+1,0),
		(len(vertices_corner)-2,-1,-1,-2*w,+1,1,+1,0),
		(+1,len(vertices_corner),  +1,-2*w,-1,1,+1,0),
		(len(vertices_corner)-2,-1,-1,-2*w,-1,0,+1,1),
		(+1,len(vertices_corner),  +1,-2*w,-1,0,-1,1),
		(len(vertices_corner)-2,-1,-1,-2*w,-1,1,-1,0),
		(+1,len(vertices_corner),  +1,-2*w,+1,1,-1,0),
		(len(vertices_corner)-2,-1,-1,-w,-1,1,-1,0),
		(+1,len(vertices_corner),  +1,-w,+1,1,-1,0),
		(len(vertices_corner)-2,-1,-1, 0,-1,1,-1,0),
		(+1,len(vertices_corner),  +1, 0,+1,1,-1,0),
		(len(vertices_corner)-2,-1,-1, 0,+1,0,-1,1),
	]

	#add fillets in reverse order, as this inserts additional edges
	fillets = [slice(89,91),slice(53,55),slice(41,43),slice(5,7)]
	corner_offset = -2*w
	circle_offsets = [0,-w,-2*w]
	space_offsets = [0,-w]

	face = vslot(symmetry,fillets,corner_offset,circle_offsets,space_offsets)

	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name

	part.Shape = face.extrude(Vector(0,0,l)).removeSplitter()

	#color
	if params['finish'] == "Black":
		part.ViewObject.DiffuseColor = (0.1,0.1,0.1)

def vslot20x80(params,document):
	name = params["name"]
	l = params["l"]

	#due to symmetry this can be nicely decomposed
	#start iteration,end iteration, step, x offset,sign x, cmp x, sign y, cmp y
	symmetry = [
		(+1,len(vertices_corner),  +1, 0,+1,0,+1,1),
		(len(vertices_corner)-2,-1,-1, 0,+1,1,+1,0),
		(+1,len(vertices_corner),  +1, 0,-1,1,+1,0),
		(len(vertices_corner)-2,-1,-1,-w,+1,1,+1,0),
		(+1,len(vertices_corner),  +1,-w,-1,1,+1,0),
		(len(vertices_corner)-2,-1,-1,-2*w,+1,1,+1,0),
		(+1,len(vertices_corner),  +1,-2*w,-1,1,+1,0),
		(len(vertices_corner)-2,-1,-1,-3*w,+1,1,+1,0),
		(+1,len(vertices_corner),  +1,-3*w,-1,1,+1,0),
		(len(vertices_corner)-2,-1,-1,-3*w,-1,0,+1,1),
		(+1,len(vertices_corner),  +1,-3*w,-1,0,-1,1),
		(len(vertices_corner)-2,-1,-1,-3*w,-1,1,-1,0),
		(+1,len(vertices_corner),  +1,-3*w,+1,1,-1,0),
		(len(vertices_corner)-2,-1,-1,-2*w,-1,1,-1,0),
		(+1,len(vertices_corner),  +1,-2*w,+1,1,-1,0),
		(len(vertices_corner)-2,-1,-1,-w,-1,1,-1,0),
		(+1,len(vertices_corner),  +1,-w,+1,1,-1,0),
		(len(vertices_corner)-2,-1,-1, 0,-1,1,-1,0),
		(+1,len(vertices_corner),  +1, 0,+1,1,-1,0),
		(len(vertices_corner)-2,-1,-1, 0,+1,0,-1,1),
	]

	#add fillets in reverse order, as this inserts additional edges
	fillets = [slice(113,115),slice(65,67),slice(53,55),slice(5,7)]
	corner_offset = -3*w
	circle_offsets = [0,-w,-2*w,-3*w]
	space_offsets = [0,-w,-2*w]

	face = vslot(symmetry,fillets,corner_offset,circle_offsets,space_offsets)

	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name

	part.Shape = face.extrude(Vector(0,0,l)).removeSplitter()

	#color
	if params['finish'] == "Black":
		part.ViewObject.DiffuseColor = (0.1,0.1,0.1)
