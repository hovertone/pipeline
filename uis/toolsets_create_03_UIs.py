# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'X:\app\win\Pipeline\uis222\toolsets_create_03.ui'
#
# Created: Wed May 22 13:10:34 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

class toolset_create_ui(object):
    def setupUi(self, C):
        C.setObjectName("C")
        C.resize(321, 208)
        self.widget = QWidget(C)
        self.widget.setGeometry(QRect(10, 10, 301, 151))
        self.widget.setObjectName("widget")
        self.formLayout = QFormLayout(self.widget)
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.l_menuSection = QLabel(self.widget)
        self.l_menuSection.setLayoutDirection(Qt.LeftToRight)
        self.l_menuSection.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.l_menuSection.setObjectName("l_menuSection")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.l_menuSection)
        self.cb_menuSection = QComboBox(self.widget)
        self.cb_menuSection.setObjectName("cb_menuSection")
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cb_menuSection)
        self.le_name = QLineEdit(self.widget)
        self.le_name.setPlaceholderText("")
        self.le_name.setObjectName("le_name")
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.le_name)
        self.l_description = QLabel(self.widget)
        self.l_description.setLayoutDirection(Qt.RightToLeft)
        self.l_description.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.l_description.setObjectName("l_description")
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.l_description)
        self.pte_description = QPlainTextEdit(self.widget)
        self.pte_description.setObjectName("pte_description")
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.pte_description)
        self.l_name = QLabel(self.widget)
        self.l_name.setLayoutDirection(Qt.RightToLeft)
        self.l_name.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.l_name.setObjectName("l_name")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.l_name)
        self.widget1 = QWidget(C)
        self.widget1.setGeometry(QRect(150, 170, 158, 25))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_ok = QPushButton(self.widget1)
        self.pb_ok.setObjectName("pb_ok")
        self.horizontalLayout.addWidget(self.pb_ok)
        self.pb_cancel = QPushButton(self.widget1)
        self.pb_cancel.setObjectName("pb_cancel")
        self.horizontalLayout.addWidget(self.pb_cancel)

        self.retranslateUi(C)
        QMetaObject.connectSlotsByName(C)

    def retranslateUi(self, C):
        C.setWindowTitle("Create Toolset")
        self.l_menuSection.setText("Menu section:")
        self.le_name.setToolTip("English text only")
        self.l_description.setText("Description:")
        self.pte_description.setToolTip("А тут можно и на русском")
        self.l_name.setText("Name:")
        self.pb_ok.setToolTip("asdfasdf")
        self.pb_ok.setText("OK")
        self.pb_cancel.setText("Cancel")

