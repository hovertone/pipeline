

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os



class FileItem (QWidget):

    _path = ""
    _text = ""
    _type = None
    _date = []

    def __init__(self, path, text, type, date=None, parent=None):
        super(FileItem, self).__init__(parent)

        self._path = path
        self._text = text
        self._type = type
        self._date = date

        self.hLayout = QHBoxLayout(self)

        self.labelIcon = QLabel(self)
        self.labelName = QLabel(self)
        self.labelDate = QLabel(self)

        self.labelName.setText(text)

        if date:
            self.labelDate.setText(date["day"] + " " + date["time"])

        self.hLayout.addWidget(self.labelIcon)
        self.hLayout.addWidget(self.labelName)
        self.hLayout.addWidget(self.labelDate)


        icon_path = os.path.join(os.path.dirname(__file__).replace("\\", "/"), "icons")

        if type == "folder":
            icon = os.path.join(icon_path, "f_icon.png")
            self.labelIcon.setPixmap(QPixmap(icon))
        elif type == "file":
            icon = os.path.join(icon_path, "hip_icon.png")
            self.labelIcon.setPixmap(QPixmap(icon))
        else:
            pass

        self.labelDate.setAlignment(Qt.AlignRight)
        self.labelIcon.setScaledContents(True)
        self.labelIcon.setMinimumSize(QSize(15, 15))
        self.labelIcon.setMaximumSize(QSize(15, 15))
        self.setStyleSheet("""background:rgba(0,0,0,0);""")



    @property
    def path(self):
        return self._path

    @property
    def text(self):
        return self._text

    @property
    def type(self):
        return self._type

    @property
    def date(self):
        return self._date




