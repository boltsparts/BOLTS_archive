#BOLTS - Open Library of Technical Specifications
#Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import Part

def washer1(params,document):
	key = params['key']
	d1 = params['d1']
	d2 = params['d2']
	s = params['s']
	name = params['name']

	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name

	outer = Part.makeCylinder(0.5*d2,s)
	inner = Part.makeCylinder(0.5*d1,s)
	part.Shape = outer.cut(inner).removeSplitter()

def washer2(params,document):
	key = params['key']
	d1 = params['d1']
	d2 = params['d2']
	s = params['s']
	name = params['name']

	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name

	outer = Part.makeCylinder(0.5*d2,s)
	outer = outer.makeChamfer(0.3*s,outer.Edges[0:1])
	inner = Part.makeCylinder(0.5*d1,s)
	shape = outer.cut(inner)
	#guessed size for the chamfer
	part.Shape = shape.removeSplitter()
