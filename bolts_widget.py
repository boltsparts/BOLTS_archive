# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bolts_widget.ui'
#
# Created: Thu Sep  5 17:19:49 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_BoltsWidget(object):
    def setupUi(self, BoltsWidget):
        BoltsWidget.setObjectName(_fromUtf8("BoltsWidget"))
        BoltsWidget.resize(333, 316)
        self.content = QtGui.QWidget()
        self.content.setEnabled(True)
        self.content.setObjectName(_fromUtf8("content"))
        self.gridLayoutWidget = QtGui.QWidget(self.content)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 258, 322))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gridLayoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.partsTree = QtGui.QTreeWidget(self.gridLayoutWidget)
        self.partsTree.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.partsTree.setAutoExpandDelay(1)
        self.partsTree.setExpandsOnDoubleClick(False)
        self.partsTree.setColumnCount(2)
        self.partsTree.setObjectName(_fromUtf8("partsTree"))
        self.partsTree.headerItem().setText(0, _fromUtf8("Name"))
        self.partsTree.header().setDefaultSectionSize(150)
        self.partsTree.header().setMinimumSectionSize(50)
        self.partsTree.header().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.partsTree)
        self.name = QtGui.QLabel(self.gridLayoutWidget)
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.verticalLayout_2.addWidget(self.name)
        self.description = QtGui.QLabel(self.gridLayoutWidget)
        self.description.setText(_fromUtf8(""))
        self.description.setObjectName(_fromUtf8("description"))
        self.verticalLayout_2.addWidget(self.description)
        self.params = QtGui.QWidget(self.gridLayoutWidget)
        self.params.setObjectName(_fromUtf8("params"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.params)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.key_combobox = QtGui.QComboBox(self.params)
        self.key_combobox.setObjectName(_fromUtf8("key_combobox"))
        self.horizontalLayout.addWidget(self.key_combobox)
        self.param_label = QtGui.QLabel(self.params)
        self.param_label.setMinimumSize(QtCore.QSize(20, 0))
        self.param_label.setText(_fromUtf8(""))
        self.param_label.setObjectName(_fromUtf8("param_label"))
        self.horizontalLayout.addWidget(self.param_label)
        self.param_lineedit = QtGui.QLineEdit(self.params)
        self.param_lineedit.setObjectName(_fromUtf8("param_lineedit"))
        self.horizontalLayout.addWidget(self.param_lineedit)
        self.verticalLayout_2.addWidget(self.params)
        self.addButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout_2.addWidget(self.addButton)
        BoltsWidget.setWidget(self.content)

        self.retranslateUi(BoltsWidget)
        QtCore.QMetaObject.connectSlotsByName(BoltsWidget)

    def retranslateUi(self, BoltsWidget):
        BoltsWidget.setWindowTitle(_translate("BoltsWidget", "Standard Parts Selector", None))
        self.partsTree.headerItem().setText(1, _translate("BoltsWidget", "Description", None))
        self.addButton.setText(_translate("BoltsWidget", "Add Part", None))

