# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'X:\app\win\Pipeline\houdini_app\AssetsUpdater\updaterUi.ui'
#
# Created: Fri Jan 10 17:01:12 2020
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

class Ui_UpdateAssets(object):
    def setupUi(self, UpdateAssets):
        UpdateAssets.setObjectName("UpdateAssets")
        UpdateAssets.resize(455, 581)
        self.verticalLayout = QVBoxLayout(UpdateAssets)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QSplitter(UpdateAssets)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.listWidget = QListWidget(self.splitter)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(558, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_close = QPushButton(UpdateAssets)
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.pushButton_update = QPushButton(UpdateAssets)
        self.pushButton_update.setObjectName("pushButton_update")
        self.horizontalLayout.addWidget(self.pushButton_update)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton_close.setMinimumSize(QSize(70, 25))
        self.pushButton_update.setMinimumSize(QSize(70, 25))

        UpdateAssets.setStyleSheet("QDialog{\n"
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

        self.retranslateUi(UpdateAssets)
        QMetaObject.connectSlotsByName(UpdateAssets)

    def retranslateUi(self, UpdateAssets):
        UpdateAssets.setWindowTitle("UpdateAssets")
        self.pushButton_close.setText("Close")
        self.pushButton_update.setText("Update")

