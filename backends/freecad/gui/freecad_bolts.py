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

from os.path import dirname, join
bolts_path = dirname(__file__)
from BOLTS import USE_PYSIDE

import FreeCAD, FreeCADGui

if USE_PYSIDE:
	from PySide import QtCore, QtGui
	from FreeCADGui import PySideUic as uic

	try:
		Ui_BoltsWidget,QBoltsWidget = uic.loadUiType(join(bolts_path,'bolts_widget.ui'))
		Ui_ValueWidget,QValueWidget = uic.loadUiType(join(bolts_path,'value_widget.ui'))
		Ui_BoolWidget,QBoolWidget = uic.loadUiType(join(bolts_path,'bool_widget.ui'))
		Ui_TableIndexWidget,QTableIndexWidget = uic.loadUiType(join(bolts_path,'tableindex_widget.ui'))
		Ui_PropertyWidget,QPropertyWidget = uic.loadUiType(join(bolts_path,'property_widget.ui'))
	except ImportError:
		FreeCAD.Console.PrintError("uic import failed. Make sure that the pyside tools are installed")
		raise
	from PySide.QtCore import Slot
	def unpack(x):
		return x
else:
	from PyQt4 import QtGui, QtCore
	from bolts_widget import Ui_BoltsWidget
	from PyQt4.QtGui import QDockWidget as QBoltsWidget
	from value_widget import Ui_ValueWidget
	from PyQt4.QtGui import QWidget as QValueWidget
	from bool_widget import Ui_BoolWidget
	from PyQt4.QtGui import QWidget as QBoolWidget
	from tableindex_widget import Ui_TableIndexWidget
	from PyQt4.QtGui import QWidget as QTableIndexWidget
	from property_widget import Ui_PropertyWidget
	from PyQt4.QtGui import QWidget as QPropertyWidget
	from PyQt4.QtCore import pyqtSlot as Slot
	def unpack(x):
		return x.toPyObject()

import Part, Sketcher
import sys
from os import listdir
from BOLTS.bolttools import blt
from BOLTS.bolttools import freecad
from BOLTS.bolttools.blt import BOLTSClass, BOLTSCollection, BOLTSRepository
import importlib

def add_part(base,params,doc):
	if isinstance(base,freecad.BaseFunction):
		module = importlib.import_module("BOLTS.freecad.%s.%s" %
			(base.collection,base.module_name))
		module.__dict__[base.name](params,doc)
	elif isinstance(base,freecad.BaseFcstd):
		#copy part to doc
		src_doc = FreeCAD.openDocument(base.path)
		src_obj = src_doc.getObject(base.objectname)
		if src_obj is None:
			raise MalformedBaseError("No object %s found" % base.objectname)
		#maps source name to destination object
		srcdstmap = {}
		dst_obj = copy_part_recursive(src_obj,doc,srcdstmap)

		#set parameters
		for obj_name,proptoparam in base.proptoparam.iteritems():
			for prop,param in proptoparam.iteritems():
				setattr(srcdstmap[obj_name],prop,params[param])

		#finish presentation
		dst_obj.touch()
		doc.recompute()
		FreeCADGui.getDocument(doc.Name).getObject(dst_obj.Name).Visibility = True
		FreeCAD.setActiveDocument(doc.Name)
		FreeCAD.closeDocument(src_doc.Name)


def copy_part_recursive(src_obj,dst_doc,srcdstmap):
	# pylint: disable=F0401

	if src_obj.Name in srcdstmap:
		return srcdstmap[src_obj.Name]
	obj_copy = dst_doc.copyObject(src_obj)
	srcdstmap[src_obj.Name] = obj_copy
	for prop_name in src_obj.PropertiesList:
		prop = src_obj.getPropertyByName(prop_name)
		if 'ReadOnly' in src_obj.getTypeOfProperty(prop_name):
			pass
		elif isinstance(prop,tuple) or isinstance(prop,list):
			new_prop = []
			for p_item in prop:
				if isinstance(p_item,Part.Feature):
					new_prop.append(copy_part_recursive(p_item,dst_doc,srcdstmap))
				elif isinstance(p_item,Sketcher.Sketch):
					new_prop.append(dst_doc.copyObject(p_item))
				else:
					new_prop.append(p_item)
			if isinstance(prop,tuple):
				new_prop = tuple(new_prop)
			setattr(obj_copy,prop_name,new_prop)
		elif isinstance(prop,Sketcher.Sketch):
			setattr(obj_copy,prop_name,dst_doc.copyObject(prop))
		elif isinstance(prop,Part.Feature):
			setattr(obj_copy,prop_name,copy_part_recursive(prop,dst_doc,srcdstmap))
		else:
			setattr(obj_copy,prop_name,src_obj.getPropertyByName(prop_name))
	obj_copy.touch()
	gui_doc = FreeCADGui.getDocument(dst_doc.Name)
	gui_doc.getObject(obj_copy.Name).Visibility = False
	return obj_copy


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

