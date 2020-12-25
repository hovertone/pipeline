# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'X:\app\win\Pipeline\uis222\toolsets_create_03.ui'
#
# Created: Wed May 22 13:10:33 2019
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
        self.le_name.setPlaceholderText(_fromUtf8(""))
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
        self.widget1 = QtGui.QWidget(C)
        self.widget1.setGeometry(QtCore.QRect(150, 170, 158, 25))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget1)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pb_ok = QtGui.QPushButton(self.widget1)
        self.pb_ok.setObjectName(_fromUtf8("pb_ok"))
        self.horizontalLayout.addWidget(self.pb_ok)
        self.pb_cancel = QtGui.QPushButton(self.widget1)
        self.pb_cancel.setObjectName(_fromUtf8("pb_cancel"))
        self.horizontalLayout.addWidget(self.pb_cancel)

        self.retranslateUi(C)
        QtCore.QMetaObject.connectSlotsByName(C)

    def retranslateUi(self, C):
        C.setWindowTitle(_translate("C", "Create Toolset", None))
        self.l_menuSection.setText(_translate("C", "Menu section:", None))
        self.le_name.setToolTip(_translate("C", "English text only", None))
        self.l_description.setText(_translate("C", "Description:", None))
        self.pte_description.setToolTip(_translate("C", "А тут можно и на русском", None))
        self.l_name.setText(_translate("C", "Name:", None))
        self.pb_ok.setToolTip(_translate("C", "asdfasdf", None))
        self.pb_ok.setText(_translate("C", "OK", None))
        self.pb_cancel.setText(_translate("C", "Cancel", None))

