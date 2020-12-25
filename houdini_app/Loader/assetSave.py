# -*- coding: utf-8 -*-


try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os, sys

from assetName_v001_UIs import Ui_AssetName


class AssetSaveUI (QDialog, Ui_AssetName):

    pressEnter = Signal()

    def __init__(self, parent=None):
        super(AssetSaveUI, self).__init__(parent)
        self.setupUi(self)

        self.pb_cancel.clicked.connect(self.close)



    def keyPressEvent(self, event):
        if event.key() == 16777220:


            self.pressEnter.emit()
        else:
            pass



if __name__ == '__main__':

    app = QApplication([])
    w=AssetSaveUI()
    w.show()
    sys.exit(app.exec_())




