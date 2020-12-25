# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'X:\app\win\Pipeline\houdini_app\shopScripts\uis\copyTex_ui02.ui'
#
# Created: Fri Jul 17 16:24:49 2020
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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(737, 390)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.replaceLayout = QHBoxLayout()
        self.replaceLayout.setObjectName("replaceLayout")
        self.lblReplaceThis = QLabel(Dialog)
        self.lblReplaceThis.setObjectName("lblReplaceThis")
        self.replaceLayout.addWidget(self.lblReplaceThis)
        self.leReplaceThis = QLineEdit(Dialog)
        self.leReplaceThis.setObjectName("leReplaceThis")
        self.replaceLayout.addWidget(self.leReplaceThis)
        self.lblWithThis = QLabel(Dialog)
        self.lblWithThis.setObjectName("lblWithThis")
        self.replaceLayout.addWidget(self.lblWithThis)
        self.leWithThis = QLineEdit(Dialog)
        self.leWithThis.setObjectName("leWithThis")
        self.replaceLayout.addWidget(self.leWithThis)
        self.verticalLayout.addLayout(self.replaceLayout)
        self.table = QTableWidget(Dialog)
        self.table.setColumnCount(0)
        self.table.setObjectName("table")
        self.table.setColumnCount(2)
        self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.table)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_ok = QPushButton(Dialog)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.pushButton_cancel = QPushButton(Dialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Lets substitute folder paths")
        self.lblReplaceThis.setText("Replace This:")
        self.lblWithThis.setText("With This:")
        self.pushButton_ok.setText("OK")
        self.pushButton_cancel.setText("Cancel")

