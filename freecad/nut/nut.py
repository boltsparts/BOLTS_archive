from FreeCAD import Vector
from Part import makeBox
import Part
import math

def nut1(params,document):
	key = params['key']
	d1 = params['d1']
	s = params['s']
	m_max = params['m_max']
	name = params['name']

	r_fillet = 0.03*s

	part = document.addObject("Part::Feature",name)

	#head
	a = s/math.tan(math.pi/3.)
	box1 = makeBox(a,s,m_max)
	box1.translate(Vector(-0.5*a,-0.5*s,0))
	box1.rotate(Vector(0,0,0),Vector(0,0,1),30)
	box2 = makeBox(a,s,m_max)
	box2.translate(Vector(-0.5*a,-0.5*s,0))
	box2.rotate(Vector(0,0,0),Vector(0,0,1),150)
	box3 = makeBox(a,s,m_max)
	box3.translate(Vector(-0.5*a,-0.5*s,0))
	box3.rotate(Vector(0,0,0),Vector(0,0,1),270)
	head = box1.fuse(box2).fuse(box3)

	hole = Part.makeCylinder(0.5*d1,2*m_max)
	nut = head.cut(hole)
#	nut = nut.makeFillet(r_fillet,nut.Edges)
	part.Shape = nut.removeSplitter()

