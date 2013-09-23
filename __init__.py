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
