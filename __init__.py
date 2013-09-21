from os.path import join, exists, dirname
from os import listdir
from bolttools import blt_parser
from bolttools import freecad
from PyQt4 import QtCore
import importlib

from freecad.gui.freecad_bolts import BoltsWidget, getMainWindow

rootpath =  dirname(__file__)

#import repo
repo = blt_parser.BOLTSRepository(rootpath)

#collect freecad base functions
bases = {}
for coll in listdir(join(rootpath,"freecad")):
	if not exists(join(rootpath,"freecad",coll,"%s.base" % coll)):
		continue
	mod = importlib.import_module("BOLTS.freecad.%s.%s" % (coll,coll))
	bases.update(mod.bases)

print bases

mw = getMainWindow()

widget = BoltsWidget(repo,bases)

mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, widget)
