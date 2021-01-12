# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\my\git\pipeline\nuke\uis\progress_bar_v001.ui'
#
# Created: Tue Jan 12 14:26:15 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(263, 78)
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(20, 40, 241, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.status_label = QtGui.QLabel(Form)
        self.status_label.setGeometry(QtCore.QRect(20, 9, 211, 31))
        self.status_label.setObjectName("status_label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Progress", None, QtGui.QApplication.UnicodeUTF8))
        self.status_label.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

