# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\dev\Pipeline\uis222\projectCreateUI_v002.ui'
#
# Created: Mon Nov 05 15:50:18 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ProjectCreate(object):
    def setupUi(self, ProjectCreate):
        ProjectCreate.setObjectName("ProjectCreate")
        ProjectCreate.resize(832, 598)
        ProjectCreate.setStyleSheet("QWidget{\n"
"background:rgb(58,58,58);\n"
"}\n"
"\n"
"QLabel{\n"
"color:rgb(196,196,196);\n"
"}\n"
"\n"
"QListWidget{\n"
"background:rgb(48,48,48);\n"
"outline: 0;\n"
"}\n"
"\n"
"\n"
"QListWidget::item{\n"
"    border:1px solid #555555;\n"
"    background:rgb(52,52,52);\n"
"    color:rgb(196,196,196);\n"
"    alternate-background-color: #222222;}\n"
"\n"
"QListWidget::item:hover{\n"
"    background: rgb(60,70,80);\n"
"    border:1px solid lightblue;}\n"
"\n"
"QListWidget::item:alternate:hover{\n"
"    background: rgb(70,80,90);\n"
"    border:1px solid lightblue;}\n"
"\n"
"QListWidget::item:alternate {\n"
"    background:rgb(48,48,48);}\n"
"\n"
"QListWidget::item:selected{\n"
"    background: rgb(40,70,100);\n"
"    border:1px solid lightblue;}\n"
"\n"
"QListWidget::item:selected:!active{\n"
"    background: rgb(40,60,90);}\n"
"\n"
"\n"
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
"QPushButton:disabled{\n"
"background:rgb(90,90,90);\n"
"border:1px solid black;\n"
"color:rgb(150,150,150);\n"
"}\n"
"\n"
"QLineEdit{\n"
"background:rgb(48,48,48);\n"
"color:rgb(196,196,196);\n"
"border:1px solid gray;\n"
"}\n"
"\n"
"\n"
"")
        self.vLayoutMain = QtGui.QVBoxLayout(ProjectCreate)
        self.vLayoutMain.setObjectName("vLayoutMain")
        self.hLayoutTop = QtGui.QHBoxLayout()
        self.hLayoutTop.setObjectName("hLayoutTop")
        self.le_root = QtGui.QLineEdit(ProjectCreate)
        self.le_root.setObjectName("le_root")
        self.hLayoutTop.addWidget(self.le_root)
        self.le_projectName = QtGui.QLineEdit(ProjectCreate)
        self.le_projectName.setObjectName("le_projectName")
        self.hLayoutTop.addWidget(self.le_projectName)
        self.vLayoutMain.addLayout(self.hLayoutTop)
        self.hLayoutCenter = QtGui.QHBoxLayout()
        self.hLayoutCenter.setObjectName("hLayoutCenter")
        self.vLayoutSq = QtGui.QVBoxLayout()
        self.vLayoutSq.setObjectName("vLayoutSq")
        self.hLayoutSqTop = QtGui.QHBoxLayout()
        self.hLayoutSqTop.setObjectName("hLayoutSqTop")
        self.lb_Sq = QtGui.QLabel(ProjectCreate)
        self.lb_Sq.setMinimumSize(QtCore.QSize(56, 23))
        self.lb_Sq.setObjectName("lb_Sq")
        self.hLayoutSqTop.addWidget(self.lb_Sq)
        self.pb_Sq_add = QtGui.QPushButton(ProjectCreate)
        self.pb_Sq_add.setEnabled(True)
        self.pb_Sq_add.setMinimumSize(QtCore.QSize(55, 25))
        self.pb_Sq_add.setObjectName("pb_Sq_add")
        self.hLayoutSqTop.addWidget(self.pb_Sq_add)
        self.pb_sq_remove = QtGui.QPushButton(ProjectCreate)
        self.pb_sq_remove.setMinimumSize(QtCore.QSize(55, 25))
        self.pb_sq_remove.setObjectName("pb_sq_remove")
        self.hLayoutSqTop.addWidget(self.pb_sq_remove)
        self.pb_sq_clear = QtGui.QPushButton(ProjectCreate)
        self.pb_sq_clear.setMinimumSize(QtCore.QSize(55, 25))
        self.pb_sq_clear.setObjectName("pb_sq_clear")
        self.hLayoutSqTop.addWidget(self.pb_sq_clear)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayoutSqTop.addItem(spacerItem)
        self.vLayoutSq.addLayout(self.hLayoutSqTop)
        self.listWidgetSq = QtGui.QListWidget(ProjectCreate)
        self.listWidgetSq.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed)
        self.listWidgetSq.setAlternatingRowColors(True)
        self.listWidgetSq.setObjectName("listWidgetSq")
        self.vLayoutSq.addWidget(self.listWidgetSq)
        self.hLayoutCenter.addLayout(self.vLayoutSq)
        self.vLayoutShots = QtGui.QVBoxLayout()
        self.vLayoutShots.setObjectName("vLayoutShots")
        self.hLayoutShotsTop = QtGui.QHBoxLayout()
        self.hLayoutShotsTop.setObjectName("hLayoutShotsTop")
        self.lb_Shots = QtGui.QLabel(ProjectCreate)
        self.lb_Shots.setMinimumSize(QtCore.QSize(40, 23))
        self.lb_Shots.setObjectName("lb_Shots")
        self.hLayoutShotsTop.addWidget(self.lb_Shots)
        self.pb_Shots_add = QtGui.QPushButton(ProjectCreate)
        self.pb_Shots_add.setMinimumSize(QtCore.QSize(50, 25))
        self.pb_Shots_add.setObjectName("pb_Shots_add")
        self.hLayoutShotsTop.addWidget(self.pb_Shots_add)
        self.pb_Shots_remove = QtGui.QPushButton(ProjectCreate)
        self.pb_Shots_remove.setMinimumSize(QtCore.QSize(55, 25))
        self.pb_Shots_remove.setObjectName("pb_Shots_remove")
        self.hLayoutShotsTop.addWidget(self.pb_Shots_remove)
        self.pb_Shots_clear = QtGui.QPushButton(ProjectCreate)
        self.pb_Shots_clear.setMinimumSize(QtCore.QSize(50, 25))
        self.pb_Shots_clear.setObjectName("pb_Shots_clear")
        self.hLayoutShotsTop.addWidget(self.pb_Shots_clear)
        self.lb_Step = QtGui.QLabel(ProjectCreate)
        self.lb_Step.setObjectName("lb_Step")
        self.hLayoutShotsTop.addWidget(self.lb_Step)
        self.le_Step = QtGui.QLineEdit(ProjectCreate)
        self.le_Step.setObjectName("le_Step")
        self.hLayoutShotsTop.addWidget(self.le_Step)
        self.vLayoutShots.addLayout(self.hLayoutShotsTop)
        self.listWidgetShots = QtGui.QListWidget(ProjectCreate)
        self.listWidgetShots.setObjectName("listWidgetShots")
        self.vLayoutShots.addWidget(self.listWidgetShots)
        self.hLayoutCenter.addLayout(self.vLayoutShots)
        self.vLayoutMain.addLayout(self.hLayoutCenter)
        self.hLayoutBottom = QtGui.QHBoxLayout()
        self.hLayoutBottom.setObjectName("hLayoutBottom")
        spacerItem1 = QtGui.QSpacerItem(88, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayoutBottom.addItem(spacerItem1)
        self.pb_create = QtGui.QPushButton(ProjectCreate)
        self.pb_create.setMinimumSize(QtCore.QSize(55, 25))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.pb_create.setFont(font)
        self.pb_create.setObjectName("pb_create")
        self.hLayoutBottom.addWidget(self.pb_create)
        self.pb_cancel = QtGui.QPushButton(ProjectCreate)
        self.pb_cancel.setMinimumSize(QtCore.QSize(55, 25))
        self.pb_cancel.setObjectName("pb_cancel")
        self.hLayoutBottom.addWidget(self.pb_cancel)
        self.vLayoutMain.addLayout(self.hLayoutBottom)

        self.retranslateUi(ProjectCreate)
        QtCore.QMetaObject.connectSlotsByName(ProjectCreate)
        ProjectCreate.setTabOrder(self.le_root, self.listWidgetShots)
        ProjectCreate.setTabOrder(self.listWidgetShots, self.listWidgetSq)
        ProjectCreate.setTabOrder(self.listWidgetSq, self.le_projectName)

    def retranslateUi(self, ProjectCreate):
        ProjectCreate.setWindowTitle(QtGui.QApplication.translate("ProjectCreate", "ProjectCreate", None, QtGui.QApplication.UnicodeUTF8))
        self.le_root.setText(QtGui.QApplication.translate("ProjectCreate", "P:", None, QtGui.QApplication.UnicodeUTF8))
        self.le_root.setPlaceholderText(QtGui.QApplication.translate("ProjectCreate", "Root path:", None, QtGui.QApplication.UnicodeUTF8))
        self.le_projectName.setPlaceholderText(QtGui.QApplication.translate("ProjectCreate", "Project name:", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_Sq.setText(QtGui.QApplication.translate("ProjectCreate", "Sequences:", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_Sq_add.setText(QtGui.QApplication.translate("ProjectCreate", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_sq_remove.setText(QtGui.QApplication.translate("ProjectCreate", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_sq_clear.setText(QtGui.QApplication.translate("ProjectCreate", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_Shots.setText(QtGui.QApplication.translate("ProjectCreate", "Shots:", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_Shots_add.setText(QtGui.QApplication.translate("ProjectCreate", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_Shots_remove.setText(QtGui.QApplication.translate("ProjectCreate", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_Shots_clear.setText(QtGui.QApplication.translate("ProjectCreate", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_Step.setText(QtGui.QApplication.translate("ProjectCreate", "Sot Step", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_create.setText(QtGui.QApplication.translate("ProjectCreate", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_cancel.setText(QtGui.QApplication.translate("ProjectCreate", "Quit", None, QtGui.QApplication.UnicodeUTF8))

