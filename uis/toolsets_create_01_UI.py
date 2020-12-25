# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'X:\app\win\Pipeline\uis222\toolsets_create_01.ui'
#
# Created: Tue May 21 15:31:17 2019
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

class Ui_C(object):
    def setupUi(self, C):
        C.setObjectName(_fromUtf8("C"))
        C.resize(321, 208)
        self.buttonBox = QtGui.QDialogButtonBox(C)
        self.buttonBox.setGeometry(QtCore.QRect(-30, 170, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.widget = QtGui.QWidget(C)
        self.widget.setGeometry(QtCore.QRect(10, 10, 301, 151))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout = QtGui.QFormLayout(self.widget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.l_menuSection = QtGui.QLabel(self.widget)
        self.l_menuSection.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.l_menuSection.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.l_menuSection.setObjectName(_fromUtf8("l_menuSection"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.l_menuSection)
        self.cb_menuSection = QtGui.QComboBox(self.widget)
        self.cb_menuSection.setObjectName(_fromUtf8("cb_menuSection"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cb_menuSection)
        self.le_name = QtGui.QLineEdit(self.widget)
        self.le_name.setObjectName(_fromUtf8("le_name"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.le_name)
        self.l_description = QtGui.QLabel(self.widget)
        self.l_description.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.l_description.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.l_description.setObjectName(_fromUtf8("l_description"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.l_description)
        self.pte_description = QtGui.QPlainTextEdit(self.widget)
        self.pte_description.setObjectName(_fromUtf8("pte_description"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.pte_description)
        self.l_name = QtGui.QLabel(self.widget)
        self.l_name.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.l_name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.l_name.setObjectName(_fromUtf8("l_name"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.l_name)

        self.retranslateUi(C)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), C.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), C.reject)
        QtCore.QMetaObject.connectSlotsByName(C)

    def retranslateUi(self, C):
        C.setWindowTitle(_translate("C", "Create Toolset", None))
        self.l_menuSection.setText(_translate("C", "Menu section:", None))
        self.l_description.setText(_translate("C", "Description:", None))
        self.l_name.setText(_translate("C", "Name:", None))

