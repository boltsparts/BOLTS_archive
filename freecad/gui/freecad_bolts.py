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
from os import listdir
from os.path import dirname, join
from BOLTS.bolttools import blt_parser
bolts_path = dirname(__file__)
from BOLTS.bolttools.blt_parser import BOLTSClass, BOLTSCollection, BOLTSRepository

#get ui from designer file
Ui_BoltsWidget,QBoltsWidget = uic.loadUiType(join(bolts_path,'bolts_widget.ui'))
Ui_ValueWidget,QValueWidget = uic.loadUiType(join(bolts_path,'value_widget.ui'))
Ui_BoolWidget,QBoolWidget = uic.loadUiType(join(bolts_path,'value_widget.ui'))
Ui_TableIndexWidget,QTableIndexWidget = uic.loadUiType(join(bolts_path,'tableindex_widget.ui'))
Ui_PropertyWidget,QPropertyWidget = uic.loadUiType(join(bolts_path,'property_widget.ui'))

#custom widgets

class PropertyWidget(QPropertyWidget):
	def __init__(self,parent,prop,value):
		QPropertyWidget.__init__(self,parent)
		self.ui = Ui_PropertyWidget()
		self.ui.setupUi(self)
		self.ui.prop.setTextFormat(QtCore.Qt.RichText)
		self.ui.prop.setText("<b>%s:</b>" % prop)
		self.ui.value.setText(value)

class LengthWidget(QValueWidget):
	def __init__(self,parent,label,default):
		QValueWidget.__init__(self,parent)
		self.ui = Ui_ValueWidget()
		self.ui.setupUi(self)
		self.ui.label.setText(label)
		self.ui.valueEdit.setText(default)

		self.validator = QtGui.QDoubleValidator(0,sys.float_info.max,4,self)
		self.ui.valueEdit.setValidator(self.validator)

	def getValue(self):
		return float(self.ui.valueEdit.text())

class NumberWidget(QValueWidget):
	def __init__(self,parent,label,default):
		QValueWidget.__init__(self,parent)
		self.ui = Ui_ValueWidget()
		self.ui.setupUi(self)
		self.ui.label.setText(label)
		self.ui.valueEdit.setText(default)

		self.validator = QtGui.QDoubleValidator(self)
		self.ui.valueEdit.setValidator(self.validator)

	def getValue(self):
		return float(self.ui.valueEdit.text())

class StringWidget(QValueWidget):
	def __init__(self,parent,label,default):
		QValueWidget.__init__(self,parent)
		self.ui = Ui_ValueWidget()
		self.ui.setupUi(self)
		self.ui.label.setText(label)
		self.ui.valueEdit.setText(default)

	def getValue(self):
		return self.ui.valueEdit.text()

class BoolWidget(QBoolWidget):
	def __init__(self,parent,label,default):
		QBoolWidget.__init__(self,parent)
		self.ui = Ui_BoolWidget()
		self.ui.setupUi(self)
		self.ui.label.setText(label)
		self.ui.checkBox.setChecked(default)

	def getValue(self):
		self.ui.checkBox.isChecked()

class TableIndexWidget(QTableIndexWidget):
	def __init__(self,parent,label,keys,default):
		QTableIndexWidget.__init__(self,parent)
		self.ui = Ui_TableIndexWidget()
		self.ui.setupUi(self)
		self.ui.label.setText(label)

		for key,i in zip(keys,range(len(keys))):
			self.ui.comboBox.addItem(key)
			if key == default:
				self.ui.comboBox.setCurrentIndex(i)

	def getValue(self):
		return str(self.ui.comboBox.currentText())

