# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\dev\Pipeline\houdini\AssetsLoader\ui\AssetsLib_v001.ui'
#
# Created: Thu Nov 08 16:16:35 2018
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


class Ui_AssetsLib(object):
    def setupUi(self, AssetsLib):
        AssetsLib.setObjectName("AssetsLib")
        AssetsLib.resize(887, 728)
        AssetsLib.setStyleSheet("QWidget#AssetsLib{\n"
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
"QListWidget:item{\n"
"color:rgb(196,196,196);\n"
"}\n"
"QListWidget{\n"
"alternate-background-color:rgb(30,30,30);\n"
"}\n"
"\n"
"")
        self.vLayoutMain = QVBoxLayout(AssetsLib)
        self.vLayoutMain.setObjectName("vLayoutMain")
        self.hLayout_top = QHBoxLayout()
        self.hLayout_top.setObjectName("hLayout_top")
        self.vLayout_category = QVBoxLayout()
        self.vLayout_category.setObjectName("vLayout_category")
        self.lb_category = QLabel(AssetsLib)
        self.lb_category.setObjectName("lb_category")
        self.vLayout_category.addWidget(self.lb_category)
        self.cbox_category = QComboBox(AssetsLib)
        self.cbox_category.setMinimumSize(QSize(150, 23))
        self.cbox_category.setObjectName("cbox_category")
        self.cbox_category.addItem("")
        self.cbox_category.addItem("")
        self.cbox_category.addItem("")
        self.cbox_category.addItem("")
        self.vLayout_category.addWidget(self.cbox_category)
        self.hLayout_top.addLayout(self.vLayout_category)
        self.vLayout_search = QVBoxLayout()
        self.vLayout_search.setObjectName("vLayout_search")
        self.lb_search = QLabel(AssetsLib)
        self.lb_search.setObjectName("lb_search")
        self.vLayout_search.addWidget(self.lb_search)
        self.le_search = QLineEdit(AssetsLib)
        self.le_search.setMinimumSize(QSize(0, 23))
        self.le_search.setObjectName("le_search")
        self.vLayout_search.addWidget(self.le_search)
        self.hLayout_top.addLayout(self.vLayout_search)
        self.vLayoutMain.addLayout(self.hLayout_top)
        self.listWidget_lib = QListWidget(AssetsLib)
        self.listWidget_lib.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.listWidget_lib.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.listWidget_lib.setMovement(QListView.Static)
        self.listWidget_lib.setFlow(QListView.LeftToRight)
        self.listWidget_lib.setResizeMode(QListView.Adjust)
        self.listWidget_lib.setLayoutMode(QListView.Batched)
        self.listWidget_lib.setSpacing(9)
        self.listWidget_lib.setWrapping(True)
        self.listWidget_lib.setModelColumn(0)
        self.listWidget_lib.setUniformItemSizes(False)
        self.listWidget_lib.setWordWrap(False)
        self.listWidget_lib.setObjectName("listWidget_lib")
        self.vLayoutMain.addWidget(self.listWidget_lib)

        self.retranslateUi(AssetsLib)
        QMetaObject.connectSlotsByName(AssetsLib)

    def retranslateUi(self, AssetsLib):
        AssetsLib.setWindowTitle("AssetsLib")
        self.lb_category.setText("Category:")
        self.cbox_category.setItemText(0, "Char")
        self.cbox_category.setItemText(1, "Env")
        self.cbox_category.setItemText(2, "Fx")
        self.cbox_category.setItemText(3, "Props")
        self.lb_search.setText("Search:")
        __sortingEnabled = self.listWidget_lib.isSortingEnabled()
        self.listWidget_lib.setSortingEnabled(False)
        self.listWidget_lib.setSortingEnabled(__sortingEnabled)

