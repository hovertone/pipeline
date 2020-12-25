# -*- coding: utf-8 -*-


try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    import hou
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os, sys
from functools import partial
from ui.AssetsLib_v002_UIs import Ui_AssetsLib
from lib_item import AssetItem



class AssetsLoader(QDialog, Ui_AssetsLib):

    def __init__(self, parent=None):
        super(AssetsLoader, self).__init__(parent)
        self.setupUi(self)
        self.hSlider_zoom.setValue(100)
        self.path = "O:/"


        self.cbox_category.currentIndexChanged.connect(self.get_list)
        self.hSlider_zoom.valueChanged.connect(self.slider_value)
        self.le_search.textChanged.connect(self.search_action)
        self.cbox_category.setCurrentIndex(3)
        self.get_list()



    def get_list(self, text=None):

        self.listWidget_lib.clear()
        path = os.path.join(self.path, self.cbox_category.currentText()).replace("\\", "/")
        list = os.listdir(path)
        files = []

        for l in list:
            if l[-3:] == "hda":
                if text:
                    if str(text) in l:
                        files.append(l)
                else:
                    files.append(l)

        for f in files:
            model = AssetItem(path=path, text=f)
            model.pb_load.clicked.connect(partial(self.itemAction, model.lb_text.text()))
            listItem = QListWidgetItem()
            listItem.setText(f.split(".")[0])
            self.listWidget_lib.addItem(listItem)
            listItem.setSizeHint(QSize(self.hSlider_zoom.value(), self.hSlider_zoom.value()))
            self.listWidget_lib.setItemWidget(listItem, model)


    def itemAction(self, text):
        net_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
        parent = net_editor.pwd()
        hou.node(parent.path()).createNode(text, text, run_init_scripts=True)


    def slider_value(self):
        value = self.hSlider_zoom.value()
        for i in range(self.listWidget_lib.count()):
            self.listWidget_lib.item(i).setSizeHint(QSize(value, value))


    def search_action(self):
        if self.le_search.text() > 1:
            self.get_list(text=self.le_search.text())












if __name__ == '__main__':

    app = QApplication([])
    w=AssetsLoader()
    w.show()
    sys.exit(app.exec_())
