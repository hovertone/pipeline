# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'X:\app\win\Pipeline\uis222\toolsets_create_01.ui'
#
# Created: Tue May 21 15:31:18 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class toolset_create_ui(object):
    def setupUi(self, C):
        C.setObjectName("C")
        C.resize(321, 208)
        self.buttonBox = QtGui.QDialogButtonBox(C)
        self.buttonBox.setGeometry(QtCore.QRect(-30, 170, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtGui.QWidget(C)
        self.widget.setGeometry(QtCore.QRect(10, 10, 301, 151))
        self.widget.setObjectName("widget")
        self.formLayout = QtGui.QFormLayout(self.widget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.l_menuSection = QtGui.QLabel(self.widget)
        self.l_menuSection.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.l_menuSection.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.l_menuSection.setObjectName("l_menuSection")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.l_menuSection)
        self.cb_menuSection = QtGui.QComboBox(self.widget)
        self.cb_menuSection.setObjectName("cb_menuSection")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cb_menuSection)
        self.le_name = QtGui.QLineEdit(self.widget)
        self.le_name.setObjectName("le_name")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.le_name)
        self.l_description = QtGui.QLabel(self.widget)
        self.l_description.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.l_description.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.l_description.setObjectName("l_description")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.l_description)
        self.pte_description = QtGui.QPlainTextEdit(self.widget)
        self.pte_description.setObjectName("pte_description")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.pte_description)
        self.l_name = QtGui.QLabel(self.widget)
        self.l_name.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.l_name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.l_name.setObjectName("l_name")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.l_name)

        self.retranslateUi(C)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), C.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), C.reject)
        QtCore.QMetaObject.connectSlotsByName(C)

    def retranslateUi(self, C):
        C.setWindowTitle(QtGui.QApplication.translate("C", "Create Toolset", None, QtGui.QApplication.UnicodeUTF8))
        self.l_menuSection.setText(QtGui.QApplication.translate("C", "Menu section:", None, QtGui.QApplication.UnicodeUTF8))
        self.l_description.setText(QtGui.QApplication.translate("C", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.l_name.setText(QtGui.QApplication.translate("C", "Name:", None, QtGui.QApplication.UnicodeUTF8))

