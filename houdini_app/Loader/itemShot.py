

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os



class FileItemShot(QFrame):

    _path = ""
    _asset_type = ""
    _text = ""
    _folder_type = None
    _date = []


    def __init__(self, path, asset_type, text, folder_type, date=None, parent=None):
        super(FileItemShot, self).__init__(parent)

        self._path = path
        self._asset_type = asset_type
        self._text = text
        self._folder_type = folder_type
        self._date = date

        self.hLayout = QVBoxLayout(self)
        #self.sLayout = QHBoxLayout()
        self.labelIcon = QLabel(self)
        self.labelName = QLabel(self)
        self.labelDate = QLabel(self)


        if folder_type == "file":
            if date:
                self.labelDate.setText(date["day"] + " " + date["time"])

        self.hLayout.addWidget(self.labelIcon)
        self.hLayout.addWidget(self.labelName)


        basic_icon = os.path.join(os.path.dirname(__file__).replace("\\", "/"), "icons")
        out_icon = os.path.join(self._path, self._text+"/out/proxy/proxy.jpg").replace("\\","/")

        if folder_type == "shot" or folder_type == "asset":

            if os.path.isfile(out_icon):
                icon = out_icon
            else:
                icon = os.path.join(basic_icon, "f_icon_v2.png")

            pix = QPixmap(icon)

            pix.scaled(self.width(), self.height())
            self.icon = pix
            self.labelIcon.setPixmap(QPixmap(self.icon))
            self.labelIcon.setScaledContents(True)
            self.labelIcon.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.MinimumExpanding)

        elif folder_type == "file":
            icon = os.path.join(basic_icon, "hip_icon.png")
            pix = QPixmap(icon)
            self.icon = pix.scaled(self.width(), self.height())
            self.labelIcon.setPixmap(QPixmap(self.icon))
        else:
            pass

        self.labelIcon.setScaledContents(True)
        font = QFont()
        font.setBold(True)
        font.setPointSize(9)

        self.labelName.setFont(font)
        self.labelName.setText(text)
        self.labelIcon.setGeometry(QRect(10, 10, 100, 100))

        self.labelDate.setAlignment(Qt.AlignRight)
        self.labelName.setAlignment(Qt.AlignHCenter)

        self.labelIcon.setScaledContents(True)
        self.hLayout.setSpacing(4)
        self.hLayout.setContentsMargins(3,3,3,3)

        self.setObjectName("Item")
        self.labelIcon.setObjectName("Icon")
        self.setStyleSheet("QLabel{background:rgba(0,0,0,0);}")
        #self.labelIcon.setStyleSheet("QLabel#Icon{border:1px solid gray; border-radius: 2px;}")
        # self.setStyleSheet("QFrame#Item{"
        #                    "border:1px solid dark-gray;"
        #                    "border-radius: 2px;}")
        #


    def set_icon(self, image):
        self.labelIcon.setPixmap(QPixmap(image))
        self.labelIcon.repaint()


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




