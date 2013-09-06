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

def washer2(params,document):
	key = params['key']
	d1 = params['d1']
	d2 = params['d2']
	s = params['s']
	name = params['name']

	part = document.addObject("Part::Feature",name)
	outer = Part.makeCylinder(d2,s)
	inner = Part.makeCylinder(d1,s)
	shape = outer.cut(inner)
	#guessed size for the chamfer
	part.Shape = shape.makeChamfer(0.1*d1,shape.Edges[0:1])

bases = {'washer1':washer1, 'washer2':washer2}
