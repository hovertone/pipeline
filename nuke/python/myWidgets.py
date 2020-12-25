try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
except:
    from PySide import QtGui
    from PySide import QtCore


class QTextMovieLabel(QtWidgets.QLabel):
    def __init__(self, text, fileName):
        QtGuiWidgets.QLabel.__init__(self)
        self._text = text
        m = QtGuiWidgets.QMovie(fileName)
        m.start()
        self.setMovie(m)

        # pos = QtGui.QCursor.pos()
        # print pos.x()
        # self.adjustSize()
        # print self.width()
        # self.move(pos.x() - self.width() / 2, pos.y() - self.height() / 2)

    def setMovie(self, movie):
        QtGuiWidgets.QLabel.setMovie(self, movie)
        s=movie.currentImage().size()
        self._movieWidth = s.width()
        self._movieHeight = s.height()

    def paintEvent(self, evt):
        QtGuiWidgets.QLabel.paintEvent(self, evt)
        p = QtGuiWidgets.QPainter(self)
        p.setFont(self.font())
        x = self._movieWidth + 6
        y = (self.height() + p.fontMetrics().xHeight()) / 2
        p.drawText(x, y, self._text)
        p.end()

    def sizeHint(self):
        fm = QtGuiWidgets.QFontMetrics(self.font())
        return QtCore.QSize(self._movieWidth + 6 + fm.width(self._text),
                self._movieHeight)

    def setText(self, text):
        self._text = text


class gifTooltipWindow(QtWidgets.QWidget):
    def __init__(self, gifName):
        super(gifTooltipWindow, self).__init__()

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.masterLayout = QtGuiWidgets.QVBoxLayout(self)
        self.gif = QTextMovieLabel('', 'C:/Users/Admin/Downloads/%s.gif' % (gifName))
        self.masterLayout.addWidget(self.gif)
        self.setLayout(self.masterLayout)

        # pos = QtGui.QCursor.pos()
        # self.adjustSize()
        # self.move(pos.x() - self.width()/2, pos.y() - self.height()/2)
        #self.adjustSize()



class LayerButton(QtWidgets.QPushButton):
    def __init__(self, name, button_width, parent=None):
        super(LayerButton, self).__init__(parent)
        self.setMouseTracking(True)
        self.setText(name)
        self.setMinimumWidth(button_width / 2)
        self.regular_color = "background-color:#282828; font: 13px"
        self.orange_color = "background-color:#C26828; font: 13px"
        self.green_color = "background-color: #1EB028; font: 13px"
        self.setStyleSheet(self.regular_color)

    def enterEvent(self, event):
        if not self.styleSheet() == self.green_color:
            self.setStyleSheet(self.orange_color)

    def leaveEvent(self, event):
        if not self.styleSheet() == self.green_color:
            self.setStyleSheet(self.regular_color)

class ScriptButtonWithGif(LayerButton):
    def __init__(self, name, script, gifname, button_width, parent=None):
        super(ScriptButtonWithGif, self).__init__(name, button_width, parent)
        self.script = script
        self.gifname = gifname
        self.setMouseTracking(True)

        #self.clicked.connect(self.executeScript, )
        #self.tooltipWindowAppear = False

    def mouseMoveEvent(self, event):
        if self.gifname != None:
            if not self.tooltipWindowAppear:
                timer = QtCore.QTimer()
                timer.singleShot(500, self.shower)
            self.tooltipWindowAppear = True

    def shower(self):
        global g

        g = gifTooltipWindow(self.gifname)
        g.show()

    def enterEvent(self, event):
        pass
        #print 'Mouse Enter'


    def leaveEvent(self, event):
        #print 'Mouse Leave'
        global g
        #g = gifTooltipWindow()
        if self.gifname != None:
            g.close()
            g.destroy()
            del(g)
            self.tooltipWindowAppear = False

    def executeScript(self):
        exec (self.sender().script)
        self.close()
        self.destroy()

    # def keyPressEvent(self, e):
    #     #nuke.message('keyPressEvent')
    #     if e.key() == QtCore.Qt.Key_Escape:
    #         self.close()
    #         self.destroy()
    #
    # def keyReleaseEvent(self, e):
    #     pass
    #
    # def eventFilter(self, object, event):
    #     if event.type() in [QtCore.QEvent.WindowDeactivate, QtCore.QEvent.FocusOut]:
    #         self.close()
    #         self.destroy()
    #         return True


class LineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent, layer_list):
        super(LineEdit, self).__init__(parent)
        self.parent = parent
        layer = [i for i in layer_list]
        self.completerList = []
        self.completer = QtGuiWidgets.QCompleter(layer, self)
        self.completer.setCompletionMode(QtGuiWidgets.QCompleter.InlineCompletion)
        self.setCompleter(self.completer)
        self.completer.activated.connect(self.returnPressed)