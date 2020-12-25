# -*- coding: utf-8 -*-

# Form implementation generated from reading uis222 file 'X:\app\win\Pipeline\uis222\shotsOpener_01.uis222'
#
# Created: Fri Oct 26 14:37:17 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(548, 309)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.projectFrame = QtGui.QGroupBox(Form)
        self.projectFrame.setObjectName("projectFrame")
        self.verticalLayout = QtGui.QVBoxLayout(self.projectFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.seqFrame1 = QtGui.QGroupBox(self.projectFrame)
        self.seqFrame1.setObjectName("seqFrame1")
        self.horizontalLayout = QtGui.QHBoxLayout(self.seqFrame1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtGui.QPushButton(self.seqFrame1)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_3 = QtGui.QPushButton(self.seqFrame1)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtGui.QPushButton(self.seqFrame1)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.verticalLayout.addWidget(self.seqFrame1)
        self.seqFrame2 = QtGui.QGroupBox(self.projectFrame)
        self.seqFrame2.setObjectName("seqFrame2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.seqFrame2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_5 = QtGui.QPushButton(self.seqFrame2)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_6 = QtGui.QPushButton(self.seqFrame2)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        self.pushButton_7 = QtGui.QPushButton(self.seqFrame2)
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_2.addWidget(self.pushButton_7)
        self.verticalLayout.addWidget(self.seqFrame2)
        self.gridLayout.addWidget(self.projectFrame, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.projectFrame.setTitle(QtGui.QApplication.translate("Form", "projecFrame", None, QtGui.QApplication.UnicodeUTF8))
        self.seqFrame1.setTitle(QtGui.QApplication.translate("Form", "SqF", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("Form", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("Form", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.seqFrame2.setTitle(QtGui.QApplication.translate("Form", "SqF2", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("Form", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_6.setText(QtGui.QApplication.translate("Form", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_7.setText(QtGui.QApplication.translate("Form", "PushButton", None, QtGui.QApplication.UnicodeUTF8))

