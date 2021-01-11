#-------------------Maya 2017-------------------------#

try:
    import PySide2.QtGui as qg
    import PySide2.QtCore as qc
    import PySide2.QtWidgets as qw
    from PySide2.QtCore import Signal as pyqtSignal
    from PySide2.QtCore import Slot as pyqtSlot
    import ast
    import ctypes

    class PushButtonRight(qw.QPushButton):

       rightClick = pyqtSignal()

       def __init__(self, string, W):
           qw.QPushButton.__init__(self, string, W)

       def mousePressEvent(self, event):
           qw.QPushButton.mousePressEvent(self, event)

           if event.button() == qc.Qt.RightButton:
               self.rightClick.emit()

    Style = ["(68, 68, 68)", "(93, 93, 93, 255)", "(112, 112, 112, 255)", "(29, 29, 29, 255)", "(200, 200, 200, 255)", 11, "(98, 98, 98)", 1]

    def Window(W, Titel="", Width=100, Height=100, WState="Fixed", HState="Fixed", MW=False, Pos=[0,0], WColor = Style[0], Modal=False):

        W.setWindowTitle(Titel)
        W.setWindowFlags(qc.Qt.WindowStaysOnTopHint)

        '''---------------------'''

        if WState == "Fixed":
            W.setFixedWidth(Width)

        if WState == "Maximum":
            W.setMaximumWidth(Width)

        if WState == "Minimum":
            W.setMinimumWidth(Width)

        '''---------------------'''

        if HState == "Fixed":
            W.setFixedHeight(Height)

        if HState == "Maximum":
            W.setMaximumHeight(Width)

        if HState == "Minimum":
            W.setMinimumHeight(Width)

        '''---------------------'''

        if MW == True:
            W.move(Pos[0],Pos[0])

        WC = list(ast.literal_eval(WColor))

        p = W.palette()
        p.setColor(W.backgroundRole(), qg.QColor(WC[0], WC[1], WC[2]))
        W.setPalette(p)

        W.setModal(Modal)

        return W

    def Button(W, Name = "", Pos=[0,0], Width = 50, Height = 20, Color = Style[1], Hover = Style[2], Presed = Style[3], FColor = Style[4], FSize = Style[5], BColor = Style[6], BSize = Style[7], TT = "", IPath = ""):

        btn = PushButtonRight(Name, W)

        btn.move(Pos[0], Pos[1])

        BC = list(ast.literal_eval(Presed))

        if ((BC[0]+BC[1]+BC[2])/3) > 128:
            PBC = "(" + str(BC[0] - 5) + ", " + str(BC[1] - 5) + ", " + str(BC[2] - 5) + ")"
        else:
            PBC = "(" + str(BC[0] + 5) + ", " + str(BC[1] + 5) + ", " + str(BC[2] + 5) + ")"

        btn.setFixedWidth(Width)
        btn.setFixedHeight(Height)
        btn.setStyleSheet("QPushButton{background-color: rgba" + Color + "; color: rgba" + FColor + "; font-size: " + str(FSize) + "px; border: " + str(BSize) + "px solid rgb" + BColor + ";}"
                          "QPushButton:hover{background-color: rgba" + Hover + "}"
                          "QPushButton:pressed{background-color: rgba" + Presed + "; color: rgb(255, 255, 255); border: solid rgb" + PBC + ";}"
                          )

        if TT != "":
            btn.setToolTip(TT)

        btn.setIcon(qg.QIcon(IPath))

        return btn

    def CheckButton(W, Name = "", Pos=[0,0], Width = 50, Height = 20, Color = Style[1], Hover = Style[2], Presed = Style[3], FColor = Style[4], FSize = Style[5], BColor = Style[6], BSize = Style[7], TT = "", IPath = ""):

        cbtn = PushButtonRight(Name, W)

        cbtn.setCheckable(True)

        cbtn.move(Pos[0], Pos[1])

        BC = list(ast.literal_eval(Presed))

        if ((BC[0] + BC[1] + BC[2]) / 3) > 128:
            PBC = "(" + str(BC[0] - 5) + ", " + str(BC[1] - 5) + ", " + str(BC[2] - 5) + ")"
        else:
            PBC = "(" + str(BC[0] + 5) + ", " + str(BC[1] + 5) + ", " + str(BC[2] + 5) + ")"

        cbtn.setFixedWidth(Width)
        cbtn.setFixedHeight(Height)
        cbtn.setStyleSheet("QPushButton{background-color: rgba" + Color + "; color: rgba" + FColor + "; font-size: " + str(FSize) + "px; border: " + str(BSize) + "px solid rgb" + BColor + ";}"
                          "QPushButton:hover{background-color: rgba" + Hover + "}"
                          "QPushButton:pressed{background-color: rgba" + Presed + "; color: rgb(255, 255, 255); border: solid rgb" + PBC + ";}"
                          "QPushButton:on{background-color: rgba" + Presed + "; color: rgb(255, 255, 255); border: solid rgb" + PBC + ";}"
                          )

        if TT != "":
            cbtn.setToolTip(TT)

        cbtn.setIcon(qg.QIcon(IPath))

        return cbtn

    def Spinner(W, SType="Float", Pos=[0,0],  Width = 50, Height = 20, Range="(0, 100)", Value=0, Step=1, Suffix="", TT=""):

        SR = list(ast.literal_eval(Range))

        if SType == "Integer":

            spn = qw.QSpinBox(W)
            spn.move(Pos[0], Pos[1])

            spn.setRange(SR[0], SR[1])

            spn.setValue(Value)
            spn.setSingleStep(Step)
            spn.setSuffix(Suffix)

            if TT != "":
                spn.setToolTip(TT)

        if SType == "Float":

            spn = qw.QDoubleSpinBox(W)
            spn.move(Pos[0], Pos[1])

            spn.setRange(SR[0], SR[1])

            spn.setValue(Value)
            spn.setSingleStep(Step)
            spn.setSuffix(Suffix)

            if TT != "":
                spn.setToolTip(TT)

        spn.setFixedWidth(Width)
        spn.setFixedHeight(Height)

        return spn

    def CheckBox(W, Name="", Pos=[0,0], State=False, TT=""):

        cb = qw.QCheckBox(Name, W)
        cb.move(Pos[0], Pos[1])

        if State == True:
            cb.toggle()

        if TT != "":
            cb.setToolTip(TT)

        return cb

    def Label(W, Text="", Pos=[0,0]):
        lbl = qw.QLabel(W)
        lbl.move(Pos[0], Pos[1])
        lbl.setText(Text)

        return lbl

    def TextBox(W, Text="", Pos=[0,0], Width=100, Height=20):

        tb = qw.QLineEdit(W)
        tb.move(Pos[0], Pos[1])
        tb.setText(Text)
        tb.setFixedWidth(Width)
        tb.setFixedHeight(Height)

        return tb

    def ListBox(W, Pos=[0,0], Width=100, Height=100):
        lb = qw.QListWidget(W)
        lb.move(Pos[0], Pos[1])
        lb.setFixedWidth(Width)
        lb.setFixedHeight(Height)

        return lb

    def GroupeBox(W, Name="", Pos=[0,0], Width=100, Height=100):
        gb = qw.QGroupBox(Name, W)
        gb.move(Pos[0], Pos[1])
        gb.setFixedWidth(Width)
        gb.setFixedHeight(Height)

        return gb

