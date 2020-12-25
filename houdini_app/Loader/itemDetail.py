# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'D:\PROJECTS\Pipeline\houdini_app\Loader\listItem.ui'
#
# Created: Sun Apr 28 21:43:59 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!
try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os



class ItemDetail(QFrame):

    _path = ""
    _asset_type = ""
    _text = ""
    _folder_type = None
    _date = []
    _load_data = None

    loadSignal = Signal(str)

    def __init__(self, path, asset_type, text, folder_type, date=None, parent=None):
        super(ItemDetail, self).__init__(parent)

        self._path = path
        self._asset_type = asset_type
        self._text = text
        self._folder_type = folder_type
        self._date = date

        if os.path.isfile(path+"/"+text):
            self._folder_type = "file"
        else:
            self._folder_type = "asset"

        self.hLayout = QHBoxLayout(self)
        self.labelIcon = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHeightForWidth(self.labelIcon.sizePolicy().hasHeightForWidth())
        self.labelIcon.setSizePolicy(sizePolicy)
        self.labelIcon.setMaximumSize(QSize(44, 44))
        self.labelIcon.setScaledContents(True)
        self.labelIcon.setWordWrap(True)
        self.hLayout.addWidget(self.labelIcon)
        self.labelName = QLabel(self)
        self.labelName.setScaledContents(False)
        self.hLayout.addWidget(self.labelName)
        spacerItem = QSpacerItem(200, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout.addItem(spacerItem)

        font = QFont()
        font.setWeight(75)
        font.setBold(True)

        font2 = QFont()
        font2.setPointSize(10)
        font2.setWeight(75)
        font2.setBold(True)

        if self._folder_type == "asset":
            self.pb_loadAsset = QPushButton(self)
            self.pb_loadAsset.setText("Open last")
            self.pb_loadAsset.setMinimumSize(75, 27)
            self.pb_loadAsset.clicked.connect(self.load)
            self.hLayout.addWidget(self.pb_loadAsset)

        self.line_2 = QFrame(self)
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.hLayout.addWidget(self.line_2)

        self.versionVLayout = QVBoxLayout()
        self.labelV = QLabel(self)
        if self._folder_type == "asset":
            self.labelV.setText("Last version:")
        elif self._folder_type == "file":
            self.labelV.setText("Version:")
        self.versionVLayout.addWidget(self.labelV)
        self.labelVersion = QLabel(self)
        self.versionVLayout.addWidget(self.labelVersion)
        self.hLayout.addLayout(self.versionVLayout)

        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.hLayout.addWidget(self.line)

        self.dateVLaout = QVBoxLayout()
        self.labelD = QLabel(self)
        self.labelD.setText("Date:")
        self.dateVLaout.addWidget(self.labelD)
        self.labelDate = QLabel(self)

        if date:
            self.labelDate.setText(date["day"] + " " + date["time"])

        self.dateVLaout.addWidget(self.labelDate)
        self.hLayout.addLayout(self.dateVLaout)


        self.labelDate.setFont(font2)
        self.labelVersion.setFont(font2)
        self.labelName.setFont(font2)

        self.labelDate.setMidLineWidth(300)
        self.labelVersion.setMidLineWidth(300)
        self.labelName.setMidLineWidth(300)
        self.labelName.setMaximumWidth(400)

        self.hLayout.setSpacing(3)
        self.hLayout.setContentsMargins(3,3,3,3)

        self.labelName.setText(text)
        icon_path = os.path.join(os.path.dirname(__file__).replace("\\", "/"), "icons")

        if self._folder_type == "shot" or self._folder_type == "asset":
            icon = os.path.join(icon_path, "f_icon_v2.png")
            self.labelIcon.setPixmap(QPixmap(icon))
        elif self._folder_type == "file":
            if self._text.rsplit(".", 1)[1] == 'hip':
                icon = os.path.join(icon_path, "hip_icon.png")
            elif self._text.rsplit(".", 1)[1] == "mb" or self._text.rsplit(".", 1)[1] == "ma":
                icon = os.path.join(icon_path, "maya_icon.png")
            elif self._text.rsplit(".", 1)[1] == "nk" or self._text.rsplit(".", 1)[1] == "nk~":
                icon = os.path.join(icon_path, "nk_icon.png")
            else:
                icon = os.path.join(icon_path, "file_icon.png")
            self.labelIcon.setPixmap(QPixmap(icon))
            if date:
                self.labelDate.setText(date["day"] + " " + date["time"])

        self.setStyleSheet("QLabel{background:rgba(0,0,0,0);}")

        if self._folder_type == 'asset':
            try:
                self.get_last_version()
            except:
                pass


    def load(self):
        print "EMIT"
        self.loadSignal.emit(str(self._load_data))


    def get_last_version(self):
        path = os.path.join(self._path, self._text)
        files = os.listdir(path)
        versions = []

        for f in files:
            if len(f.split(".")) == 2:
            # if not "afanasy" in f:
                if not os.path.isdir(os.path.join(path, f).replace("\\", "/")):
                    v = f.rsplit(".", 1)[0][-3:]
                    versions.append(v)
        versions = sorted(versions)
        self.labelVersion.setText(versions[-1])

        for f in files:
            if len(f.split(".")) == 2:
            # if not "afanasy" in f:
                v = f.rsplit(".", 1)[0][-3:]
                if v == versions[-1]:
                    self._load_data = os.path.join(path, f).replace("\\", "/")
                    return self._load_data


    def resizeEvent(self, *args, **kwargs):
        self.labelIcon.setMaximumSize(self.height(), self.height())


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

    @property
    def load_data(self):
        return self._load_data



