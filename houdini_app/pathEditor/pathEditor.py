

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *
import sys


class PathEditor(QDialog):
    def __init__(self, parent=None):
        super(PathEditor, self).__init__(parent)
        self.listWidget = QListWidget(self)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.listWidget)

        self.listWidget.addItems(["sss", "xxx", "kkkk", "www"])

        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            item.setData(1, "Sss")
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            print item.data(1)
            print item.text()

    def getTexturesPath(self):
        import hou
        obj = hou.node('/obj')
        child = obj.allSubChildren()
        images = []
        for c in child:
            if c.type().name() == "arnold::image":



        for i in xrange(len(images)):
            item = self.listWidget.addItem(images[i])
            item.setData(i, images[i])



















if __name__ == '__main__':

    app = QApplication([])
    w=PathEditor()
    w.show()
    sys.exit(app.exec_())

