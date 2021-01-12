print 'in subprocess taskbar'

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *


class TaskThread(QThread):
    taskFinished = Signal()

    def __init__(self, function, p):
        QThread.__init__(self)
        self.function = function
        self.size = dict(width=1920, height=1080)

    def setSize(self, width, height):
        self.size = dict(width=width, height=height)

    def run(self):
        self.function(size=self.size)
        self.taskFinished.emit()

def rmv(p):
    pass


def main():
    print 'in main'

