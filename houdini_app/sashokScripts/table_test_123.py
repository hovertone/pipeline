


try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

except:
    from PySide.QtGui import *
    from PySide.QtCore import *


import sys

class myWindow(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)

        print 'heehehe'
        self.layout = QHBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        #self.setCentralWidget(self.table)
        data1 = ['row1','row2','row3','row4']
        data2 = ['1','2.0','3.00000001','3.9999999']

        self.table.setRowCount(4)

        for row in range(4):
            item1 = QTableWidgetItem(data1[row])
            if row % 2 == 0:
                item1.setBackground(QColor(255, 128, 128))
            self.table.setItem(row,0,item1)

        self.table.item(1,0).setBackground(QColor(125,125,125))
        #self.setAutoFillBackground(False)
        #self.table.setStyleSheet('''background: rgb(22,33,44);''')
        item = self.table.item(3, 0)
        item.setBackground(QBrush(QColor(144, 1, 1)))

if __name__ == '__main__':

    app = QApplication([])
    w=myWindow()
    w.show()
    sys.exit(app.exec_())

def active(app):
    if app.objectName() == "myWindow":
        app.get_list()
        app.show()
    else:
        w = myWindow(parent=app)
        w.show()


def get_Houdini_Window():
    list = QApplication.allWidgets()
    for item in list:
        if item.objectName() == "myWindow":
            return item
        elif type(item) == QWidget and item.windowIconText():
            return item
    return False


def wait_houdini_window():
    app = get_Houdini_Window()
    return active(app)