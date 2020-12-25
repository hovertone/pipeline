# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'X:\app\win\Pipeline\houdini_app\Loader\add_shot.ui'
#
# Created: Fri Jan 17 12:58:47 2020
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

class AddShot(QDialog):
    def __init__(self, parent=None):
        super(AddShot, self).__init__(parent)
        self.resize(222, 90)
        self.formLayout = QFormLayout(self)
        self.label_shot = QLabel(self)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_shot)
        self.lineEdit_shot = QLineEdit(self)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_shot)
        self.label_ff = QLabel(self)
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_ff)
        self.lineEdit_ff = QLineEdit(self)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_ff)
        self.label_lf = QLabel(self)
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_lf)
        self.lineEdit_lf = QLineEdit(self)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_lf)
        self.pushButton = QPushButton(self)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.pushButton)
        self.pushButton.setMinimumSize(70, 25)

        self.lineEdit_shot.setValidator(QIntValidator())
        self.lineEdit_ff.setValidator(QIntValidator())
        self.lineEdit_lf.setValidator(QIntValidator())

        self.setWindowTitle("Add Shot")
        self.label_shot.setText("SHOT:")
        self.label_ff.setText("FIRST FRAME:")
        self.label_lf.setText("LAST FRAME:")
        self.pushButton.setText("ADD SHOT")
        self.lineEdit_shot.setText("000")
        self.lineEdit_ff.setText("1001")
        self.lineEdit_lf.setText("1050")

        self.setStyleSheet("QDialog{\n"
                                  "background:rgb(58,58,58);\n"
                                  "}\n"
                                  "\n"
                                  "QLabel{\n"
                                  "color:rgb(196,196,196);\n"
                                  "}\n"
                                  "\n"
                                  "QLineEdit{\n"
                                  "background:rgb(48,48,48);\n"
                                  "color:rgb(196,196,196);\n"
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
                                  "")


if __name__ == '__main__':

    app = QApplication([])
    w=AddShot()
    w.show()
    sys.exit(app.exec_())
