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

def pipe(params,document):
	id = params['id']
	od = params['od']
	l = params['l']
	name = params['name']

	if id > od:
		raise ValueError("Inner diameter must be smaller than outer diameter")

	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name

	outer = Part.makeCylinder(0.5*od,l)
	inner = Part.makeCylinder(0.5*id,l)
	part.Shape = outer.cut(inner).removeSplitter()

def pipe_wall(params,document):
	od = params['od']
	wall = params['wall']
	l = params['l']
	name = params['name']

	id = od - 2*wall

	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name

	outer = Part.makeCylinder(0.5*od,l)
	inner = Part.makeCylinder(0.5*id,l)
	part.Shape = outer.cut(inner).removeSplitter()
