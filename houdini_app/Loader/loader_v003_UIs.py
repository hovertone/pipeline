# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'X:\app\win\Pipeline\houdini_app\Loader\loader_v003.ui'
#
# Created: Tue Apr 16 15:23:20 2019
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
import sys

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
        self.verticalLayout_2 = QVBoxLayout(FileManager)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_top = QFrame(FileManager)
        self.frame_top.setMinimumSize(QSize(0, 55))
        self.frame_top.setMaximumSize(QSize(16777215, 50))
        self.frame_top.setStyleSheet("QFrame{\n"
"background:rgb(45, 45, 45);\n"
"}")
        self.frame_top.setFrameShape(QFrame.Box)
        self.frame_top.setFrameShadow(QFrame.Raised)
        self.frame_top.setLineWidth(1)
        self.frame_top.setObjectName("frame_top")
        self.horizontalLayout_4 = QHBoxLayout(self.frame_top)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setContentsMargins(9, -1, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lb_top = QLabel(self.frame_top)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_top.setFont(font)
        self.lb_top.setObjectName("lb_top")
        self.horizontalLayout_4.addWidget(self.lb_top)
        self.verticalLayout_2.addWidget(self.frame_top)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(9, 0, 9, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(235, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pb_back = QPushButton(FileManager)
        self.pb_back.setMaximumSize(QSize(26, 21))
        self.pb_back.setText("")
        self.pb_back.setObjectName("pb_back")
        self.horizontalLayout.addWidget(self.pb_back)

        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.lb_path = QLabel(FileManager)
        self.lb_path.setMinimumSize(QSize(0, 25))
        self.lb_path.setMaximumSize(QSize(16777215, 25))
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_path.setFont(font)
        self.lb_path.setObjectName("lb_path")
        self.horizontalLayout.addWidget(self.lb_path)
        self.pb_viewGrid = QPushButton(FileManager)
        self.pb_viewGrid.setMaximumSize(QSize(26, 21))
        self.pb_viewGrid.setText("")
        self.pb_viewGrid.setObjectName("pb_viewGrid")
        self.horizontalLayout.addWidget(self.pb_viewGrid)
        self.pb_viewLine = QPushButton(FileManager)
        self.pb_viewLine.setMaximumSize(QSize(26, 21))
        self.pb_viewLine.setText("")
        self.pb_viewLine.setObjectName("pb_viewLine")
        self.horizontalLayout.addWidget(self.pb_viewLine)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_left = QFrame(FileManager)
        self.frame_left.setStyleSheet("QFrame{\n"
"background:rgb(50, 50, 50);\n"
"}")
        self.frame_left.setFrameShape(QFrame.Box)
        self.frame_left.setFrameShadow(QFrame.Raised)
        self.frame_left.setObjectName("frame_left")
        self.gridLayout = QGridLayout(self.frame_left)
        self.gridLayout.setObjectName("gridLayout")
        self.label_sequence = QLabel(self.frame_left)
        font = QFont()
        font.setPointSize(9)
        self.label_sequence.setFont(font)
        self.label_sequence.setObjectName("label_sequence")
        self.gridLayout.addWidget(self.label_sequence, 1, 0, 1, 1)
        self.label_project = QLabel(self.frame_left)
        font = QFont()
        font.setPointSize(9)
        self.label_project.setFont(font)
        self.label_project.setObjectName("label_project")
        self.gridLayout.addWidget(self.label_project, 0, 0, 1, 1)
        self.cbox_project = QComboBox(self.frame_left)
        self.cbox_project.setMinimumSize(QSize(150, 0))
        self.cbox_project.setObjectName("cbox_project")
        self.gridLayout.addWidget(self.cbox_project, 0, 1, 1, 1)
        self.cbox_sequence = QComboBox(self.frame_left)
        self.cbox_sequence.setEnabled(True)
        self.cbox_sequence.setMinimumSize(QSize(100, 0))
        self.cbox_sequence.setObjectName("cbox_sequence")
        self.gridLayout.addWidget(self.cbox_sequence, 1, 1, 1, 1)
        self.label_type = QLabel(self.frame_left)
        font = QFont()
        font.setPointSize(9)
        self.label_type.setFont(font)
        self.label_type.setObjectName("label_type")
        self.gridLayout.addWidget(self.label_type, 2, 0, 1, 1)
        self.cbox_type = QComboBox(self.frame_left)
        self.cbox_type.setMinimumSize(QSize(100, 0))
        self.cbox_type.setObjectName("cbox_type")
        self.cbox_type.addItem("")
        self.cbox_type.addItem("")
        self.cbox_type.addItem("")
        self.cbox_type.addItem("")
        self.gridLayout.addWidget(self.cbox_type, 2, 1, 1, 1)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 6, 1, 1, 1)
        self.pb_byname = QPushButton(self.frame_left)
        self.pb_byname.setObjectName("pb_byname")
        self.gridLayout.addWidget(self.pb_byname, 4, 1, 1, 1)
        self.pb_bydate = QPushButton(self.frame_left)
        self.pb_bydate.setObjectName("pb_bydate")
        self.gridLayout.addWidget(self.pb_bydate, 3, 1, 1, 1)
        self.pb_reverse = QPushButton(self.frame_left)
        self.pb_reverse.setObjectName("pb_reverse")
        self.gridLayout.addWidget(self.pb_reverse, 5, 1, 1, 1)
        self.horizontalLayout_3.addWidget(self.frame_left)
        self.listWidget_files = QListWidget(FileManager)
        self.listWidget_files.setFrameShape(QFrame.Box)
        self.listWidget_files.setFrameShadow(QFrame.Raised)
        self.listWidget_files.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.listWidget_files.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.listWidget_files.setMovement(QListView.Static)
        self.listWidget_files.setFlow(QListView.LeftToRight)
        self.listWidget_files.setProperty("isWrapping", True)
        self.listWidget_files.setResizeMode(QListView.Adjust)
        self.listWidget_files.setLayoutMode(QListView.Batched)
        self.listWidget_files.setSpacing(5)
        self.listWidget_files.setViewMode(QListView.ListMode)
        self.listWidget_files.setModelColumn(0)
        self.listWidget_files.setUniformItemSizes(False)
        self.listWidget_files.setWordWrap(False)
        self.listWidget_files.setObjectName("listWidget_files")

        self.horizontalLayout_3.addWidget(self.listWidget_files)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QSpacerItem(245, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.h_slider_zoomView = QSlider(FileManager)
        self.h_slider_zoomView.setMinimumSize(QSize(150, 0))
        self.h_slider_zoomView.setMaximumSize(QSize(150, 16777215))
        self.h_slider_zoomView.setOrientation(Qt.Horizontal)
        self.h_slider_zoomView.setObjectName("h_slider_zoomView")
        self.horizontalLayout_2.addWidget(self.h_slider_zoomView)
        spacerItem4 = QSpacerItem(408, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.frame_bottom = QFrame(FileManager)
        self.frame_bottom.setStyleSheet("QFrame{\n"
"background:rgb(50, 50, 50);\n"
"}")
        self.frame_bottom.setFrameShape(QFrame.Box)
        self.frame_bottom.setFrameShadow(QFrame.Raised)
        self.frame_bottom.setObjectName("frame_bottom")
        self.horizontalLayout_5 = QHBoxLayout(self.frame_bottom)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.pb_pref = QPushButton(self.frame_bottom)
        self.pb_pref.setMinimumSize(QSize(80, 25))
        self.pb_pref.setObjectName("pb_pref")
        self.horizontalLayout_5.addWidget(self.pb_pref)

        self.pb_montage = QPushButton(self.frame_bottom)
        self.pb_montage.setMinimumSize(QSize(80, 25))
        self.pb_montage.setObjectName("pb_montage")
        self.horizontalLayout_5.addWidget(self.pb_montage)

        spacerItem5 = QSpacerItem(460, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.pb_new = QPushButton(self.frame_bottom)
        self.pb_new.setMinimumSize(QSize(70, 25))
        self.pb_new.setObjectName("pb_new")
        self.horizontalLayout_5.addWidget(self.pb_new)
        self.pb_save = QPushButton(self.frame_bottom)
        self.pb_save.setMinimumSize(QSize(70, 25))
        self.pb_save.setObjectName("pb_save")
        self.horizontalLayout_5.addWidget(self.pb_save)
        self.pb_select_shot = QPushButton(self.frame_bottom)
        self.pb_select_shot.setMinimumSize(QSize(100, 25))
        self.pb_select_shot.setObjectName("pb_select_shot")
        self.horizontalLayout_5.addWidget(self.pb_select_shot)
        spacerItem6 = QSpacerItem(30, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.pb_open = QPushButton(self.frame_bottom)
        self.pb_open.setMinimumSize(QSize(60, 25))
        self.pb_open.setObjectName("pb_open")
        self.horizontalLayout_5.addWidget(self.pb_open)
        self.pb_close = QPushButton(self.frame_bottom)
        self.pb_close.setMinimumSize(QSize(60, 25))
        self.pb_close.setObjectName("pb_close")
        self.horizontalLayout_5.addWidget(self.pb_close)
        self.verticalLayout_2.addWidget(self.frame_bottom)

        self.retranslateUi(FileManager)
        QMetaObject.connectSlotsByName(FileManager)

    def retranslateUi(self, FileManager):
        FileManager.setWindowTitle("File Manager")
        self.lb_top.setText("Loader")
        self.lb_path.setText("/Storage/Project/")
        self.label_sequence.setText("Sequence:")
        self.label_project.setText("Project:")
        self.label_type.setText("Type:")
        self.cbox_type.setItemText(0, "FX")
        self.cbox_type.setItemText(1, "LIGHTING")
        self.cbox_type.setItemText(2, "ANIMATION")
        self.cbox_type.setItemText(3, "MODELING")
        self.pb_byname.setText("Name")
        self.pb_bydate.setText("Date")
        self.pb_reverse.setText("Invert ")
        __sortingEnabled = self.listWidget_files.isSortingEnabled()
        self.listWidget_files.setSortingEnabled(False)

        self.listWidget_files.setSortingEnabled(__sortingEnabled)
        self.pb_pref.setText("Preferences")
        self.pb_montage.setText("Montage")
        self.pb_new.setText("New")
        self.pb_save.setText("Save")
        self.pb_select_shot.setText("Select Shot")
        self.pb_open.setText("Open")
        self.pb_close.setText("Close")


