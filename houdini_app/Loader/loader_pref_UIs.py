# -*- coding: utf-8 -*-

# Form implementation generated from reading uis222 file 'D:\dev\Pipeline\houdini\Loader\loader_pref_v002.uis222'
#
# Created: Tue Oct 30 17:38:59 2018
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

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        Preferences.setObjectName("Preferences")
        Preferences.resize(409, 128)
        Preferences.setStyleSheet("QWidget{\n"
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
        self.vLayoutMain = QVBoxLayout(Preferences)
        self.vLayoutMain.setObjectName("vLayoutMain")
        self.hLayoutProjects = QHBoxLayout()
        self.hLayoutProjects.setObjectName("hLayoutProjects")
        self.lb_projects = QLabel(Preferences)
        self.lb_projects.setMinimumSize(QSize(90, 0))
        self.lb_projects.setObjectName("lb_projects")
        self.hLayoutProjects.addWidget(self.lb_projects)
        self.le_projects = QLineEdit(Preferences)
        self.le_projects.setObjectName("le_projects")
        self.hLayoutProjects.addWidget(self.le_projects)
        self.vLayoutMain.addLayout(self.hLayoutProjects)
        self.hLayoutCaches = QHBoxLayout()
        self.hLayoutCaches.setObjectName("hLayoutCaches")
        self.lb_caches = QLabel(Preferences)
        self.lb_caches.setMinimumSize(QSize(90, 0))
        self.lb_caches.setObjectName("lb_caches")
        self.hLayoutCaches.addWidget(self.lb_caches)
        self.le_caches = QLineEdit(Preferences)
        self.le_caches.setObjectName("le_caches")
        self.hLayoutCaches.addWidget(self.le_caches)
        self.vLayoutMain.addLayout(self.hLayoutCaches)
        self.hLayoutLib = QHBoxLayout()
        self.hLayoutLib.setObjectName("hLayoutLib")
        self.lb_lib = QLabel(Preferences)
        self.lb_lib.setMinimumSize(QSize(90, 0))
        self.lb_lib.setObjectName("lb_lib")
        self.hLayoutLib.addWidget(self.lb_lib)
        self.le_lib = QLineEdit(Preferences)
        self.le_lib.setObjectName("le_lib")
        self.hLayoutLib.addWidget(self.le_lib)
        self.vLayoutMain.addLayout(self.hLayoutLib)
        self.hLayoutBtns = QHBoxLayout()
        self.hLayoutBtns.setObjectName("hLayoutBtns")

        self.lb_name = QLabel(Preferences)
        self.lb_name.setText("Name: ")
        self.lb_name.setMinimumSize(QSize(90, 0))
        self.le_name = QLineEdit(Preferences)
        self.hLayoutName = QHBoxLayout()
        self.hLayoutName.addWidget(self.lb_name)
        self.hLayoutName.addWidget(self.le_name)
        self.vLayoutMain.addLayout(self.hLayoutName)

        self.lb_key = QLabel(Preferences)
        self.lb_key.setText("User Key: ")
        self.lb_key.setMinimumSize(QSize(90, 0))
        self.le_key = QLineEdit(Preferences)
        self.hLayoutKey = QHBoxLayout()
        self.hLayoutKey.addWidget(self.lb_key)
        self.hLayoutKey.addWidget(self.le_key)
        self.vLayoutMain.addLayout(self.hLayoutKey)

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayoutBtns.addItem(spacerItem)
        self.pb_cancel = QPushButton(Preferences)
        self.pb_cancel.setMinimumSize(QSize(50, 23))
        self.pb_cancel.setObjectName("pb_cancel")
        self.hLayoutBtns.addWidget(self.pb_cancel)
        self.pb_save = QPushButton(Preferences)
        self.pb_save.setMinimumSize(QSize(50, 23))
        self.pb_save.setObjectName("pb_save")
        self.hLayoutBtns.addWidget(self.pb_save)
        self.vLayoutMain.addLayout(self.hLayoutBtns)

        self.retranslateUi(Preferences)
        QMetaObject.connectSlotsByName(Preferences)

    def retranslateUi(self, Preferences):
        Preferences.setWindowTitle("Loader Preferences")
        self.lb_projects.setText("Projects storage:")
        self.lb_caches.setText("Caches storage:")
        self.lb_lib.setText("Lib storage:")
        self.pb_cancel.setText("Cancel")
        self.pb_save.setText("Save")

