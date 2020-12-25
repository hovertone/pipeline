#!/usr/bin/python


try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *
import sys


from loader_v003_UIs import Ui_FileManager



class LoaderHou(QDialog, Ui_FileManager):
    def __init__(self, parent=None):
        super(LoaderHou, self).__init__(parent)
        self.setupUi(self)





if __name__ == '__main__':

    app = QApplication([])
    w=LoaderHou()
    w.show()
    sys.exit(app.exec_())
