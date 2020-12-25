# -*- coding: utf-8 -*-

# Form implementation generated from reading uis222 file 'D:\dev\Pipeline\uis222\lightGroupManager.uis222'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!



#####  from PySide import QtCore, QtGui #############


try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *



class Ui_LightGroupManager(object):
    def setupUi(self, LightGroupManager):
        LightGroupManager.setObjectName("LightGroupManager")
        LightGroupManager.resize(685, 554)
        self.verticalLayout_4 = QVBoxLayout(LightGroupManager)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lb_lights = QLabel(LightGroupManager)
        self.lb_lights.setMaximumSize(QSize(311, 16))
        self.lb_lights.setObjectName("lb_lights")
        self.verticalLayout_3.addWidget(self.lb_lights)
        self.lw_lights = QListWidget(LightGroupManager)
        self.lw_lights.setObjectName("lw_lights")
        self.verticalLayout_3.addWidget(self.lw_lights)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pb_insert_aov = QPushButton(LightGroupManager)
        self.pb_insert_aov.setMaximumSize(QSize(31, 23))
        self.pb_insert_aov.setObjectName("pb_insert_aov")
        self.verticalLayout.addWidget(self.pb_insert_aov)
        self.pb_remove_aov = QPushButton(LightGroupManager)
        self.pb_remove_aov.setMaximumSize(QSize(31, 23))
        self.pb_remove_aov.setObjectName("pb_remove_aov")
        self.verticalLayout.addWidget(self.pb_remove_aov)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lb_aovs = QLabel(LightGroupManager)
        self.lb_aovs.setMaximumSize(QSize(311, 20))
        self.lb_aovs.setObjectName("lb_aovs")
        self.verticalLayout_2.addWidget(self.lb_aovs)
        self.lw_aovs = QListWidget(LightGroupManager)
        self.lw_aovs.setObjectName("lw_aovs")
        self.verticalLayout_2.addWidget(self.lw_aovs)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QSpacerItem(388, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pb_refresh = QPushButton(LightGroupManager)
        self.pb_refresh.setObjectName("pb_refresh")
        self.horizontalLayout_2.addWidget(self.pb_refresh)
        self.pb_apply = QPushButton(LightGroupManager)
        self.pb_apply.setObjectName("pb_apply")
        self.horizontalLayout_2.addWidget(self.pb_apply)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.retranslateUi(LightGroupManager)
        QMetaObject.connectSlotsByName(LightGroupManager)

    def retranslateUi(self, LightGroupManager):
        LightGroupManager.setWindowTitle("Light Group Manager")
        self.lb_lights.setText("Lights")
        self.pb_insert_aov.setText(">>")
        self.pb_remove_aov.setText("<<")
        self.lb_aovs.setText("AOVs")
        self.pb_refresh.setText("Refresh")
        self.pb_apply.setText("Apply")

