from PyQt4 import QtGui, QtCore, uic
import FreeCAD
import sys
sys.path.append('..')
from os import listdir
from  blt_parser import load_collection

#get ui from designer file

##for development:
##compile Qt Designer stuff into module
#with open('bolts_widget.py','w') as pyfile:
#	uic.compileUi(open('bolts_widget.ui'),pyfile)
##by loading the module twice ui file changes are possible without restarting
##freecad, which is very convenient for development
#import bolts_widget
#reload(bolts_widget)

#for production:
import bolts_widget

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
	def setup_param_widget(self,ui):
		if 'key' in self.target_args:
			ui.key_combobox.clear()
			keys = [row[0] for row in sorted(self.data.iteritems(),key=lambda x: float(x[0][1:]))]
			for key in keys:
				ui.key_combobox.addItem(key)
		for arg in self.target_args:
			if arg == 'key':
				continue
			ui.param_label.setText(arg)
			ui.param_lineedit.setText('')

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

class BoltsWidget(QtGui.QDockWidget):
	def __init__(self,bases):
		QtGui.QDockWidget.__init__(self)
		self.ui = bolts_widget.Ui_BoltsWidget()
		self.ui.setupUi(self)

		self.bases = bases

		self.std_root = QtGui.QTreeWidgetItem(self.ui.partsTree,['Standards','Ordered by organisation'])
		self.std_root.setData(0,32,None)
		self.std_coll_items = {}
		for org in ['DIN','DINISO','EN','DINENISO','DINEN']:
			std_coll = StandardCollection(org,'%s standards' % org)
			self.std_coll_items[org] = std_coll.get_tree_item(self.std_root)

		self.coll_root = QtGui.QTreeWidgetItem(self.ui.partsTree,['Collections','Ordered by collections'])
		self.coll_root.setData(0,32,None)

		self.debug = ''

	def on_addButton_clicked(self,checked):
		items = self.ui.partsTree.selectedItems()
		if len(items) < 1:
			return
		item = items[0]
		data = item.data(0,32).toPyObject()

		if isinstance(data,BOLTSStandard):
			if data.base in self.bases:
				document = FreeCAD.ActiveDocument
				#assemble parameters
				params = {}
				key = str(self.ui.key_combobox.currentText())
				params['key'] = key
				params['name'] = data.name_template % (data.standard,key)
				for dim,val in zip(data.columns,data.data[key]):
					params[dim] = val
				params[self.ui.param_label.text()] = float(self.ui.param_lineedit.text())
				self.bases[data.base](params,document)


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
			self.debug = data.setup_param_widget(self.ui)
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


import washer
reload(washer)

widget = BoltsWidget(washer.bases)

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

#add parts

files = listdir('blt')
for file in files:
	blt = load_collection(file)
	widget.addCollection(blt)

mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, widget)
