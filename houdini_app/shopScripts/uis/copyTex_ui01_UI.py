# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'X:\app\win\Pipeline\houdini_app\shopScripts\uis222\copyTex_ui01.ui'
#
# Created: Thu Jul 16 14:07:30 2020
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
        Dialog.resize(562, 300)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblWhereToSplit = QLabel(Dialog)
        self.lblWhereToSplit.setObjectName("lblWhereToSplit")
        self.verticalLayout.addWidget(self.lblWhereToSplit)
        self.leExistingPath = QLineEdit(Dialog)
        self.leExistingPath.setEnabled(False)
        self.leExistingPath.setObjectName("leExistingPath")
        self.verticalLayout.addWidget(self.leExistingPath)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblEnterFolderName = QLabel(Dialog)
        self.lblEnterFolderName.setObjectName("lblEnterFolderName")
        self.horizontalLayout.addWidget(self.lblEnterFolderName)
        self.leEnterFolderName = QLineEdit(Dialog)
        self.leEnterFolderName.setObjectName("leEnterFolderName")
        self.horizontalLayout.addWidget(self.leEnterFolderName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lblResultAmount = QLabel(self.groupBox)
        self.lblResultAmount.setObjectName("lblResultAmount")
        self.verticalLayout_4.addWidget(self.lblResultAmount)
        self.lstResultFolders = QListWidget(self.groupBox)
        self.lstResultFolders.setEnabled(False)
        self.lstResultFolders.setObjectName("lstResultFolders")
        self.verticalLayout_4.addWidget(self.lstResultFolders)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout.addWidget(self.groupBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), Dialog.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Dialog")
        self.lblWhereToSplit.setText("At what point should we split path?")
        self.lblEnterFolderName.setText("Enter folder name:")
        self.groupBox.setTitle("Result")
        self.lblResultAmount.setText("No match so far. Enter folder name above.")

