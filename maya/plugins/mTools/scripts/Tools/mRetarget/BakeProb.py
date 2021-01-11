import MUI.MaxUI as mui
reload (mui)
import PySide2.QtGui as qg
import PySide2.QtCore as qc
import PySide2.QtWidgets as qw
import maya.cmds as cmds

class BakeProb(qw.QDialog):

    def __init__(self):
        qw.QDialog.__init__(self)

        '''-------- Window --------'''

        mui.Window(W=self, Titel="Prob", Width=325, Height=330)

        '''---------- UI ----------'''

        mui.Button

BakeProb_Dialog = BakeProb()
BakeProb_Dialog.show()