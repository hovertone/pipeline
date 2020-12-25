# -*- coding: utf-8 -*-


try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import sys, os
from updaterUi_UIs import Ui_UpdateAssets
import item



try:
    import hou
except:
    pass



class AssetsUpdate(QDialog, Ui_UpdateAssets):

    def __init__(self, parent=None):
        super(AssetsUpdate, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_update.setEnabled(False)
        self.listWidget.itemClicked.connect(self.selecItems)
        self.pushButton_update.clicked.connect(self.updateBtn)
        self.pushButton_close.clicked.connect(self.close)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)


    def get_assets(self):
        self.listWidget.clear()
        obj = hou.node('/obj')
        s = obj.children()
        dictList = []
        for i in s:
            try:
                current = int(i.parm("version").eval())
                attr_value = i.parm("fileName").eval()
                v = attr_value.rsplit("/", 2)[0]
                versions = os.listdir(v)
                last = int(versions[-1].replace("v", ""))
                asset = {
                    "name": i.name(),
                    "current": current,
                    "last": last,
                }
                dictList.append(asset)
            except:
                pass

        for d in dictList:
            model = item.AssetItem(name=d['name'], current=d['current'], last=d['last'])
            listItem = QListWidgetItem()
            self.listWidget.addItem(listItem)
            listItem.setSizeHint(QSize(0, 40))
            self.listWidget.setItemWidget(listItem, model)


    def selecItems(self):
        self.pushButton_update.setEnabled(True)


    def updateBtn(self):
        if self.listWidget.selectedItems():
            for item in self.listWidget.selectedItems():
                name = self.listWidget.itemWidget(item).name
                obj = hou.node('/obj/' + name)
                obj.parm("set_last_version").pressButton()
            return self.get_assets()











if __name__ == '__main__':

    app = QApplication([])
    w=AssetsUpdate()
    print w.objectName()
    w.show()
    sys.exit(app.exec_())
