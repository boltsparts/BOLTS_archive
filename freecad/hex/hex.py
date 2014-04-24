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

from FreeCAD import Vector
from Part import makeBox
import Part
import math
import FreeCADGui

thread_color = (0.5,1.,5.,0.)

def runs_headless():
	return 'setupWithoutGUI' in FreeCADGui.__dict__

def color_face(part,n):
	if runs_headless():
		return
	color = part.ViewObject.DiffuseColor[0]
	n_faces = len(part.Shape.Faces)
	part.ViewObject.DiffuseColor = [color if i != n else thread_color for i in range(n_faces)]

def hex1(params,document):
	key = params['key']
	d1 = params['d1']
	k = params['k']
	s = params['s']
	h = params['h']
	if h is None:
		h = 0.
	l = params['l']
	name = params['name']

	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name

	#head
	a = s/math.tan(math.pi/3.)
	box1 = makeBox(a,s,k)
	box1.translate(Vector(-0.5*a,-0.5*s,0))
	box1.rotate(Vector(0,0,0),Vector(0,0,1),30)
	box2 = makeBox(a,s,k)
	box2.translate(Vector(-0.5*a,-0.5*s,0))
	box2.rotate(Vector(0,0,0),Vector(0,0,1),150)
	box3 = makeBox(a,s,k)
	box3.translate(Vector(-0.5*a,-0.5*s,0))
	box3.rotate(Vector(0,0,0),Vector(0,0,1),270)
	head = box1.fuse(box2).fuse(box3)

	shaft_unthreaded = Part.makeCylinder(0.5*d1,h+k)
	shaft_threaded = Part.makeCylinder(0.5*d1,l-h)
	shaft_threaded.translate(Vector(0,0,h+k))
	part.Shape = head.fuse(shaft_unthreaded).removeSplitter().fuse(shaft_threaded)

	#color thread
	color_face(part,9)

def hex2(params,document):
	key = params['key']
	d1 = params['d1']
	k = params['k']
	s = params['s']
	b1 = params['b1']
	b2 = params['b2']
	b3 = params['b3']
	l = params['l']
	b = b3;
	if l < 125:
		b = b1
	elif l < 200:
		b = b2
	name = params['name']

	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name

	#head
	a = s/math.tan(math.pi/3.)
	box1 = makeBox(a,s,k)
	box1.translate(Vector(-0.5*a,-0.5*s,0))
	box1.rotate(Vector(0,0,0),Vector(0,0,1),30)
	box2 = makeBox(a,s,k)
	box2.translate(Vector(-0.5*a,-0.5*s,0))
	box2.rotate(Vector(0,0,0),Vector(0,0,1),150)
	box3 = makeBox(a,s,k)
	box3.translate(Vector(-0.5*a,-0.5*s,0))
	box3.rotate(Vector(0,0,0),Vector(0,0,1),270)
	head = box1.fuse(box2).fuse(box3)

	shaft_unthreaded = Part.makeCylinder(0.5*d1,l-b+k)
	shaft_threaded = Part.makeCylinder(0.5*d1,b)
	shaft_threaded.translate(Vector(0,0,l-b+k))
	part.Shape = head.fuse(shaft_unthreaded).removeSplitter().fuse(shaft_threaded)

	#color thread
	color_face(part,9)

