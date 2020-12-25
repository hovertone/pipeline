# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\dev\Pipeline\houdini\Loader\assetName_v001.ui'
#
# Created: Wed Nov 07 12:46:09 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    import hou
except:
    from PySide.QtGui import *
    from PySide.QtCore import *



class Ui_AssetName(object):
    def setupUi(self, AssetName):
        AssetName.setObjectName("AssetName")
        AssetName.resize(409, 128)
        AssetName.setStyleSheet("QWidget{\n"
"background:rgb(58,58,58);\n"
"}\n"
"\n"
"QLabel{\n"
"color:rgb(196,196,196);\n"
"}\n"
"\n"
"QListWidget{\n"
"background:rgb(48,48,48);\n"
"}\n"
"\n"
"QPushButton{\n"
"background:qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(60,60, 60, 255), stop:1 rgba(85, 85, 85, 255));\n"
"border:1px solid black;\n"
"color:rgb(196,196,196);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background:qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(68,68, 68, 255), stop:1 rgba(93, 93, 93, 255));\n"
"border:1px solid black;\n"
"color:rgb(196,196,196);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background:rgb(185,134,32);\n"
"border:1px solid black;\n"
"color:rgb(196,196,196);\n"
"}\n"
"\n"
"QLineEdit{\n"
"background:rgb(48,48,48);\n"
"color:rgb(196,196,196);\n"
"border:1px solid gray;\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.vLayoutMain = QVBoxLayout(AssetName)
        self.vLayoutMain.setObjectName("vLayoutMain")
        self.hLayoutProjects = QHBoxLayout()
        self.hLayoutProjects.setObjectName("hLayoutProjects")
        self.lb_assetName = QLabel(AssetName)
        self.lb_assetName.setMinimumSize(QSize(90, 0))
        self.lb_assetName.setObjectName("lb_assetName")
        self.hLayoutProjects.addWidget(self.lb_assetName)
        self.le_assetName = QLineEdit(AssetName)
        self.le_assetName.setObjectName("le_assetName")
        self.hLayoutProjects.addWidget(self.le_assetName)
        self.vLayoutMain.addLayout(self.hLayoutProjects)
        self.hLayoutBtns = QHBoxLayout()
        self.hLayoutBtns.setObjectName("hLayoutBtns")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayoutBtns.addItem(spacerItem)
        self.pb_cancel = QPushButton(AssetName)
        self.pb_cancel.setMinimumSize(QSize(50, 23))
        self.pb_cancel.setObjectName("pb_cancel")
        self.hLayoutBtns.addWidget(self.pb_cancel)
        self.pb_save = QPushButton(AssetName)
        self.pb_save.setMinimumSize(QSize(50, 23))
        self.pb_save.setObjectName("pb_save")
        self.hLayoutBtns.addWidget(self.pb_save)
        self.vLayoutMain.addLayout(self.hLayoutBtns)

        self.retranslateUi(AssetName)
        QMetaObject.connectSlotsByName(AssetName)

    def retranslateUi(self, AssetName):
        AssetName.setWindowTitle("AssetName")
        self.lb_assetName.setText("Asset name:")
        self.pb_cancel.setText("Cancel")
        self.pb_save.setText("Save")

