# -*- coding: utf-8 -*-
'''
Channel Hotbox v1.4 for Nuke
by Falk Hofmann, London, 2013, last updated 2017

this script allows you to switch, shuffle out or grade channels

click:
change the viewer to the selected channel

shift+click:
shuffle out all selected channels

strg+click:
create grade node with channel set to selected

alt:
switch viewer back to rgba


falk@kombinat-13b.de

import hotbox
nuke.menu("Nuke").findItem("Edit").addCommand("HotBox", 'channelHotbox.start()', "alt+q")

'''

import math
import nuke

try:
    # < Nuke 11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtGui as QtGuiWidgets
except:
    # >= Nuke 11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtGuiWidgets

SHOW_ON_CURSOR = 1  # 0 - uses SHOW_ON_SCREEN method; 1 pops the hotbox centered below the cursor
SHOW_ON_SCREEN = 0  # 0 - show on screen cursor is currently on; 1 - on primary screen ; 2 - on secondary screen


class LayerButton(QtGuiWidgets.QPushButton):
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


class LineEdit(QtGuiWidgets.QLineEdit):
    def __init__(self, parent, layer_list):
        super(LineEdit, self).__init__(parent)
        self.parent = parent
        layer = [i for i in layer_list]
        self.completerList = []
        self.completer = QtGuiWidgets.QCompleter(layer, self)
        self.completer.setCompletionMode(QtGuiWidgets.QCompleter.InlineCompletion)
        self.setCompleter(self.completer)
        self.completer.activated.connect(self.returnPressed)


class HotBox(QtGuiWidgets.QWidget):
    first_release = None
    shuffle_list = []

    def __init__(self):
        super(HotBox, self).__init__()

        av = nuke.activeViewer().node()
        vn = av.input(nuke.activeViewer().activeInput())

        if SHOW_ON_CURSOR == 0:
            screen_offset = 0

            if SHOW_ON_SCREEN == 1:
                screen_rect = QtGui.QApplication.desktop().screenGeometry(1)
                screen_width, screen_height = screen_rect.width(), screen_rect.height()

            elif SHOW_ON_SCREEN == 2:
                screen_rect = QtGui.QApplication.desktop().screenGeometry(0)
                screen_width, screen_height = screen_rect.width(), screen_rect.height()
                screen_offset = QtGui.QApplication.desktop().screenGeometry(1).width()

            else:
                point = QtGui.QCursor.pos()
                screen = QtGui.QDesktopWidget().screenNumber(point)

                if screen == 0:
                    screen_offset = QtGui.QApplication.desktop().screenGeometry(1).width()

                    screen_rect = QtGui.QApplication.desktop().screenGeometry(screen)
                    screen_width, screen_height = screen_rect.width(), screen_rect.height()

        layer = list(set([c.split('.')[0] for c in vn.channels()]))
        layer.sort()

        if 'rgba' in layer:
            layer.remove('rgba')
            layer.insert(0, 'rgba')
            if 'rgb' in layer:
                layer.remove('rgb')
                layer.insert(1, 'rgb')
                if 'alpha' in layer:
                    layer.remove('alpha')
                    layer.insert(2, 'alpha')
            elif 'alpha' in layer:
                layer.remove('alpha')
                layer.insert(1, 'alpha')

        length = math.ceil(math.sqrt(len(layer) + 1))
        width = length * 200
        height = length * 50
        offset = QtCore.QPoint(width * 0.5, height * 0.5)
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)

        if SHOW_ON_CURSOR == 1:
            point = QtGui.QCursor.pos() - offset
            self.move(point)
        else:
            self.move(((screen_width - width) / 2) + screen_offset, (screen_height - height) / 2)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        grid = QtGuiWidgets.QGridLayout()
        self.setLayout(grid)

        column_counter = 0
        row_counter = 0
        button_width = width / length

        for i in layer:
            button = LayerButton(i, button_width)
            button.clicked.connect(self.clicked, )
            button.setSizePolicy(QtGuiWidgets.QSizePolicy.Preferred, QtGuiWidgets.QSizePolicy.Expanding)
            grid.addWidget(button, row_counter, column_counter)

            if column_counter > length:
                row_counter += 1
                column_counter = 0

            else:
                column_counter += 1

        self.input = LineEdit(self, layer)
        self.input.setSizePolicy(QtGuiWidgets.QSizePolicy.Preferred, QtGuiWidgets.QSizePolicy.Expanding)
        grid.addWidget(self.input, row_counter, column_counter)
        self.input.setFocus()

        self.input.returnPressed.connect(self.line_enter)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif e.key() == QtCore.Qt.Key_Alt:
            nuke.activeViewer().node()['channels'].setValue('rgba')
            self.close()
        elif e.key() == QtCore.Qt.Key_Shift:
            self.first_release = True

    def keyReleaseEvent(self, e):
        if e.key() == QtCore.Qt.Key_Shift:
            if self.first_release and self.shuffle_list != []:
                nuke.activeViewer().node()['channels'].setValue('rgba')
                self.close()
                node = nuke.toNode(nuke.activeViewer().node().input(nuke.activeViewer().activeInput()).name())
                for n in self.shuffle_list:
                    shuffle = nuke.nodes.Shuffle(xpos=(node.xpos() + 100), ypos=(node.ypos() + 50),
                                                 label='[value in] -> [value out]')
                    shuffle['in'].setValue(n)
                    shuffle['selected'].setValue(True)
                    shuffle.setInput(0, node)
                    shuffle.autoplace()

            self.first_release = False

    def clicked(self):
        modifiers = QtGuiWidgets.QApplication.keyboardModifiers()

        if modifiers == QtCore.Qt.ShiftModifier:
            channel = self.sender().text()

            if channel in self.shuffle_list:
                self.shuffle_list.remove(channel)
                self.sender().setStyleSheet("background-color: #282828; font: 13px")
            else:
                self.shuffle_list.append(channel)
                self.sender().setStyleSheet("background-color: #1EB028; font: 13px")

        elif modifiers == QtCore.Qt.ControlModifier:
            node = nuke.toNode(nuke.activeViewer().node().input(nuke.activeViewer().activeInput()).name())
            self.close()
            node.setSelected(True)
            grade = nuke.createNode("Grade")
            grade['channels'].setValue(self.sender().text())

        else:
            nuke.activeViewer().node()['channels'].setValue(self.sender().text())
            self.close()

    def line_enter(self):
        nuke.activeViewer().node()['channels'].setValue(self.input.text())
        self.close()


hotbox = None


def start():
    if not len(nuke.allNodes('Viewer')) == 0:
        if nuke.activeViewer().activeInput() is not None:
            global hotbox
            hotbox = HotBox()
            hotbox.show()
        else:
            nuke.message('no active viewer connected to node')
    else:
        nuke.message('no viewer found in script')
