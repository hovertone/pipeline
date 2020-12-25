from PySide.QtGui import QApplication, QMainWindow, QPushButton, \
            QVBoxLayout, QWidget

class HoverButton(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        print 'Mouse Enter'

    def leaveEvent(self, event):
        print 'Mouse Leave'

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        button = HoverButton('Test')
        centralWidget = QWidget()
        vbox = QVBoxLayout(centralWidget)
        vbox.addWidget(button)
        self.setCentralWidget(centralWidget)

def startmain():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    startmain()