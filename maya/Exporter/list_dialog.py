

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *
import sys




class ListDialog(QDialog):
    def __init__(self, parent=None):
        super(ListDialog, self).__init__(parent)

        self.list = QListWidget(self)
        self.pb_ok = QPushButton(self)
        self.pb_cancel = QPushButton(self)

        self.pb_ok.setText("OK")
        self.pb_cancel.setText("Cancel")

        self.pb_ok.setEnabled(False)

        self.vLayoutMain = QVBoxLayout(self)

        self.hLayout = QHBoxLayout()

        self.hLayout.addWidget(self.pb_ok)
        self.hLayout.addWidget(self.pb_cancel)

        self.vLayoutMain.addWidget(self.list)
        self.vLayoutMain.addLayout(self.hLayout)

        self.pb_cancel.clicked.connect(self.close)
        self.list.itemClicked.connect(self.item_click)


    def item_click(self):
        self.pb_ok.setEnabled(True)




if __name__ == '__main__':

    app = QApplication([])
    w=ListDialog()
    w.show()
    sys.exit(app.exec_())
