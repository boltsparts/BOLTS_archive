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

def roundBattery(params,document):
	diam = params['d']
	h = params['h']
	name = params['name']

	part = document.addObject("Part::Feature","BOLTS_part")
	nub = Part.makeCylinder(0.15*diam,h)
	cell = Part.makeCylinder(0.5*diam,0.97*h)
	part.Shape = nub.fuse(cell).removeSplitter()
	part.Label = name