#-------------------Maya 2016-------------------------#

except ImportError:
    import PySide.QtGui as qg
    import PySide.QtCore as qc
    from PySide.QtCore import Signal as pyqtSignal
    from PySide.QtCore import Slot as pyqtSlot
    import ast
    import ctypes

    class PushButtonRight(qg.QPushButton):

       rightClick = pyqtSignal()

       def __init__(self, string, W):
           qg.QPushButton.__init__(self, string, W)

       def mousePressEvent(self, event):
           qg.QPushButton.mousePressEvent(self, event)

           if event.button() == qc.Qt.RightButton:
               self.rightClick.emit()

    Style = ["(68, 68, 68)", "(93, 93, 93, 255)", "(112, 112, 112, 255)", "(29, 29, 29, 255)", "(200, 200, 200, 255)", 11, "(98, 98, 98)", 1]

    def Window(W, Titel="", Width=100, Height=100, WState="Fixed", HState="Fixed", MW=False, Pos=[0,0], WColor = Style[0], Modal=False):

        W.setWindowTitle(Titel)
        W.setWindowFlags(qc.Qt.WindowStaysOnTopHint)

        '''---------------------'''

        if WState == "Fixed":
            W.setFixedWidth(Width)

        if WState == "Maximum":
            W.setMaximumWidth(Width)

        if WState == "Minimum":
            W.setMinimumWidth(Width)

        '''---------------------'''

        if HState == "Fixed":
            W.setFixedHeight(Height)

        if HState == "Maximum":
            W.setMaximumHeight(Width)

        if HState == "Minimum":
            W.setMinimumHeight(Width)

        '''---------------------'''

        if MW == True:
            W.move(Pos[0],Pos[0])

        WC = list(ast.literal_eval(WColor))

        p = W.palette()
        p.setColor(W.backgroundRole(), qg.QColor(WC[0], WC[1], WC[2]))
        W.setPalette(p)

        W.setModal(Modal)

        return W

    def Button(W, Name = "", Pos=[0,0], Width = 50, Height = 20, Color = Style[1], Hover = Style[2], Presed = Style[3], FColor = Style[4], FSize = Style[5], BColor = Style[6], BSize = Style[7], TT = "", IPath = ""):

        btn = PushButtonRight(Name, W)

        btn.move(Pos[0], Pos[1])

        BC = list(ast.literal_eval(Presed))

        if ((BC[0]+BC[1]+BC[2])/3) > 128:
            PBC = "(" + str(BC[0] - 5) + ", " + str(BC[1] - 5) + ", " + str(BC[2] - 5) + ")"
        else:
            PBC = "(" + str(BC[0] + 5) + ", " + str(BC[1] + 5) + ", " + str(BC[2] + 5) + ")"

        btn.setFixedWidth(Width)
        btn.setFixedHeight(Height)
        btn.setStyleSheet("QPushButton{background-color: rgba" + Color + "; color: rgba" + FColor + "; font-size: " + str(FSize) + "px; border: " + str(BSize) + "px solid rgb" + BColor + ";}"
                          "QPushButton:hover{background-color: rgba" + Hover + "}"
                          "QPushButton:pressed{background-color: rgba" + Presed + "; color: rgb(255, 255, 255); border: solid rgb" + PBC + ";}"
                          )

        if TT != "":
            btn.setToolTip(TT)

        btn.setIcon(qg.QIcon(IPath))

        return btn

    def CheckButton(W, Name = "", Pos=[0,0], Width = 50, Height = 20, Color = Style[1], Hover = Style[2], Presed = Style[3], FColor = Style[4], FSize = Style[5], BColor = Style[6], BSize = Style[7], TT = "", IPath = ""):

        cbtn = PushButtonRight(Name, W)

        cbtn.setCheckable(True)

        cbtn.move(Pos[0], Pos[1])

        BC = list(ast.literal_eval(Presed))

        if ((BC[0] + BC[1] + BC[2]) / 3) > 128:
            PBC = "(" + str(BC[0] - 5) + ", " + str(BC[1] - 5) + ", " + str(BC[2] - 5) + ")"
        else:
            PBC = "(" + str(BC[0] + 5) + ", " + str(BC[1] + 5) + ", " + str(BC[2] + 5) + ")"

        cbtn.setFixedWidth(Width)
        cbtn.setFixedHeight(Height)
        cbtn.setStyleSheet("QPushButton{background-color: rgba" + Color + "; color: rgba" + FColor + "; font-size: " + str(FSize) + "px; border: " + str(BSize) + "px solid rgb" + BColor + ";}"
                          "QPushButton:hover{background-color: rgba" + Hover + "}"
                          "QPushButton:pressed{background-color: rgba" + Presed + "; color: rgb(255, 255, 255); border: solid rgb" + PBC + ";}"
                          "QPushButton:on{background-color: rgba" + Presed + "; color: rgb(255, 255, 255); border: solid rgb" + PBC + ";}"
                          )

        if TT != "":
            cbtn.setToolTip(TT)

        cbtn.setIcon(qg.QIcon(IPath))

        return cbtn

    def Spinner(W, SType="Float", Pos=[0,0],  Width = 50, Height = 20, Range="(0, 100)", Value=0, Step=1, Suffix="", TT=""):

        SR = list(ast.literal_eval(Range))

        if SType == "Integer":

            spn = qg.QSpinBox(W)
            spn.move(Pos[0], Pos[1])

            spn.setRange(SR[0], SR[1])

            spn.setValue(Value)
            spn.setSingleStep(Step)
            spn.setSuffix(Suffix)

            if TT != "":
                spn.setToolTip(TT)

        if SType == "Float":

            spn = qg.QDoubleSpinBox(W)
            spn.move(Pos[0], Pos[1])

            spn.setRange(SR[0], SR[1])

            spn.setValue(Value)
            spn.setSingleStep(Step)
            spn.setSuffix(Suffix)

            if TT != "":
                spn.setToolTip(TT)

        spn.setFixedWidth(Width)
        spn.setFixedHeight(Height)

        return spn

    def CheckBox(W, Name="", Pos=[0,0], State=False, TT=""):

        cb = qg.QCheckBox(Name, W)
        cb.move(Pos[0], Pos[1])

        if State == True:
            cb.toggle()

        if TT != "":
            cb.setToolTip(TT)

        return cb

    def Label(W, Text="", Pos=[0,0]):
        lbl = qg.QLabel(W)
        lbl.move(Pos[0], Pos[1])
        lbl.setText(Text)

        return lbl

    def TextBox(W, Text="", Pos=[0,0], Width=100, Height=20):

        tb = qg.QLineEdit(W)
        tb.move(Pos[0], Pos[1])
        tb.setText(Text)
        tb.setFixedWidth(Width)
        tb.setFixedHeight(Height)

        return tb

    def ListBox(W, Pos=[0,0], Width=100, Height=100):
        lb = qg.QListWidget(W)
        lb.move(Pos[0], Pos[1])
        lb.setFixedWidth(Width)
        lb.setFixedHeight(Height)

        return lb

    def GroupeBox(W, Name="", Pos=[0,0],Width=100, Height=100):
        gb = qg.QGroupBox(Name, W)
        gb.move(Pos[0], Pos[1])
        gb.setFixedWidth(Width)
        gb.setFixedHeight(Height)

        return gb
































































