import copyTex_ui04_UI

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

except:
    from PySide.QtGui import *
    from PySide.QtCore import *
import sys

class mmm(QDialog, copyTex_ui04_UI.Ui_Dialog):
    def __init__(self, paths=None, parent=None):
        super(mmm, self).__init__(parent)
        self.setupUi(self)

def active(app):
    if app.objectName() == "mmm":
        app.get_list()
        app.show()
    else:
        w = mmm(parent=app)
        w.show()


def get_Houdini_Window():
    list = QApplication.allWidgets()
    for item in list:
        if item.objectName() == "mmm":
            return item
        elif type(item) == QWidget and item.windowIconText():
            return item
    return False


def wait_houdini_window():
    app = get_Houdini_Window()
    return active(app)

if __name__ == '__main__':

    app = QApplication([])
    w = mmm()
    w.show()
    sys.exit(app.exec_())