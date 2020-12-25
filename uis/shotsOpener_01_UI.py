# -*- coding: utf-8 -*-

# Form implementation generated from reading uis222 file 'X:\app\win\Pipeline\uis222\shotsOpener_01.uis222'
#
# Created: Fri Oct 26 14:37:17 2018
#      by: PyQt4 UI code generator 4.11
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(548, 309)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.projectFrame = QtGui.QGroupBox(Form)
        self.projectFrame.setObjectName(_fromUtf8("projectFrame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.projectFrame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.seqFrame1 = QtGui.QGroupBox(self.projectFrame)
        self.seqFrame1.setObjectName(_fromUtf8("seqFrame1"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.seqFrame1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(self.seqFrame1)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_3 = QtGui.QPushButton(self.seqFrame1)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtGui.QPushButton(self.seqFrame1)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.verticalLayout.addWidget(self.seqFrame1)
        self.seqFrame2 = QtGui.QGroupBox(self.projectFrame)
        self.seqFrame2.setObjectName(_fromUtf8("seqFrame2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.seqFrame2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_5 = QtGui.QPushButton(self.seqFrame2)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_6 = QtGui.QPushButton(self.seqFrame2)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        self.pushButton_7 = QtGui.QPushButton(self.seqFrame2)
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.horizontalLayout_2.addWidget(self.pushButton_7)
        self.verticalLayout.addWidget(self.seqFrame2)
        self.gridLayout.addWidget(self.projectFrame, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.projectFrame.setTitle(_translate("Form", "projecFrame", None))
        self.seqFrame1.setTitle(_translate("Form", "SqF", None))
        self.pushButton.setText(_translate("Form", "PushButton", None))
        self.pushButton_3.setText(_translate("Form", "PushButton", None))
        self.pushButton_4.setText(_translate("Form", "PushButton", None))
        self.seqFrame2.setTitle(_translate("Form", "SqF2", None))
        self.pushButton_5.setText(_translate("Form", "PushButton", None))
        self.pushButton_6.setText(_translate("Form", "PushButton", None))
        self.pushButton_7.setText(_translate("Form", "PushButton", None))