class AngleWidget(QValueWidget):
	def __init__(self,parent,label,default):
		QValueWidget.__init__(self,parent)
		self.ui = Ui_ValueWidget()
		self.ui.setupUi(self)
		self.ui.label.setText(label)
		self.ui.valueEdit.setText(default)

		self.validator = QtGui.QDoubleValidator(self)
		self.validator.setRange(-360.,360.,2)
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
		self.ui.checkBox.setText(label)
		if default == "True":
			self.ui.checkBox.setChecked(True)
		else:
			self.ui.checkBox.setChecked(False)

	def getValue(self):
		return self.ui.checkBox.isChecked()

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
	def __init__(self,repo,freecad):
		QBoltsWidget.__init__(self)
		self.ui = Ui_BoltsWidget()
		self.ui.setupUi(self)

		self.repo = repo
		self.freecad = freecad

		self.param_widgets = {}
		self.props_widgets = {}

		self.coll_root = QtGui.QTreeWidgetItem(self.ui.partsTree,['Collections','Ordered by collections'])
		self.coll_root.setData(0,32,None)
		self.std_root = QtGui.QTreeWidgetItem(self.ui.partsTree,['Standard','Ordered by issueing body'])
		self.std_root.setData(0,32,None)

		#set up collections
		for coll in self.repo.collections:
			coll_item = QtGui.QTreeWidgetItem(self.coll_root,[coll.name, coll.description])
			coll_item.setData(0,32,coll)
			for cl in coll.classes:
				if not cl.id in self.freecad.getbase:
					continue
				cl_item = QtGui.QTreeWidgetItem(coll_item,[cl.name, cl.description])
				cl_item.setData(0,32,cl)

		#set up standards
		for body in repo.standard_bodies:
			std_item = QtGui.QTreeWidgetItem(self.std_root,[body, "Standards issued by %s" % body])
			std_item.setData(0,32,None)
			for cl in repo.standardized[body]:
				if not cl.id in self.freecad.getbase:
					continue
				cl_item = QtGui.QTreeWidgetItem(std_item,[cl.name, cl.description])
				cl_item.setData(0,32,cl)


		self.remove_empty_items(self.coll_root)

	def remove_empty_items(self,root_item):
		children = [root_item.child(i) for i in range(root_item.childCount())]
		for child in children:
			self.remove_empty_items(child)
			data = unpack(child.data(0,32))
			if not isinstance(data,BOLTSClass) and child.childCount() == 0:
				root_item.removeChild(child)

	def setup_param_widgets(self,cl,base):
		#construct widgets
		params = cl.parameters.union(base.parameters)

		for p in params.free:
			p_type = params.types[p]
			default = str(params.defaults[p])
			if p_type == "Length (mm)":
				self.param_widgets[p] = LengthWidget(self.ui.params,p + " (mm)",default)
			elif p_type == "Length (in)":
				self.param_widgets[p] = LengthWidget(self.ui.params,p + " (in)",default)
			elif p_type == "Number":
				self.param_widgets[p] = NumberWidget(self.ui.params,p,default)
			elif p_type == "Angle (deg)":
				self.param_widgets[p] = AngleWidget(self.ui.params,p + " (deg)",default)
			elif p_type == "Bool":
				self.param_widgets[p] = BoolWidget(self.ui.params,p,default)
			elif p_type == "Table Index":
				self.param_widgets[p] = TableIndexWidget(self.ui.params,p,params.choices[p],default)
			else:
				raise ValueError("Unknown type encountered for parameter %s: %s" % (p,p_type))
			self.param_widgets[p].setToolTip(params.description[p])
		#add them to layout
			self.ui.param_layout.addWidget(self.param_widgets[p])
		if base.type == "fcstd":
			self.ui.addButton.setText("Add part (may take a bit)")
		else:
			self.ui.addButton.setText("Add part")

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

	@Slot(bool)
	def on_addButton_clicked(self,checked):
		if FreeCAD.activeDocument() is None:
			FreeCAD.newDocument()

		items = self.ui.partsTree.selectedItems()

		if len(items) < 1:
			return

		data = unpack(items[0].data(0,32))

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

		lengths = {"Length (mm)" : "mm", "Length (in)" : "in"}

		for key,tp in data.parameters.types.iteritems():
			if tp in lengths:
				if params[key] is None:
					#A undefined value is not necessarily fatal
					continue
				revision = int(FreeCAD.Version()[2].split()[0])
				if revision >= 2836:
					params[key] = FreeCAD.Units.parseQuantity("%g %s" %
						(params[key], lengths[tp])).Value
				else:
					params[key] = FreeCAD.Units.translateUnit("%g %s" %
						(params[key], lengths[tp]))

		#add part
		try:
			base = self.freecad.getbase[data.id]
			add_part(base,params,FreeCAD.ActiveDocument)
			FreeCADGui.SendMsgToActiveView("ViewFit")
			FreeCAD.ActiveDocument.recompute()
		except ValueError as e:
			QtGui.QErrorMessage(self).showMessage(str(e))
		except Exception as e:
			FreeCAD.Console.PrintMessage(e)
			QtGui.QErrorMessage(self).showMessage("An error occured when trying to add the part: %s\nParameter Values: %s" % (e,params))

	@Slot()
	def on_partsTree_itemSelectionChanged(self):
		items = self.ui.partsTree.selectedItems()
		if len(items) < 1:
			return
		item = items[0]
		data = unpack(item.data(0,32))

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
			self.setup_param_widgets(data,self.freecad.getbase[data.id])
		elif isinstance(data,BOLTSCollection):
			self.setup_props_collection(data)
