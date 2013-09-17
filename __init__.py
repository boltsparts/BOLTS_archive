from os.path import join, exists, dirname
from os import listdir
from bolttools import blt_parser
from bolttools import freecad
from PyQt4 import QtCore

from freecad.gui.freecad_bolts import BoltsWidget, getMainWindow

rootpath =  dirname(__file__)

#import repo
repo = blt_parser.BOLTSRepository(rootpath)

#collect bases
bases = {}
from BOLTS.freecad.hex import hex
bases.update(hex.bases)

mw = getMainWindow()

widget = BoltsWidget(repo,bases)

mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, widget)
