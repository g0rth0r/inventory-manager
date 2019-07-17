# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchPart.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(385, 426)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 380, 361, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.loadPartLabel = QtGui.QLabel(Dialog)
        self.loadPartLabel.setGeometry(QtCore.QRect(10, 10, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.loadPartLabel.setFont(font)
        self.loadPartLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loadPartLabel.setObjectName(_fromUtf8("loadPartLabel"))
        self.searchLine = QtGui.QLineEdit(Dialog)
        self.searchLine.setGeometry(QtCore.QRect(70, 60, 291, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.searchLine.setFont(font)
        self.searchLine.setObjectName(_fromUtf8("searchLine"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 60, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.listResults = QtGui.QListWidget(Dialog)
        self.listResults.setGeometry(QtCore.QRect(70, 90, 291, 281))
        self.listResults.setObjectName(_fromUtf8("listResults"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.loadPartLabel.setText(_translate("Dialog", "Load Part Number", None))
        self.label.setText(_translate("Dialog", "Search: ", None))

