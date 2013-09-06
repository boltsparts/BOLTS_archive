# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'key_widget.ui'
#
# Created: Fri Sep  6 15:01:52 2013
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

class Ui_key_widget(object):
    def setupUi(self, key_widget):
        key_widget.setObjectName(_fromUtf8("key_widget"))
        key_widget.resize(150, 50)
        self.verticalLayout = QtGui.QVBoxLayout(key_widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.comboBox = QtGui.QComboBox(key_widget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.verticalLayout.addWidget(self.comboBox)

        self.retranslateUi(key_widget)
        QtCore.QMetaObject.connectSlotsByName(key_widget)

    def retranslateUi(self, key_widget):
        key_widget.setWindowTitle(_translate("key_widget", "Form", None))

