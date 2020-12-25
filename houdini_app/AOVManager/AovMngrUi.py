# -*- coding: utf-8 -*-



try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *
import sys


class AovManagerUI(QDialog):
    def __init__(self, parent=None):
        super(AovManagerUI, self).__init__(parent)

        #LISTS
        self.comboboxL = QComboBox()
        self.comboboxL.addItem("TESTL")
        self.comboboxR = QComboBox()
        self.comboboxR.addItem("TESTR")
        self.listWidgetL = QListWidget()
        self.listWidgetR = QListWidget()

        # BUTTONS
        self.pb_apply = QPushButton()
        self.pb_apply.setText("Apply")
        self.pb_cancel = QPushButton()
        self.pb_cancel.setText("Cancel")

        # LAYOUT
        self.layout = QVBoxLayout(self)
        self.hLayout = QHBoxLayout()
        self.layout.addWidget(self.comboboxL)
        self.layout.addWidget(self.comboboxR)
        self.layout.addWidget(self.pb_apply)















if __name__ == '__main__':

    app = QApplication([])
    w=AovManagerUI()
    w.show()
    sys.exit(app.exec_())
