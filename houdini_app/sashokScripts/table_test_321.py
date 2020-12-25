from PySide2 import QtGui, QtCore, QtWidgets
import hou


# solution here:
# https://stackoverflow.com/questions/39995688/set-different-color-to-specifc-items-in-qlistwidget
# https://www.saltycrane.com/blog/2008/01/pyqt4-qitemdelegate-example-with/
class MyDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        painter.save()

        # set background color
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        if option.state & QtWidgets.QStyle.State_Selected:
            # If the item is selected, always draw background blue
            painter.setBrush(QtGui.QBrush(QtCore.Qt.blue))
        else:
            # Get the color
            c = index.data(QtCore.Qt.BackgroundRole)
            painter.setBrush(QtGui.QBrush(QtGui.QColor(c)))

        # Draw the background rectangle
        painter.drawRect(option.rect)

        # Get text data
        text = index.data(QtCore.Qt.DisplayRole)

        # Draw text data
        painter.setPen(QtGui.QPen(index.data(QtCore.Qt.FontRole)))
        painter.setPen(QtGui.QColor(index.data(QtCore.Qt.TextColorRole)))
        alignment = index.data(QtCore.Qt.TextAlignmentRole)
        painter.drawText(option.rect, alignment, text)

        painter.restore()


class Model(QtCore.QAbstractTableModel):
    def __init__(self):
        QtCore.QAbstractTableModel.__init__(self)
        self.tableList = ["Item %02d" % (i + 1) for i in range(5)]

    def rowCount(self, parent):
        return len(self.tableList)

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if (role == QtCore.Qt.DisplayRole):
            return self.tableList[index.row()]

        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignVCenter

        if role == QtCore.Qt.TextColorRole:
            return QtGui.QColor(255, 255, 255)

        if role == QtCore.Qt.BackgroundRole:
            return QtGui.QColor(255, 25 + 30 * index.row(), 75)


class TableView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        tableModel = Model()
        tableView = QtWidgets.QTableView()
        tableView.setModel(tableModel)
        mydelegate = MyDelegate(self)
        tableView.setItemDelegate(mydelegate)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(tableView)
        self.setLayout(hbox)

        # comment / uncomment this line to see colors
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)


# dialog = TableView()
# dialog.show()