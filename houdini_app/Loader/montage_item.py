

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import sys, os



class MontageItem(QFrame):

    _dailies = None

    def __init__(self, shot, parent=None):
        super(MontageItem, self).__init__(parent)
        self.lb_name = QLabel(self)
        self.hLayout = QHBoxLayout(self)
        self.cbox = QComboBox(self)

        self.lb_name.setText(shot)
        self.hLayout.addWidget(self.lb_name)
        self.hLayout.addWidget(self.cbox)
        self.hLayout.setContentsMargins(1,1,1,1)
        self.lb_name.setStyleSheet("""color:rgb(250,250,250);""")
        #self.setStyleSheet('''QCheckBox{color:rgb(200,200,200);}
        #QFrame{background:rgba(0,0,0,0);}''')
        self.get_dailies(shot=shot)


    @property
    def dailies(self):
        return self.lb_name.text() + "/out/" + self.cbox.currentText()


    def get_dailies(self, shot):
        if os.path.exists(shot+"/out"):
            for f in os.listdir(shot+"/out"):
                if "DAILIES" in f:
                    self.cbox.addItem(f)









if __name__ == '__main__':

    app = QApplication([])
    w=MontageItem("P:/Raid/sequences/serenade/sh010")
    w.show()
    sys.exit(app.exec_())