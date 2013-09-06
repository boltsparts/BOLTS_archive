# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dim_widget.ui'
#
# Created: Fri Sep  6 15:01:59 2013
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

class Ui_dim_widget(object):
    def setupUi(self, dim_widget):
        dim_widget.setObjectName(_fromUtf8("dim_widget"))
        dim_widget.resize(150, 50)
        self.horizontalLayout = QtGui.QHBoxLayout(dim_widget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(dim_widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.valueEdit = QtGui.QLineEdit(dim_widget)
        self.valueEdit.setObjectName(_fromUtf8("valueEdit"))
        self.horizontalLayout.addWidget(self.valueEdit)

        self.retranslateUi(dim_widget)
        QtCore.QMetaObject.connectSlotsByName(dim_widget)

    def retranslateUi(self, dim_widget):
        dim_widget.setWindowTitle(_translate("dim_widget", "Form", None))
        self.label.setText(_translate("dim_widget", "TextLabel", None))

