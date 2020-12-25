

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os



class FileItem (QFrame):

    _path = ""
    _asset_type = ""
    _text = ""
    _folder_type = None
    _date = []

    def __init__(self, path, asset_type, text, folder_type, date=None, parent=None):
        super(FileItem, self).__init__(parent)

        self._path = path
        self._asset_type = asset_type
        self._text = text
        self._folder_type = folder_type
        self._date = date

        if folder_type == "shot":
            self.hLayout = QVBoxLayout(self)
        else:
            self.hLayout = QHBoxLayout(self)

        self.sLayout = QHBoxLayout()

        self.labelIcon = QLabel(self)
        self.labelName = QLabel(self)
        self.labelDate = QLabel(self)

        self.labelName.setText(text)

        if folder_type == "file":
            if date:
                self.labelDate.setText(date["day"] + " " + date["time"])

        self.hLayout.addWidget(self.labelIcon)
        self.sLayout.addWidget(self.labelName)
        self.hLayout.addWidget(self.labelDate)
        self.hLayout.addLayout(self.sLayout)


        icon_path = os.path.join(os.path.dirname(__file__).replace("\\", "/"), "icons")

        if folder_type == "shot" or folder_type == "asset":
            icon = os.path.join(icon_path, "f_icon.png")
            self.labelIcon.setPixmap(QPixmap(icon))
        elif folder_type == "file":
            icon = os.path.join(icon_path, "hip_icon.png")
            self.labelIcon.setPixmap(QPixmap(icon))
        else:
            pass

        #self.labelIcon.setScaledContents(True)

        self.labelDate.setAlignment(Qt.AlignRight)
        self.labelIcon.setScaledContents(True)
        #self.labelIcon.sizeHint()
        self.labelIcon.setMinimumSize(50,50)
        #self.labelIcon.setMaximumSize(200,200)
        self.hLayout.setSpacing(3)
        self.hLayout.setContentsMargins(3,3,3,3)
        self.setObjectName("Item")
        self.setStyleSheet("QLabel{background:rgba(0,0,0,0);}")
        self.setStyleSheet("QFrame#Item{border:1px solid black;}")



    @property
    def path(self):
        return self._path

    @property
    def asset_type(self):
        return self._asset_type

    @property
    def text(self):
        return self._text

    @property
    def folder_type(self):
        return self._folder_type

    @property
    def date(self):
        return self._date




