#!/usr/bin/python

"""
ZetCode PySide tutorial

This program creates a statusbar.

author: Jan Bodnar
website: zetcode.com
"""

import sys
try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

except:
    from PySide.QtGui import *
    from PySide.QtCore import *


class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        #self.statusBar().showMessage("<html><b>Hello</b</html>")
        self.layout = QVBoxLayout()
        self.mainLayout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        item = QListWidgetItem()
        #item.setCheckState(Qt.Checked)
        #item.setText( '<b>' + 'test' + '</b>' )
        #item.setData(QFont("myFontFamily",italic=True), Qt.FontRole)
        item.setBackground( QColor('#7fc97f'))
        self.list_widget.addItem(item)

        self.layout.addWidget(self.list_widget)

        self.mainLayout.addLayout(self.layout)

        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()