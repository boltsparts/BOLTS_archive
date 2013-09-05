#bases
import Part

def washer1(params,document):
	key = params['key']
	d1 = params['d1']
	d2 = params['d2']
	s = params['s']
	name = params['name']

	part = document.addObject("Part::Feature",name)
	outer = Part.makeCylinder(d2,s)
	inner = Part.makeCylinder(d1,s)
	part.Shape = outer.cut(inner)

bases = {'washer1':washer1}
