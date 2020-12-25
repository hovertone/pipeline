import sys
#from PyQt4.QtGui  import *
#from PyQt4.QtCore import *
try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    import hou
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os, sys


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):

        self.le_search = QLineEdit()                            # self.   +++

        se_btn    = QPushButton("Search")
        se_btn.clicked.connect(self.find_item)

        self.listwidget = QListWidget()
        self.total_list = ["machine", "mac1", "printer", "Printer","xerox bundles", "2mac"]
        self.listwidget.addItems(self.total_list)

        hbox      = QHBoxLayout()
        hbox.addWidget(self.le_search)                          # self.   +++
        hbox.addWidget(se_btn)

        auto_search_vbox = QVBoxLayout(self)
        auto_search_vbox.addLayout(hbox)
        auto_search_vbox.addWidget(self.listwidget)

    def find_item(self):
#        out = self.listwidget.findItems("mac", QtCore.Qt.MatchExactly)          # ---
#        out = self.listwidget.findItems(self.le_search.text(), Qt.MatchExactly)
        out = self.listwidget.findItems(self.le_search.text(),
                                        Qt.MatchContains |          # +++
                                        Qt.MatchCaseSensitive)      # +++

        print("out->", [ i.text() for i in out ] )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

    self.listWidget_lib.itemWidget(self.listWidget_lib.item(i)).path),

    def search_action(self):
        out = self.listWidget_lib.findItems(self.le_search.text(),
                                        Qt.MatchContains |
                                        Qt.MatchCaseSensitive)

        #print("out->", [i.text() for i in out])
        for i in out:
            if self.listWidget_lib.itemWidget()

