#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import sys

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    import hou
except:
    from PySide.QtGui import *
    from PySide.QtCore import *


from item import FileItem

class CBOX(QListWidget):



    def __init__(self, parent=None):
        super(CBOX, self).__init__(parent)
        items = ["WIP", "COMMENTED", "HOLD", "NONE", "DONE"]
        self.setEditable(True)
        self.editItem()






if __name__ == '__main__':

    app = QApplication([])
    w=CBOX()
    w.show()
    sys.exit(app.exec_())