class BoltsWidget(QBoltsWidget):
	def __init__(self,repo):
		QBoltsWidget.__init__(self)
		self.ui = Ui_BoltsWidget()
		self.ui.setupUi(self)

		self.repo = repo

		self.param_widgets = {}
		self.props_widgets = {}

		self.coll_root = QtGui.QTreeWidgetItem(self.ui.partsTree,['Collections','Ordered by collections'])
		self.coll_root.setData(0,32,None)

		for coll in self.repo.collections:
			coll_item = QtGui.QTreeWidgetItem(self.coll_root,[coll.name, coll.description])
			coll_item.setData(0,32,coll)
			for cl in coll.classes:
				if not cl.id in self.repo.freecad.getbase:
					continue
				cl_item = QtGui.QTreeWidgetItem(coll_item,[cl.name, cl.description])
				cl_item.setData(0,32,cl)

		self.remove_empty_items(self.coll_root)

	def remove_empty_items(self,root_item):
		children = [root_item.child(i) for i in range(root_item.childCount())]
		for child in children:
			self.remove_empty_items(child)
			data = child.data(0,32).toPyObject()
			if not isinstance(data,BOLTSClass) and child.childCount() == 0:
				root_item.removeChild(child)

	def setup_param_widgets(self,cl):
		#construct widgets
		for p in cl.parameters.free:
			p_type = cl.parameters.types[p]
			default = str(cl.parameters.defaults[p])
			print p,p_type,default
			if p_type == "Length (mm)":
				self.param_widgets[p] = LengthWidget(self.ui.params,p + " (mm)",default)
			elif p_type == "Length (in)":
				self.param_widgets[p] = LengthWidget(self.ui.params,p + " (in)",default)
			elif p_type == "Number":
				self.param_widgets[p] = NumberWidget(self.ui.params,p,default)
			elif p_type == "Bool":
				self.param_widgets[p] = BoolWidget(self.ui.params,p,default)
			elif p_type == "Table Index":
				for table in cl.parameters.tables:
					if table.index == p:
						#try to detect metric threads
						keys = sorted(table.data.keys())
						if "M" in [str(v)[0] for v in table.data.keys()]:
							try:
								keys = sorted(table.data.keys(),key=lambda x: float(x[1:]))
							except:
								keys = sorted(table.data.keys())
						self.param_widgets[p] = TableIndexWidget(self.ui.params,p,keys,default)
						#if more than one table has the same index, they have the same keys, so stop
						break
		#add them to layout
			self.ui.param_layout.addWidget(self.param_widgets[p])

	def setup_props_collection(self,coll):
		#construct widgets
		self.props_widgets.append(PropertyWidget(self.ui.props,"Name",coll.name))
		self.props_widgets.append(PropertyWidget(self.ui.props,"Description",coll.description))
		self.props_widgets.append(PropertyWidget(self.ui.props,"Authors",", ".join(coll.author_names)))
		self.props_widgets.append(PropertyWidget(self.ui.props,"License",coll.license_name))

		#add them to layout
		for widget in self.props_widgets:
			self.ui.props_layout.addWidget(widget)

	def setup_props_class(self,cl):
		#construct widgets
		self.props_widgets.append(PropertyWidget(self.ui.props,"Name",cl.name))
		if cl.description:
			self.props_widgets.append(PropertyWidget(self.ui.props,"Description",cl.description))
		if not cl.standard is None:
			if cl.status == "withdrawn":
				self.props_widgets.append(PropertyWidget(self.ui.props,"Status","<font color='red'>%s</font>" % cl.status))
			else:
				self.props_widgets.append(PropertyWidget(self.ui.props,"Status","<font color='green'>%s</font>" % cl.status))
			if not cl.replaces is None:
				self.props_widgets.append(PropertyWidget(self.ui.props,"Replaces",cl.replaces))
			if not cl.replacedby is None:
				self.props_widgets.append(PropertyWidget(self.ui.props,"Replacedby",cl.replacedby))
		if cl.url:
			self.props_widgets.append(PropertyWidget(self.ui.props,"URL",cl.url))

		#add them to layout
		for widget in self.props_widgets:
			self.ui.props_layout.addWidget(widget)

	def on_addButton_clicked(self,checked):
		if FreeCAD.activeDocument() is None:
			FreeCAD.newDocument()

		items = self.ui.partsTree.selectedItems()

		if len(items) < 1:
			return

		data = items[0].data(0,32).toPyObject()

		if not isinstance(data,BOLTSClass):
			return

		params = {}
		#read parameters from widgets
		for key in self.param_widgets:
			params[key] = self.param_widgets[key].getValue()
		params = data.parameters.collect(params)
		params['standard'] = data.name

		params['name'] = data.naming.template % \
			tuple(params[k] for k in data.naming.substitute)

		#add part
		self.repo.freecad.getbase[data.id].add_part(params,FreeCAD.ActiveDocument)

	def on_partsTree_itemSelectionChanged(self):
		items = self.ui.partsTree.selectedItems()
		if len(items) < 1:
			return
		item = items[0]
		data = item.data(0,32).toPyObject()

		#clear props widget
		for widget in self.props_widgets:
			self.ui.props_layout.removeWidget(widget)
			widget.setParent(None)
		self.props_widgets = []
		#clear
		for key in self.param_widgets:
			self.ui.param_layout.removeWidget(self.param_widgets[key])
			self.param_widgets[key].setParent(None)
		self.param_widgets = {}

		if isinstance(data,BOLTSClass):
			self.setup_props_class(data)
			self.setup_param_widgets(data)
		elif isinstance(data,BOLTSCollection):
			self.setup_props_collection(data)

#get reference to Freecad main window
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

def addWidget(widget):
	mw = getMainWindow()
	mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, widget)

