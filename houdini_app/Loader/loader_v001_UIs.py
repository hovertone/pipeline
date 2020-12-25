# -*- coding: utf-8 -*-

# Form implementation generated from reading uis222 file 'D:\dev\Loader\loader_v001.uis222'
#
# Created: Tue Oct 23 13:30:57 2018
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

class Ui_FileManager(object):
    def setupUi(self, FileManager):
        FileManager.setObjectName("FileManager")
        FileManager.setEnabled(True)
        FileManager.resize(831, 789)
        FileManager.setStyleSheet("QDialog{\n"
"background:rgb(58,58,58);\n"
"}\n"
"QLabel{\n"
"color:rgb(196,196,196);\n"
"}\n"
"QListWidget{\n"
"background:rgb(48,48,48);\n"
"}\n"
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
"QPushButton:pressed{\n"
"background:rgb(185,134,32);\n"
"border:1px solid black;\n"
"color:rgb(196,196,196);\n"
"}\n"
"QPushButton:disabled{\n"
"background:rgb(70,70,70);\n"
"border:1px solid gray;\n"
"color:rgb(100,100,100);\n"
"}\n"
"")
        self.vLayoutMain = QVBoxLayout(FileManager)
        self.vLayoutMain.setSpacing(6)
        self.vLayoutMain.setObjectName("vLayoutMain")
        self.gridLayoutTop = QGridLayout()
        self.gridLayoutTop.setObjectName("gridLayoutTop")
        self.label_project = QLabel(FileManager)
        font = QFont()
        font.setPointSize(9)
        self.label_project.setFont(font)
        self.label_project.setObjectName("label_project")
        self.gridLayoutTop.addWidget(self.label_project, 0, 0, 1, 1)
        self.label_sequence = QLabel(FileManager)
        self.label_sequence.setFont(font)
        self.label_sequence.setObjectName("label_sequence")
        self.gridLayoutTop.addWidget(self.label_sequence, 0, 1, 1, 1)
        self.label_shot = QLabel(FileManager)
        self.label_shot.setFont(font)
        self.label_shot.setObjectName("label_shot")
        self.gridLayoutTop.addWidget(self.label_shot, 0, 2, 1, 1)
        self.label_type = QLabel(FileManager)
        self.label_type.setFont(font)
        self.label_type.setObjectName("label_type")
        self.gridLayoutTop.addWidget(self.label_type, 0, 3, 1, 1)
        self.cbox_project = QComboBox(FileManager)
        self.cbox_project.setObjectName("cbox_project")
        self.gridLayoutTop.addWidget(self.cbox_project, 1, 0, 1, 1)
        self.cbox_sequence = QComboBox(FileManager)
        self.cbox_sequence.setEnabled(True)
        self.cbox_sequence.setObjectName("cbox_sequence")
        self.gridLayoutTop.addWidget(self.cbox_sequence, 1, 1, 1, 1)
        self.cbox_shot = QComboBox(FileManager)
        self.cbox_shot.setEnabled(True)
        self.cbox_shot.setObjectName("cbox_shot")
        self.gridLayoutTop.addWidget(self.cbox_shot, 1, 2, 1, 1)
        self.cbox_type = QComboBox(FileManager)
        self.cbox_type.setObjectName("cbox_type")
        self.cbox_type.addItem("")
        self.cbox_type.addItem("")
        self.cbox_type.addItem("")
        self.cbox_type.addItem("")
        self.gridLayoutTop.addWidget(self.cbox_type, 1, 3, 1, 1)
        self.vLayoutMain.addLayout(self.gridLayoutTop)
        ###
        self.hLayoutSorting = QHBoxLayout()
        self.hLayoutSorting.setSpacing(0)
        self.hLayoutSorting.setObjectName("hLayoutSorting")
        self.pb_byname = QPushButton(FileManager)
        self.pb_byname.setMinimumSize(QSize(0, 20))
        self.pb_byname.setObjectName("pb_byname")
        self.hLayoutSorting.addWidget(self.pb_byname)
        self.pb_bydate = QPushButton(FileManager)
        self.pb_bydate.setMinimumSize(QSize(0, 20))
        self.pb_bydate.setObjectName("pb_bydate")
        self.hLayoutSorting.addWidget(self.pb_bydate)
        self.pb_reverse = QPushButton(FileManager)
        self.pb_reverse.setMinimumSize(QSize(0, 20))
        self.pb_reverse.setObjectName("pb_reverse")
        self.hLayoutSorting.addWidget(self.pb_reverse)
        self.vLayoutMain.addLayout(self.hLayoutSorting)
        ###
        self.listWidget_files = QListWidget(FileManager)
        self.listWidget_files.setObjectName("listWidget_files")
        self.vLayoutMain.addWidget(self.listWidget_files)
        self.hLayoutButtons = QHBoxLayout()
        self.hLayoutButtons.setSpacing(6)
        self.hLayoutButtons.setObjectName("hLayoutButtons")

        self.pb_pref = QPushButton(FileManager)
        self.pb_pref.setMinimumSize(QSize(100, 25))
        self.pb_pref.setObjectName("pb_pref")
        self.hLayoutButtons.addWidget(self.pb_pref)

        spacerItem = QSpacerItem(618, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayoutButtons.addItem(spacerItem)

        self.pb_open = QPushButton(FileManager)
        self.pb_open.setMinimumSize(QSize(70, 25))
        self.pb_open.setObjectName("pb_open")
        self.hLayoutButtons.addWidget(self.pb_open)

        self.pb_save = QPushButton(FileManager)
        self.pb_save.setMinimumSize(QSize(70, 25))
        self.pb_save.setObjectName("pb_save")
        self.hLayoutButtons.addWidget(self.pb_save)

        self.pb_new = QPushButton(FileManager)
        self.pb_new.setMinimumSize(QSize(70, 25))
        self.pb_new.setObjectName("pb_new")
        self.hLayoutButtons.addWidget(self.pb_new)

        self.pb_select_shot = QPushButton(FileManager)
        self.pb_select_shot.setMinimumSize(QSize(100, 25))
        self.pb_select_shot.setObjectName("pb_select_shot")
        self.hLayoutButtons.addWidget(self.pb_select_shot)

        self.pb_close = QPushButton(FileManager)
        self.pb_close.setMinimumSize(QSize(70, 25))
        self.pb_close.setObjectName("pb_close")
        self.hLayoutButtons.addWidget(self.pb_close)



        self.vLayoutMain.addLayout(self.hLayoutButtons)


        self.listWidget_files.setStyleSheet("QListWidget:item{\n"
"color:rgb(196,196,196);\n"
"}\n"
"QListWidget{\n"
"alternate-background-color:rgb(30,30,30);\n"
"}\n")
        self.retranslateUi(FileManager)
        QMetaObject.connectSlotsByName(FileManager)

    def retranslateUi(self, FileManager):
        FileManager.setWindowTitle("File Manager")
        self.label_project.setText("Project:")
        self.label_sequence.setText("Sequence:")
        self.label_shot.setText("Shot:")
        self.label_type.setText("Type:")

        self.cbox_type.setItemText(0, "FX")
        self.cbox_type.setItemText(1,"LIGHT")
        self.cbox_type.setItemText(2,"ANIMATION")
        self.cbox_type.setItemText(3, "MODEL")
        self.pb_pref.setText("Preferences")
        self.pb_byname.setText("By Name")
        self.pb_bydate.setText("By Date")
        self.pb_reverse.setText("Reverse")
        self.pb_close.setText("Close")
        self.pb_open.setText("Open")
        self.pb_save.setText("Save")
        self.pb_new.setText("New")
        self.pb_select_shot.setText("Select Shot")

