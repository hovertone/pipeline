

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *
import sys



class ComboBoxShot(QComboBox):
    def __init__(self, parent=None):
        super(ComboBoxShot, self).__init__(parent)
        pass







if __name__ == '__main__':

    app = QApplication([])
    w=ComboBoxShot()
    w.show()
    sys.exit(app.exec_())


