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

def dualvwheel(params,document):
	#no params
	name = params["name"]
	#still name some quantities
	r_1 = 0.5*13.89
	r_2 = 0.5*15.974
	r_3 = 9.77
	r_4 = 0.5*18.75
	r_5 = 0.5*24.39

	#profile for revolution is symmetric, therefore only points from right half
	vertices = [
		(0,r_1,0),
		(0.5,r_1,0),
		(0.5,r_2,0),
		(0.5*10.23-0.3,r_2,0),
		(0.5*10.23,r_2+0.3,0),
		(0.5*10.23,r_3,0),
		(0.5*(10.23-4.84),r_5,0),
		(0.5*(10.23)-4.84,r_3,0),
		(0.5*(10.23)-4.84,r_4,0),
		(0,r_4,0)
	]

	lines = []

	vlast = None
	vcur = Vector(vertices[0])

	#right half
	for i in range(1,len(vertices)):
		vlast = vcur
		vcur = Vector(vertices[i])
		lines.append(makeLine(vcur,vlast))

	#left half
	for i in range(len(vertices)-2,-1,-1):
		vlast = vcur
		vcur = Vector(vertices[i])
		vcur[0] *= -1
		lines.append(makeLine(vcur,vlast))


	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name

	part.Shape  = Part.Face(Part.Wire(lines)).revolve(Vector(0,0,0),Vector(1,0,0),360).removeSplitter()


def solidvwheel(params,document):
	#no params
	name = params["name"]
	#still name some quantities
	r_1 = 0.5*13.89
	r_2 = 0.5*15.974
	r_3 = 9.77
	r_4 = 0.5*23.89

	#profile for revolution is symmetric, therefore only points from right half
	vertices = [
		(0,r_1,0),
		(0.5,r_1,0),
		(0.5,r_2,0),
		(0.5*10.23-0.3,r_2,0),
		(0.5*10.23,r_2+0.3,0),
		(0.5*10.23,r_3,0),
		(0.5*5.89,r_4,0),
		(0,r_4,0),
	]

	lines = []

	vlast = None
	vcur = Vector(vertices[0])

	#right half
	for i in range(1,len(vertices)):
		vlast = vcur
		vcur = Vector(vertices[i])
		lines.append(makeLine(vcur,vlast))

	#left half
	for i in range(len(vertices)-2,-1,-1):
		vlast = vcur
		vcur = Vector(vertices[i])
		vcur[0] *= -1
		lines.append(makeLine(vcur,vlast))


	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name

	part.Shape  = Part.Face(Part.Wire(lines)).revolve(Vector(0,0,0),Vector(1,0,0),360).removeSplitter()

def minivwheel(params,document):
	#no params
	name = params["name"]
	#still name some quantities
	r_1 = 0.5*8.64
	r_2 = 0.5*9.974
	r_3 = 0.5*12.21
	r_4 = 0.5*15.23

	#profile for revolution is symmetric, therefore only points from right half
	vertices = [
		(0,r_1,0),
		(0.5,r_1,0),
		(0.5,r_2,0),
		(0.5*8.8-0.3,r_2,0),
		(0.5*8.8,r_2+0.3,0),
		(0.5*8.8,r_3,0),
		(0.5*5.78,r_4,0),
		(0,r_4,0),
	]

	lines = []

	vlast = None
	vcur = Vector(vertices[0])

	#right half
	for i in range(1,len(vertices)):
		vlast = vcur
		vcur = Vector(vertices[i])
		lines.append(makeLine(vcur,vlast))

	#left half
	for i in range(len(vertices)-2,-1,-1):
		vlast = vcur
		vcur = Vector(vertices[i])
		vcur[0] *= -1
		lines.append(makeLine(vcur,vlast))


	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name

	part.Shape  = Part.Face(Part.Wire(lines)).revolve(Vector(0,0,0),Vector(1,0,0),360).removeSplitter()




