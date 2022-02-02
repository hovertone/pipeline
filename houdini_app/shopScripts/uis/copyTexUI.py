
try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import hou
import sys
import os
sys.path.append('%s/uis' % os.environ['shopScriptsPWD'])
import copyTex_ui04_UI
reload(copyTex_ui04_UI)

import copyTex
reload(copyTex)

print('INSIDE COPYTEXUI')


class copyTexUI(QDialog, copyTex_ui04_UI.Ui_Dialog):
    def __init__(self, paths=None, parent=None):
        super(copyTexUI, self).__init__(parent)
        self.setupUi(self)

        self.connect(self.pushButton_cancel, SIGNAL('clicked()'), self.close)
        self.connect(self.pushButton_ok, SIGNAL('clicked()'), self.copyFiles)

        self.inputPaths = paths
        #self.leExistingPath.setText(self.inputPaths[0])

        self.leReplaceThis.textChanged.connect(self.updateLeft)
        self.leWithThis.textChanged.connect(self.updateRight)

        self.table.setItemDelegate(QItemDelegate())

        self.canProceed = False

        self.updateLeft()

    def updateLeft(self):

        if self.leReplaceThis.text() == '':
            # ON WINDOW OPEN
            self.table.setRowCount(len(self.inputPaths))
            for i, e in enumerate(self.inputPaths):
                #print 'PATH', e
                item = QTableWidgetItem(str(e))
                self.table.setItem(i, 0, item)

                # RESIZING COLUMNS AND HIDE HEADERS
                header = self.table.horizontalHeader()
                header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
                header.hide()
                self.table.verticalHeader().hide()

                # RESIZING WINDOW TO CONTAIN ALL TABLE WIDGET
                self.resize((self.table.sizeHintForColumn(0) + 70) * 2, self.height())
        else:
            print('in here')
            pattern = self.leReplaceThis.text()

            rows = self.table.rowCount()
            for i in range(rows):
                item = self.table.item(i, 0)
                if pattern in item.text():
                    item.setBackground(QColor(25, 50, 25))
                else:
                    item.setBackground(QBrush(QColor(44, 44, 44)))

        self.updateRight()

            # if self.leWithThis != '':
            #     print 'WITH THIS IS NOT EMPTY'
            #     self.updateRight()

    def updateRight(self):
        print('IN UPDATE RIGHT')
        replaceThis = self.leReplaceThis.text()
        withThis = self.leWithThis.text()
        rows = self.table.rowCount()

        if withThis == '':
            for i in range(rows):
                itemRight = QTableWidgetItem('No match found.')
                self.table.setItem(i, 1, itemRight)
                self.canProceed = False
        else:
            for i in range(rows):
                itemLeft = self.table.item(i, 0)
                if replaceThis in itemLeft.text():
                    itemRight = self.table.item(i, 1)
                    itemRight.setText(itemLeft.text().replace(replaceThis, withThis))
                    itemRight.setBackground(QColor(25, 50, 25))
                else:
                    itemRight = self.table.item(i, 1)
                    itemRight.setText('No match found.')
                    itemRight.setBackground(QColor(44, 44, 44))

            self.canProceed = False
            for i in range(rows):
                item = self.table.item(i, 1)
                if item.text() != 'No match found.':
                    self.canProceed = True

            header = self.table.horizontalHeader()
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)


    def copyFiles(self):
        if self.canProceed:
            src = self.leReplaceThis.text()
            dest = self.leWithThis.text()
            paths = list()
            for i in range(self.table.rowCount()):
                item = self.table.item(i, 0)
                if item.text() != 'No match found.':
                    paths.append(item.text())

            print('FOLDERS', src)
            print('DEST', dest)
            print('PATHS', str(paths))

            if self.ckbTx.isChecked():
                tx = True
            else:
                tx = False

            if self.ckbNonTx.isChecked():
                nonTx = True
            else:
                nonTx = False

            copyTex.main(src, dest, paths, tx, nonTx)

            self.close()
        else:
            hou.ui.displayMessage('We need to find match to proceed ')

def active(app, paths):
    if app.objectName() == "copyTexUI":
        app.get_list()
        app.show()
    else:
        w = copyTexUI(parent=app,paths=paths)
        w.show()


def get_Houdini_Window():
    list = QApplication.allWidgets()
    for item in list:
        if item.objectName() == "copyTexUI":
            return item
        elif type(item) == QWidget and item.windowIconText():
            return item
    return False


def wait_houdini_window(paths):
    print('IN WAIT HOUDINI WINDOW')
    app = get_Houdini_Window()
    return active(app, paths)

if __name__ == '__main__':

    app = QApplication([])
    w=copyTexUI()
    w.show()
    sys.exit(app.exec_())




