# Copyright 2012-2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtGui, QtCore, uic
import FreeCAD
import sys
sys.path.append('..')
from os import listdir
from  blt_parser import load_collection

#get ui from designer file
Ui_BoltsWidget,QBoltsWidget = uic.loadUiType('bolts_widget.ui')
Ui_DimWidget,QDimWidget = uic.loadUiType('dim_widget.ui')
Ui_KeyWidget,QKeyWidget = uic.loadUiType('key_widget.ui')

#classes to encapsulate the data from the blt collections
class BOLTSStandard:
	def __init__(self,standard,part):
		self.standard = standard
		self.description = part['description']
		self.base = part['base']
		self.target_args = part['target-args']
		self.name_template = part['name']['template']
		self.name_parameters = part['name']['parameters']
		self.columns = part['table']['columns']
		self.data = part['table']['data']
	def setup_param_widget(self,bolts_widget):

		for arg in self.target_args:
			if arg == 'key':
				keys = [row[0] for row in sorted(self.data.iteritems(),key=lambda x: float(x[0][1:]))]
				bolts_widget.add_param_widget(arg,lambda p: KeyWidget(p,keys))
			else:
				bolts_widget.add_param_widget(arg,lambda p: DimWidget(p,arg))

	def get_tree_item(self,parent_item):
		item = QtGui.QTreeWidgetItem(parent_item,[self.standard,self.description])
		item.setData(0,32,self)
		return item

class StandardCollection:
	def __init__(self,org, description):
		self.org = org
		self.description = description
	def get_tree_item(self,parent_item):
		item = QtGui.QTreeWidgetItem(parent_item,[self.org,self.description])
		item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
		item.setExpanded(False)
		item.setData(0,32,self)
		return item

class BOLTSCollection:
	def __init__(self,blt):
		coll = blt['collection']
		self.name = coll['name']
		self.description = coll['description']
		self.author = coll['author']
		self.license = coll['license']
		self.blt_version = coll['blt-version']
	def get_tree_item(self,parent_item):
		item = QtGui.QTreeWidgetItem(parent_item,[self.name,self.description])
		item.setData(0,32,self)
		return item

#customm widgets

class DimWidget(QDimWidget):
	def __init__(self,parent,label):
		QDimWidget.__init__(self,parent)
		self.ui = Ui_DimWidget()
		self.ui.setupUi(self)
		self.ui.label.setText(label)

		self.validator = QtGui.QDoubleValidator(self)
		self.ui.valueEdit.setValidator(self.validator)

	def getValue(self):
		return float(self.ui.valueEdit.text())

class KeyWidget(QKeyWidget):
	def __init__(self,parent,keys):
		QKeyWidget.__init__(self,parent)
		self.ui = Ui_KeyWidget()
		self.ui.setupUi(self)
		for key in keys:
			self.ui.comboBox.addItem(key)
	def getValue(self):
		return str(self.ui.comboBox.currentText())


