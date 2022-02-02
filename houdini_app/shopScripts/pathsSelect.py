try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os
import sys
import hou

import copyTexUI

class pathsSelect_UI(object):
        def setupUI(self, Dialog):
            Dialog.resize(500, 500)
            Dialog.setWindowTitle('Select paths to work with')
            #self.centralWidget = QWidget(Dialog)
            #self.centralWidget.resize(500, 500)
            self.mainLayout = QVBoxLayout(Dialog)
            self.listLayout = QVBoxLayout()

            self.list_widget = QListWidget()
            self.list_widget.setMinimumSize(QSize(100, 300))
            self.list_widget.setWindowTitle('Paths:')
            self.mainLayout.addWidget(self.list_widget)
            
            # BUTTONS           
            self.buttonsLayout = QHBoxLayout()
            buttonWidth = 100

            self.pushButton_check_all = QPushButton()
            self.pushButton_check_all.setText('Check All')
            self.pushButton_check_all.setMaximumSize(QSize(buttonWidth, 50))
            self.buttonsLayout.addWidget(self.pushButton_check_all)

            self.pushButton_uncheck_all = QPushButton()
            self.pushButton_uncheck_all.setText('Uncheck All')
            self.pushButton_uncheck_all.setMaximumSize(QSize(buttonWidth, 50))
            self.buttonsLayout.addWidget(self.pushButton_uncheck_all)

            spacerItem = QSpacerItem(100, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.buttonsLayout.addItem(spacerItem)

            self.pushButton_ok = QPushButton()
            self.pushButton_ok.setText('OK')
            self.pushButton_ok.setMaximumSize(QSize(buttonWidth, 50))
            self.buttonsLayout.addWidget(self.pushButton_ok)

            self.pushButton_cancel = QPushButton()
            self.pushButton_cancel.setText('Cancel')
            self.pushButton_cancel.setMaximumSize(QSize(buttonWidth, 50))
            self.buttonsLayout.addWidget(self.pushButton_cancel)
            

            self.mainLayout.addLayout(self.buttonsLayout)



class pathsSelect_MainWindow(QDialog, pathsSelect_UI):
    def __init__(self, parent=None, inputList=None):
        super(pathsSelect_MainWindow, self).__init__(parent)
        self.setupUI(self)

        self.connect(self.pushButton_check_all, SIGNAL('clicked()'), self.checkAll)
        self.connect(self.pushButton_uncheck_all, SIGNAL('clicked()'), self.uncheckAll)

        self.connect(self.pushButton_cancel, SIGNAL('clicked()'), self.close)
        self.connect(self.pushButton_ok, SIGNAL('clicked()'), self.openTexCopyWindow)


        if inputList:
            #print 'GOT KWARGS'
            self.input_list = inputList
            for i in self.input_list:
                item = QListWidgetItem()
                item.setCheckState(Qt.Checked)
                item.setText(i)
                self.list_widget.addItem(item)

            #self.resize(self.width(), self.minimumSizeHint().height())
            self.resize(self.list_widget.sizeHintForColumn(0)+70, self.height())

        self.okno = copyTexUI.copyTexUI(self.input_list, self)

    def openTexCopyWindow(self):
        selectedPaths = list()
        item = self.list_widget.item
        for i in range(self.list_widget.count()):
            if item(i).checkState() == Qt.Checked:
                selectedPaths.append(item(i).data(0))

        #w = uis.copyTexUI.wait_houdini_window(paths = selectedPaths)
        #w.show()
        self.okno.show()
        self.setDisabled(True)
        self.okno.setDisabled(False)
        self.close()



    def checkAll(self):
        item = self.list_widget.item
        #print 'TOTAL WIDGETS COUNT %s' % self.list_widget.count()
        for i in range(self.list_widget.count()):
            #print 'WORKING WITH %s' % i
            item(i).setCheckState(Qt.Checked)

    def uncheckAll(self):
        print('IN UNCHECK')
        item = self.list_widget.item
        #print 'TOTAL WIDGETS COUNT %s' % self.list_widget.count()
        for i in range(self.list_widget.count()):
            #print 'WORKING WITH %s' % i
            item(i).setCheckState(Qt.Unchecked)



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def active(app):
    if app.objectName() == "pathsSelect_MainWindow":
        app.get_list()
        app.show()
    else:
        tp = hou.pwd()
        grp = tp.parmTemplateGroup()
        folderP = grp.find('textures_folder')
        parms_to_avoid = tp.parm('parms_to_keep').eval().split(' ')
        texture_paths = [tp.parm(p.name()).eval() for p in folderP.parmTemplates() if p.name() and p.name() not in parms_to_avoid and '_cs' not in p.name() and '_cf' not in p.name()]

        print('TEXTURE PATHS')
        for txp in texture_paths:
            print(str(txp))

        w = pathsSelect_MainWindow(parent=app,inputList=texture_paths)
        w.show()


def get_Houdini_Window():
    list = QApplication.allWidgets()
    for item in list:
        if item.objectName() == "pathsSelect_MainWindow":
            return item
        elif type(item) == QWidget and item.windowIconText():
            return item
    return False


def wait_houdini_window():
    app = get_Houdini_Window()
    return active(app)



if __name__ == '__main__':
    app = QApplication([])
    w=pathsSelect_MainWindow(inputList = ['asdfasdf', 'sfggg', '3333'])
    w.show()
    sys.exit(app.exec_())
else:
    print('HOUDINI !!!')
    wait_houdini_window()

