

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    import hou
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import sys



class SequenceItem(QWidget):

    _name = ""
    _fps = ""
    _shots = None


    def __init__(self, index=None, name=None, data=None, fps=None, parent=None):
        super(SequenceItem, self).__init__(parent)
        self.lb_sqName = QLabel(self)
        self.lb_sqName.setText("Sequence Name: ")
        self.le_sqName = QLineEdit(self)
        if index:
            self.le_sqName.setText("SQ" + str(index))
        self.lb_fps = QLabel(self)
        self.lb_fps.setText("FPS")
        self.le_fps = QLineEdit(self)
        self.hLayout = QHBoxLayout(self)
        self.hLayout.addWidget(self.lb_sqName)
        self.hLayout.addWidget(self.le_sqName)
        self.hLayout.addWidget(self.lb_fps)
        self.hLayout.addWidget(self.le_fps)
        self.setStyleSheet("""background:rgba(0,0,0,0);""")

        if data:
            self.le_sqName.setText(name)
            if fps:
                self.le_fps.setText(fps)
            self.set_shots(data)


    def set_shots(self, shots):
        print "SET SHOTS"
        new_shots = self.remove_sh(shots)
        newlist = sorted(new_shots, key=lambda k: k['name'])
        self._shots = newlist


    def remove_sh(self, shots):
        new_shots = []
        for i in shots:

            nshot=dict(name=i['name'].strip('sh'),
                       first_frame=i["first_frame"],
                       last_frame=i["last_frame"],
                       preroll=i["preroll"])
            new_shots.append(nshot)
        return new_shots




    @property
    def name(self):
        return self.le_sqName.text()

    @property
    def fps(self):
        return self.le_fps.text()

    @property
    def shots(self):
        return self._shots




if __name__ == '__main__':

    app = QApplication([])
    w=SequenceItem()
    w.show()
    sys.exit(app.exec_())
