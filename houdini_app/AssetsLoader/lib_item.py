
try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os
import json



class AssetItem(QFrame):

    _path = ""
    _text = ""



    def __init__(self, path, text, type = None, parent=None):
        super(AssetItem, self).__init__(parent)

        self._path = path

        self.vLayout = QVBoxLayout(self)
        self.hLayout = QHBoxLayout()

        self.lb_icon = QLabel(self)
        self.lb_text = QLabel(self)
        self.pb_load = QPushButton(self)
        self.pb_load.setText("Add")
        self.pb_load.setMinimumSize(40,22)


        self.vLayout.addWidget(self.lb_icon)
        self.hLayout.addWidget(self.lb_text)
        spacerItem = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout.addItem(spacerItem)
        self.hLayout.addWidget(self.pb_load)
        self.vLayout.addLayout(self.hLayout)




        name = text.rsplit(".", 1)[0]
        icon = os.path.join(path, name+".jpg").replace("\\", "/")
        if not os.path.exists(icon):
            icon = os.path.join(path, name + ".png").replace("\\", "/")
        if not os.path.isfile(icon):
            base_path = os.path.dirname(__file__).replace("\\", "/")
            icon = os.path.join(base_path, "icons/no_image.png")

        self.lb_icon.setPixmap(QPixmap(icon))
        self.lb_icon.setScaledContents(True)
        self.lb_icon.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.MinimumExpanding)

        self.lb_text.setText(name)

        self.setObjectName("Item")
        self.lb_text.setStyleSheet("""background:rgba(0,0,0,0);""")
        self.setStyleSheet("QFrame{background:rgb(45,45,45);}\n"
                           "QFrame:hover{background:rgb(22,60,90);}\n"
                           "QFrame#Item{border:1px solid black;}")




        # NUKE TOOLTIPS
        folder = path.split('/')[:2]
        json_path = os.path.join('/'.join(folder), "descriptions.json").replace('\\', '/')
        try:
            data = dict()
            with open(json_path) as json_file:
                data = json.load(json_file)

            #print name, type#, data
            if '%s_%s' % (type, name) in data.keys():
                print 'tvar'
                self.setToolTip(data['%s_%s' % (type, name)])
        except:
            pass




    @property
    def text(self):
        return self.lb_text.text()

    @property
    def path(self):
        return self._path

