# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Pipeline\houdini_app\Loader\backup\loader_v003.ui'
#
# Created: Thu Feb  3 18:23:27 2022
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_FileManager(object):
    def setupUi(self, FileManager):
        FileManager.setObjectName("FileManager")
        FileManager.setEnabled(True)
        FileManager.resize(1049, 697)
        FileManager.setStyleSheet("QDialog{\n"
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
"\n"
"\n"
"")
        self.verticalLayout_2 = QtGui.QVBoxLayout(FileManager)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_top = QtGui.QFrame(FileManager)
        self.frame_top.setMinimumSize(QtCore.QSize(0, 55))
        self.frame_top.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_top.setStyleSheet("QFrame{\n"
"background:rgb(45, 45, 45);\n"
"}")
        self.frame_top.setFrameShape(QtGui.QFrame.Box)
        self.frame_top.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_top.setLineWidth(1)
        self.frame_top.setObjectName("frame_top")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame_top)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setContentsMargins(9, -1, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lb_top = QtGui.QLabel(self.frame_top)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_top.setFont(font)
        self.lb_top.setObjectName("lb_top")
        self.horizontalLayout_4.addWidget(self.lb_top)
        self.verticalLayout_2.addWidget(self.frame_top)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(9, 0, 9, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(235, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pb_back = QtGui.QPushButton(FileManager)
        self.pb_back.setMaximumSize(QtCore.QSize(23, 21))
        self.pb_back.setText("")
        self.pb_back.setObjectName("pb_back")
        self.horizontalLayout.addWidget(self.pb_back)
        self.pb_next = QtGui.QPushButton(FileManager)
        self.pb_next.setMaximumSize(QtCore.QSize(23, 21))
        self.pb_next.setText("")
        self.pb_next.setObjectName("pb_next")
        self.horizontalLayout.addWidget(self.pb_next)
        spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.lb_path = QtGui.QLabel(FileManager)
        self.lb_path.setMinimumSize(QtCore.QSize(0, 25))
        self.lb_path.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_path.setFont(font)
        self.lb_path.setObjectName("lb_path")
        self.horizontalLayout.addWidget(self.lb_path)
        self.pb_viewGrid = QtGui.QPushButton(FileManager)
        self.pb_viewGrid.setMaximumSize(QtCore.QSize(23, 21))
        self.pb_viewGrid.setText("")
        self.pb_viewGrid.setObjectName("pb_viewGrid")
        self.horizontalLayout.addWidget(self.pb_viewGrid)
        self.pb_viewLine = QtGui.QPushButton(FileManager)
        self.pb_viewLine.setMaximumSize(QtCore.QSize(23, 21))
        self.pb_viewLine.setText("")
        self.pb_viewLine.setObjectName("pb_viewLine")
        self.horizontalLayout.addWidget(self.pb_viewLine)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_left = QtGui.QFrame(FileManager)
        self.frame_left.setStyleSheet("QFrame{\n"
"background:rgb(50, 50, 50);\n"
"}")
        self.frame_left.setFrameShape(QtGui.QFrame.Box)
        self.frame_left.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_left.setObjectName("frame_left")
        self.gridLayout = QtGui.QGridLayout(self.frame_left)
        self.gridLayout.setObjectName("gridLayout")
        self.label_sequence = QtGui.QLabel(self.frame_left)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_sequence.setFont(font)
        self.label_sequence.setObjectName("label_sequence")
        self.gridLayout.addWidget(self.label_sequence, 1, 0, 1, 1)
        self.label_project = QtGui.QLabel(self.frame_left)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_project.setFont(font)
        self.label_project.setObjectName("label_project")
        self.gridLayout.addWidget(self.label_project, 0, 0, 1, 1)
        self.cbox_project = QtGui.QComboBox(self.frame_left)
        self.cbox_project.setMinimumSize(QtCore.QSize(150, 0))
        self.cbox_project.setObjectName("cbox_project")
        self.gridLayout.addWidget(self.cbox_project, 0, 1, 1, 1)
        self.cbox_sequence = QtGui.QComboBox(self.frame_left)
        self.cbox_sequence.setEnabled(True)
        self.cbox_sequence.setMinimumSize(QtCore.QSize(100, 0))
        self.cbox_sequence.setObjectName("cbox_sequence")
        self.gridLayout.addWidget(self.cbox_sequence, 1, 1, 1, 1)
        self.label_type = QtGui.QLabel(self.frame_left)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_type.setFont(font)
        self.label_type.setObjectName("label_type")
        self.gridLayout.addWidget(self.label_type, 2, 0, 1, 1)
        self.cbox_type = QtGui.QComboBox(self.frame_left)
        self.cbox_type.setMinimumSize(QtCore.QSize(100, 0))
        self.cbox_type.setObjectName("cbox_type")
        self.cbox_type.addItem("")
        self.cbox_type.addItem("")
        self.cbox_type.addItem("")
        self.cbox_type.addItem("")
        self.gridLayout.addWidget(self.cbox_type, 2, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 6, 1, 1, 1)
        self.pb_byname = QtGui.QPushButton(self.frame_left)
        self.pb_byname.setObjectName("pb_byname")
        self.gridLayout.addWidget(self.pb_byname, 4, 1, 1, 1)
        self.pb_bydate = QtGui.QPushButton(self.frame_left)
        self.pb_bydate.setObjectName("pb_bydate")
        self.gridLayout.addWidget(self.pb_bydate, 3, 1, 1, 1)
        self.pb_reverse = QtGui.QPushButton(self.frame_left)
        self.pb_reverse.setObjectName("pb_reverse")
        self.gridLayout.addWidget(self.pb_reverse, 5, 1, 1, 1)
        self.horizontalLayout_3.addWidget(self.frame_left)
        self.listWidget_files = QtGui.QListWidget(FileManager)
        self.listWidget_files.setFrameShape(QtGui.QFrame.Box)
        self.listWidget_files.setFrameShadow(QtGui.QFrame.Raised)
        self.listWidget_files.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.listWidget_files.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.listWidget_files.setMovement(QtGui.QListView.Static)
        self.listWidget_files.setFlow(QtGui.QListView.LeftToRight)
        self.listWidget_files.setProperty("isWrapping", True)
        self.listWidget_files.setResizeMode(QtGui.QListView.Adjust)
        self.listWidget_files.setLayoutMode(QtGui.QListView.Batched)
        self.listWidget_files.setSpacing(23)
        self.listWidget_files.setViewMode(QtGui.QListView.ListMode)
        self.listWidget_files.setModelColumn(0)
        self.listWidget_files.setUniformItemSizes(False)
        self.listWidget_files.setWordWrap(False)
        self.listWidget_files.setObjectName("listWidget_files")
        QtGui.QListWidgetItem(self.listWidget_files)
        QtGui.QListWidgetItem(self.listWidget_files)
        QtGui.QListWidgetItem(self.listWidget_files)
        QtGui.QListWidgetItem(self.listWidget_files)
        QtGui.QListWidgetItem(self.listWidget_files)
        QtGui.QListWidgetItem(self.listWidget_files)
        QtGui.QListWidgetItem(self.listWidget_files)
        QtGui.QListWidgetItem(self.listWidget_files)
        QtGui.QListWidgetItem(self.listWidget_files)
        QtGui.QListWidgetItem(self.listWidget_files)
        self.horizontalLayout_3.addWidget(self.listWidget_files)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtGui.QSpacerItem(245, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.h_slider_zoomView = QtGui.QSlider(FileManager)
        self.h_slider_zoomView.setMinimumSize(QtCore.QSize(150, 0))
        self.h_slider_zoomView.setMaximumSize(QtCore.QSize(150, 16777215))
        self.h_slider_zoomView.setOrientation(QtCore.Qt.Horizontal)
        self.h_slider_zoomView.setObjectName("h_slider_zoomView")
        self.horizontalLayout_2.addWidget(self.h_slider_zoomView)
        spacerItem4 = QtGui.QSpacerItem(408, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.frame_bottom = QtGui.QFrame(FileManager)
        self.frame_bottom.setStyleSheet("QFrame{\n"
"background:rgb(50, 50, 50);\n"
"}")
        self.frame_bottom.setFrameShape(QtGui.QFrame.Box)
        self.frame_bottom.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_bottom.setObjectName("frame_bottom")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frame_bottom)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pb_pref = QtGui.QPushButton(self.frame_bottom)
        self.pb_pref.setMinimumSize(QtCore.QSize(80, 25))
        self.pb_pref.setObjectName("pb_pref")
        self.horizontalLayout_5.addWidget(self.pb_pref)
        spacerItem5 = QtGui.QSpacerItem(460, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.pb_new = QtGui.QPushButton(self.frame_bottom)
        self.pb_new.setMinimumSize(QtCore.QSize(70, 25))
        self.pb_new.setObjectName("pb_new")
        self.horizontalLayout_5.addWidget(self.pb_new)
        self.pb_save = QtGui.QPushButton(self.frame_bottom)
        self.pb_save.setMinimumSize(QtCore.QSize(70, 25))
        self.pb_save.setObjectName("pb_save")
        self.horizontalLayout_5.addWidget(self.pb_save)
        self.pb_select_shot = QtGui.QPushButton(self.frame_bottom)
        self.pb_select_shot.setMinimumSize(QtCore.QSize(80, 25))
        self.pb_select_shot.setObjectName("pb_select_shot")
        self.horizontalLayout_5.addWidget(self.pb_select_shot)
        spacerItem6 = QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.pb_open = QtGui.QPushButton(self.frame_bottom)
        self.pb_open.setMinimumSize(QtCore.QSize(60, 25))
        self.pb_open.setObjectName("pb_open")
        self.horizontalLayout_5.addWidget(self.pb_open)
        self.pb_close = QtGui.QPushButton(self.frame_bottom)
        self.pb_close.setMinimumSize(QtCore.QSize(60, 25))
        self.pb_close.setObjectName("pb_close")
        self.horizontalLayout_5.addWidget(self.pb_close)
        self.verticalLayout_2.addWidget(self.frame_bottom)

        self.retranslateUi(FileManager)
        QtCore.QMetaObject.connectSlotsByName(FileManager)

    def retranslateUi(self, FileManager):
        FileManager.setWindowTitle(QtGui.QApplication.translate("FileManager", "File Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_top.setText(QtGui.QApplication.translate("FileManager", "Loader", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_path.setText(QtGui.QApplication.translate("FileManager", "/Storage/Project/", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sequence.setText(QtGui.QApplication.translate("FileManager", "Sequence:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_project.setText(QtGui.QApplication.translate("FileManager", "Project:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_type.setText(QtGui.QApplication.translate("FileManager", "Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.cbox_type.setItemText(0, QtGui.QApplication.translate("FileManager", "FX", None, QtGui.QApplication.UnicodeUTF8))
        self.cbox_type.setItemText(1, QtGui.QApplication.translate("FileManager", "LIGHTING", None, QtGui.QApplication.UnicodeUTF8))
        self.cbox_type.setItemText(2, QtGui.QApplication.translate("FileManager", "ANIMATION", None, QtGui.QApplication.UnicodeUTF8))
        self.cbox_type.setItemText(3, QtGui.QApplication.translate("FileManager", "MODELING", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_byname.setText(QtGui.QApplication.translate("FileManager", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_bydate.setText(QtGui.QApplication.translate("FileManager", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_reverse.setText(QtGui.QApplication.translate("FileManager", "Invert ", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.listWidget_files.isSortingEnabled()
        self.listWidget_files.setSortingEnabled(False)
        self.listWidget_files.item(0).setText(QtGui.QApplication.translate("FileManager", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_files.item(1).setText(QtGui.QApplication.translate("FileManager", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_files.item(2).setText(QtGui.QApplication.translate("FileManager", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_files.item(3).setText(QtGui.QApplication.translate("FileManager", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_files.item(4).setText(QtGui.QApplication.translate("FileManager", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_files.item(5).setText(QtGui.QApplication.translate("FileManager", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_files.item(6).setText(QtGui.QApplication.translate("FileManager", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_files.item(7).setText(QtGui.QApplication.translate("FileManager", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_files.item(8).setText(QtGui.QApplication.translate("FileManager", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_files.item(9).setText(QtGui.QApplication.translate("FileManager", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_files.setSortingEnabled(__sortingEnabled)
        self.pb_pref.setText(QtGui.QApplication.translate("FileManager", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_new.setText(QtGui.QApplication.translate("FileManager", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_save.setText(QtGui.QApplication.translate("FileManager", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_select_shot.setText(QtGui.QApplication.translate("FileManager", "Select Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_open.setText(QtGui.QApplication.translate("FileManager", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_close.setText(QtGui.QApplication.translate("FileManager", "Close", None, QtGui.QApplication.UnicodeUTF8))

import icons_v002_rc