class BoltsWidget(QBoltsWidget):
	def __init__(self,bases):
		QBoltsWidget.__init__(self)
		self.ui = Ui_BoltsWidget()
		self.ui.setupUi(self)

		self.bases = bases

		self.param_widgets = {}

		self.std_root = QtGui.QTreeWidgetItem(self.ui.partsTree,['Standards','Ordered by organisation'])
		self.std_root.setData(0,32,None)
		self.std_coll_items = {}
		for org in ['DIN','DINISO','EN','DINENISO','DINEN']:
			std_coll = StandardCollection(org,'%s standards' % org)
			self.std_coll_items[org] = std_coll.get_tree_item(self.std_root)

		self.coll_root = QtGui.QTreeWidgetItem(self.ui.partsTree,['Collections','Ordered by collections'])
		self.coll_root.setData(0,32,None)

	def remove_empty_items(self,root_item):
		children = [root_item.child(i) for i in range(root_item.childCount())]
		for child in children:
			self.remove_empty_items(child)
			data = child.data(0,32).toPyObject()
			if not isinstance(data,BOLTSStandard) and child.childCount() == 0:
				root_item.removeChild(child)


	def clear_param_widgets(self):
		for key in self.param_widgets:
			self.ui.param_layout.removeWidget(self.param_widgets[key])
			self.param_widgets[key].setParent(None)
		self.param_widgets = {}

	def add_param_widget(self,key,constructor_callback):
		self.param_widgets[key] = constructor_callback(self.ui.params)
		self.ui.param_layout.addWidget(self.param_widgets[key])

	def on_addButton_clicked(self,checked):
		if FreeCAD.activeDocument is None:
			return

		items = self.ui.partsTree.selectedItems()

		if len(items) < 1:
			return

		data = items[0].data(0,32).toPyObject()

		if not isinstance(data,BOLTSStandard):
			return

		if not data.base in self.bases:
			return

		params = {}
		#read parameters from widgets
		for key in self.param_widgets:
			params[key] = self.param_widgets[key].getValue()
		#additional parameters from table
		if 'key' in params:
			params.update(dict(zip(data.columns,data.data[params['key']])))
		params['standard'] = data.standard

		params['name'] = data.name_template % tuple(params[k] for k in data.name_parameters)

		#add part
		self.bases[data.base](params,FreeCAD.ActiveDocument)

	def on_partsTree_itemSelectionChanged(self):
		items = self.ui.partsTree.selectedItems()
		if len(items) < 1:
			return
		item = items[0]
		data = item.data(0,32).toPyObject()

		if data is None:
			self.ui.name.setText('')
			self.ui.description.setText('')
		elif isinstance(data,BOLTSStandard):
			self.ui.name.setText(data.standard)
			self.ui.description.setText(data.description)
			self.clear_param_widgets()
			data.setup_param_widget(self)
		elif isinstance(data,StandardCollection):
			self.ui.name.setText(data.org)
			self.ui.description.setText(data.description)
		elif isinstance(data,BOLTSCollection):
			self.ui.name.setText(data.name)
			self.ui.description.setText(data.description)

	def addCollection(self,blt):
		coll = BOLTSCollection(blt)
		coll_item = coll.get_tree_item(self.coll_root)
		for part in blt['parts']:
			if not part['base'] in self.bases:
				continue
			for standard_name in part['standard']:
				standard = BOLTSStandard(standard_name,part)
				standard.get_tree_item(coll_item)

				#add to respective standard
				if standard_name.startswith("DINENISO"):
					standard.get_tree_item(self.std_coll_items["DINENISO"])
				elif standard_name.startswith("DINEN"):
					standard.get_tree_item(self.std_coll_items["DINEN"])
				elif standard_name.startswith("DINISO"):
					standard.get_tree_item(self.std_coll_items["DINISO"])
				elif standard_name.startswith("DIN"):
					standard.get_tree_item(self.std_coll_items["DIN"])
				elif standard_name.startswith("EN"):
					standard.get_tree_item(self.std_coll_items["EN"])


#get references to Freecad main window
#from http://sourceforge.net/apps/mediawiki/free-cad/index.php?title=Code_snippets
def getMainWindow():
	"returns the main window"
	# using QtGui.qApp.activeWindow() isn't very reliable because if another
	# widget than the mainwindow is active (e.g. a dialog) the wrong widget is
	# returned
	toplevel = QtGui.qApp.topLevelWidgets()
	for i in toplevel:
		if i.metaObject().className() == "Gui::MainWindow":
			return i
	raise Exception("No main window found")

app = QtGui.qApp
mw = getMainWindow()

#load bases
import washer
import hex

bases = {}
bases.update(washer.bases)
bases.update(hex.bases)

widget = BoltsWidget(bases)

#load parts
files = listdir('blt')
for file in files:
	if file.startswith('.'):
		continue
	blt = load_collection(file)
	widget.addCollection(blt)

widget.remove_empty_items(widget.std_root)
widget.remove_empty_items(widget.coll_root)

mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, widget)
