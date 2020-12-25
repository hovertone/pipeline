

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os



class AssetItem(QFrame):

    _name = ""
    _current = ""
    _last = None

    def __init__(self, name, current, last, parent=None):
        super(AssetItem, self).__init__(parent)
        self._name = name
        self._current = current
        self._last = last
        self.hLayout = QHBoxLayout(self)
        self.labelName = QLabel(self)
        self.labelCurrent = QLabel(self)
        self.labelLast = QLabel(self)
        self.hLayout.addWidget(self.labelName)
        self.hLayout.addWidget(self.labelCurrent)
        self.hLayout.addWidget(self.labelLast)
        self.labelName.setText(name)
        self.labelCurrent.setText("Current version:   " + str(current))
        self.labelLast.setText("Last version:   " + str(last))
        self.setStyleSheet("""background:rgba(0,0,0,0);""")





    @property
    def name(self):
        return self._name

    @property
    def current(self):
        return self._current

    @property
    def last(self):
        return self._last




