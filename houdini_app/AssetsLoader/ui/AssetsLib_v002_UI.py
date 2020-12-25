# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\dev\Pipeline\houdini\AssetsLoader\ui\AssetsLib_v002.ui'
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

class Ui_AssetsLib(object):
    def setupUi(self, AssetsLib):
        AssetsLib.setObjectName(_fromUtf8("AssetsLib"))
        AssetsLib.resize(885, 728)
        AssetsLib.setStyleSheet(_fromUtf8("QDialog{\n"
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
"QListWidget:item{\n"
"color:rgb(196,196,196);\n"
"}\n"
"QListWidget{\n"
"alternate-background-color:rgb(30,30,30);\n"
"}\n"
"\n"
""))
        self.vLayoutMain = QtGui.QVBoxLayout(AssetsLib)
        self.vLayoutMain.setObjectName(_fromUtf8("vLayoutMain"))
        self.hLayout_top = QtGui.QHBoxLayout()
        self.hLayout_top.setObjectName(_fromUtf8("hLayout_top"))
        self.vLayout_category = QtGui.QVBoxLayout()
        self.vLayout_category.setObjectName(_fromUtf8("vLayout_category"))
        self.lb_category = QtGui.QLabel(AssetsLib)
        self.lb_category.setObjectName(_fromUtf8("lb_category"))
        self.vLayout_category.addWidget(self.lb_category)
        self.cbox_category = QtGui.QComboBox(AssetsLib)
        self.cbox_category.setMinimumSize(QtCore.QSize(150, 23))
        self.cbox_category.setObjectName(_fromUtf8("cbox_category"))
        self.cbox_category.addItem(_fromUtf8(""))
        self.cbox_category.addItem(_fromUtf8(""))
        self.cbox_category.addItem(_fromUtf8(""))
        self.cbox_category.addItem(_fromUtf8(""))
        self.vLayout_category.addWidget(self.cbox_category)
        self.hLayout_top.addLayout(self.vLayout_category)
        self.vLayout_search = QtGui.QVBoxLayout()
        self.vLayout_search.setObjectName(_fromUtf8("vLayout_search"))
        self.lb_search = QtGui.QLabel(AssetsLib)
        self.lb_search.setObjectName(_fromUtf8("lb_search"))
        self.vLayout_search.addWidget(self.lb_search)
        self.le_search = QtGui.QLineEdit(AssetsLib)
        self.le_search.setMinimumSize(QtCore.QSize(0, 23))
        self.le_search.setObjectName(_fromUtf8("le_search"))
        self.vLayout_search.addWidget(self.le_search)
        self.hLayout_top.addLayout(self.vLayout_search)
        self.vLayoutMain.addLayout(self.hLayout_top)
        self.listWidget_lib = QtGui.QListWidget(AssetsLib)
        self.listWidget_lib.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.listWidget_lib.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.listWidget_lib.setMovement(QtGui.QListView.Static)
        self.listWidget_lib.setFlow(QtGui.QListView.LeftToRight)
        self.listWidget_lib.setProperty("isWrapping", True)
        self.listWidget_lib.setResizeMode(QtGui.QListView.Adjust)
        self.listWidget_lib.setLayoutMode(QtGui.QListView.Batched)
        self.listWidget_lib.setViewMode(QtGui.QListView.ListMode)
        self.listWidget_lib.setModelColumn(0)
        self.listWidget_lib.setUniformItemSizes(False)
        self.listWidget_lib.setWordWrap(False)
        self.listWidget_lib.setObjectName(_fromUtf8("listWidget_lib"))
        self.vLayoutMain.addWidget(self.listWidget_lib)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.hSlider_zoom = QtGui.QSlider(AssetsLib)
        self.hSlider_zoom.setMaximumSize(QtCore.QSize(200, 16777215))
        self.hSlider_zoom.setMinimum(50)
        self.hSlider_zoom.setMaximum(400)
        self.hSlider_zoom.setOrientation(QtCore.Qt.Horizontal)
        self.hSlider_zoom.setObjectName(_fromUtf8("hSlider_zoom"))
        self.horizontalLayout.addWidget(self.hSlider_zoom)
        self.vLayoutMain.addLayout(self.horizontalLayout)

        self.retranslateUi(AssetsLib)
        QtCore.QMetaObject.connectSlotsByName(AssetsLib)

    def retranslateUi(self, AssetsLib):
        AssetsLib.setWindowTitle(_translate("AssetsLib", "AssetsLib", None))
        self.lb_category.setText(_translate("AssetsLib", "Category:", None))
        self.cbox_category.setItemText(0, _translate("AssetsLib", "Char", None))
        self.cbox_category.setItemText(1, _translate("AssetsLib", "Env", None))
        self.cbox_category.setItemText(2, _translate("AssetsLib", "Fx", None))
        self.cbox_category.setItemText(3, _translate("AssetsLib", "Props", None))
        self.lb_search.setText(_translate("AssetsLib", "Search:", None))

