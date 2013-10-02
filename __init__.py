from os.path import join, exists, dirname
from os import listdir
from bolttools import blt_parser
from bolttools import freecad
from PyQt4 import QtCore

from freecad.gui.freecad_bolts import BoltsWidget, getMainWindow

#import repo
rootpath =  dirname(__file__)
repo = blt_parser.BOLTSRepository(rootpath)

widget = BoltsWidget(repo)

mw = getMainWindow()
mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, widget)


import FreeCAD
def make_drawing(scale,obj):
	doc = FreeCAD.ActiveDocument
	page = doc.addObject("Drawing::FeaturePage","Page")
	page.Template = join(rootpath,"drawings","template.svg")


	#front, side right, side left, rear, top, bottom, iso
	directions = [(0.,0.,1.),(1.,0.,0.),(-1.,0.,0.),(0.,0.,-1.),(0.,-1.,0.),(0.,1.,0.),(1.,1.,1.)]
	#x center positions
	positions = [(110.,100.),(40.,100.),(180.,100.),(250.,100.),(110.,35.),(110.,165.),(215.,35.)]
	rotations = [0,0,0,0,270,270,0]
	for i in range(7):
		view = doc.addObject("Drawing::FeatureViewPart","View%d" % i)
		view.Source = obj
		view.Direction = directions[i]
		view.X = positions[i][0]
		view.Y = positions[i][1]
		view.Rotation = rotations[i]
		view.Scale = scale
		page.addObject(view)

