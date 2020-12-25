
try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    import hou
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import sys



class ShotItem(QWidget):

    _data = None

    def __init__(self, data=None, index=None, parent=None):
        super(ShotItem, self).__init__(parent)

        self.lb_shot = QLabel(self)
        self.lb_frame_start = QLabel(self)
        self.lb_frame_end = QLabel(self)
        self.lb_preroll = QLabel(self)

        self.le_shot = QLineEdit(self)
        self.le_frame_start = QLineEdit(self)
        self.le_frame_end = QLineEdit(self)
        self.le_preroll = QLineEdit(self)

        self.le_shot.setValidator(QIntValidator())
        self.le_frame_start.setValidator(QIntValidator())
        self.le_frame_end.setValidator(QIntValidator())
        self.le_preroll.setValidator(QIntValidator())

        # SET WIDGETS TEXT
        self.lb_shot.setText("Shot Number:")
        self.lb_frame_start.setText("Start Frame:")
        self.lb_frame_end.setText("End Frame:")
        self.lb_preroll.setText("Pre Roll")
        self.le_frame_start.setText("1001")
        self.le_frame_end.setText("1050")
        self.le_preroll.setText("10")

        self.hLayoutMain = QHBoxLayout(self)
        self.vLayoutShotNum = QVBoxLayout()
        self.vLayoutFStart = QVBoxLayout()
        self.vLayoutFEnd = QVBoxLayout()
        self.vLayoutPreRoll = QVBoxLayout()

        self.vLayoutShotNum.addWidget(self.lb_shot)
        self.vLayoutShotNum.addWidget(self.le_shot)

        self.vLayoutFStart.addWidget(self.lb_frame_start)
        self.vLayoutFStart.addWidget(self.le_frame_start)

        self.vLayoutFEnd.addWidget(self.lb_frame_end)
        self.vLayoutFEnd.addWidget(self.le_frame_end)

        self.vLayoutPreRoll.addWidget(self.lb_preroll)
        self.vLayoutPreRoll.addWidget(self.le_preroll)

        self.hLayoutMain.addLayout(self.vLayoutShotNum)
        self.hLayoutMain.addLayout(self.vLayoutFStart)
        self.hLayoutMain.addLayout(self.vLayoutFEnd)
        self.hLayoutMain.addLayout(self.vLayoutPreRoll)

        self.le_shot.textChanged.connect(self.check_shot_name)

        self.setStyleSheet("""background:rgba(0,0,0,0);""")

        if not index:
            self.le_shot.setText("010")
        else:
            self.le_shot.setText(str(index).zfill(3))

        if data:
            self.le_shot.setText(data["name"].strip('sh'))
            self.le_frame_start.setText(data["first_frame"])
            self.le_frame_end.setText(data["last_frame"])
            self.le_preroll.setText(data["preroll"])



    def check_shot_name(self):
        if self.le_shot.text() == "":
            self.setStyleSheet("""background:rgb(50,0,0);""")
        else:
            self.setStyleSheet("""background:rgba(0,0,0,0);""")



    @property
    def data(self):
        self._data = dict(name=self.le_shot.text(),
                          first_frame=self.le_frame_start.text(),
                          last_frame=self.le_frame_end.text(),
                          preroll=self.le_preroll.text())
        return self._data




if __name__ == '__main__':

    app = QApplication([])
    w=ShotItem()
    w.show()
    sys.exit(app.exec_())
