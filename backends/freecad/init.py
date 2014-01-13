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

import FreeCAD, FreeCADGui, Part
from os.path import join, exists, dirname
from os import listdir
import bolttools.blt
import bolttools.freecad
try:
	from PySide import QtCore
except ImportError:
	from PyQt4 import QtCore

from gui.freecad_bolts import BoltsWidget


#import repo
rootpath =  dirname(__file__)
repo = bolttools.blt.BOLTSRepository(rootpath)
freecad = bolttools.freecad.FreeCADData(rootpath)

widget = None

if widget is None:
	widget = BoltsWidget(repo,freecad)

	mw = FreeCADGui.getMainWindow()
	mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, widget)
else:
	widget.show()

def make_drawing(scale,obj):
	doc = FreeCAD.ActiveDocument
	page = doc.addObject("Drawing::FeaturePage","Page")
	page.Template = join(rootpath,"assets","template.svg")


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

def list_names(doc):
	print "Label   Name"
	print "------------"
	for part in doc.findObjects():
		if isinstance(part,Part.Feature):
			print "%s    %s" % (part.Label, part.Name)


