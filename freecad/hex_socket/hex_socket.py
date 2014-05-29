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
from Part import makeBox, makeCone, makeCylinder
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

def hex_socket1(params,document):
	d1 = params['d1']
	d2 = params['d2']
	b1 = params['b1']
	b2 = params['b2']
	b3 = params['b3']
	k_max = params['k_max']
	s = params['s']
	t = params['t']
	L = params['L']
	h_max = params['h_max']
	l = params['l']

	if l <= L:
		b = l - k_max - h_max
	elif l < 125:
		b = b1
	elif l < 200:
		b = b2
	else:
		b = b3

	if b < 0:
		raise ValueError("Invalid threaded length: %s" % b)

	h = l - k_max - b

	#head
	head = makeCone(0.5*d2,0.5*d1,k_max)
	#socket
	a = s/math.tan(math.pi/3.)
	box1 = makeBox(a,s,t)
	box1.translate(Vector(-0.5*a,-0.5*s,0))
	box1.rotate(Vector(0,0,0),Vector(0,0,1),30)
	box2 = makeBox(a,s,t)
	box2.translate(Vector(-0.5*a,-0.5*s,0))
	box2.rotate(Vector(0,0,0),Vector(0,0,1),150)
	box3 = makeBox(a,s,t)
	box3.translate(Vector(-0.5*a,-0.5*s,0))
	box3.rotate(Vector(0,0,0),Vector(0,0,1),270)
	socket = box1.fuse(box2).fuse(box3)

	shaft_unthreaded = makeCylinder(0.5*d1,h+k_max)
	shaft_threaded = makeCylinder(0.5*d1,b)
	shaft_threaded.translate(Vector(0,0,h+k_max))

	name = params['name']
	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name
	part.Shape = head.fuse(shaft_unthreaded).cut(socket).removeSplitter().fuse(shaft_threaded)

	#color thread
	color_face(part,1)

def hex_socket2(params,document):
	d1 = params['d1']
	d2 = params['d2']
	b = params['b']
	k = params['k']
	s = params['s']
	t = params['t_min']
	L = params['L']
	l = params['l']

	if l <= L:
		h = 0
	else:
		h = l - b

	if h < 0:
		raise ValueError("l is too short, resulting in negative h")

	#head
	head = makeCylinder(0.5*d2,k)
	#socket
	a = s/math.tan(math.pi/3.)
	box1 = makeBox(a,s,t)
	box1.translate(Vector(-0.5*a,-0.5*s,0))
	box1.rotate(Vector(0,0,0),Vector(0,0,1),30)
	box2 = makeBox(a,s,t)
	box2.translate(Vector(-0.5*a,-0.5*s,0))
	box2.rotate(Vector(0,0,0),Vector(0,0,1),150)
	box3 = makeBox(a,s,t)
	box3.translate(Vector(-0.5*a,-0.5*s,0))
	box3.rotate(Vector(0,0,0),Vector(0,0,1),270)
	socket = box1.fuse(box2).fuse(box3)

	shaft_unthreaded = makeCylinder(0.5*d1,h+k)
	shaft_threaded = makeCylinder(0.5*d1,b)
	shaft_threaded.translate(Vector(0,0,h+k))

	name = params['name']
	part = document.addObject("Part::Feature","BOLTS_part")
	part.Label = name
	part.Shape = head.fuse(shaft_unthreaded).cut(socket).removeSplitter().fuse(shaft_threaded)

	#color thread
	color_face(part,1)
