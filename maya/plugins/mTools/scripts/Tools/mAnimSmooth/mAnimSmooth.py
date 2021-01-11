import MUI.MaxUI as mui
reload (mui)
import PySide2.QtGui as qg
import PySide2.QtCore as qc
import PySide2.QtWidgets as qw
import maya.cmds as cmds

class BlurCurve(qw.QDialog):

    def __init__(self):
        qw.QDialog.__init__(self)

        mui.Window(W=self, Titel="Blur", Width=150, Height=75)
        
        mui.Label(W=self, Text="Amount:", Pos=[5,8])
        
        self.Am = mui.Spinner(W=self, Pos=[70, 5], Width=75, Value=1, Range="(0, 1.0)", Step=0.1)

        mui.Label(W=self, Text="Interations:", Pos=[5,28])
        
        self.Int = mui.Spinner(W=self, SType="Integer", Pos=[70, 25], Width=75, Value=2)
        
        self.DoBtn1 = mui.Button(W=self, Name = "Smooth", Pos=[5, 50], Width=140, Height=20)

        self.DoBtn1.clicked.connect(self.btnBlur)
        
    def blur(self, array, index):
        count = len(array)
        prev = index - 1
        next = index + 1
        
        if prev < 0:
            prev = index
            
        if next > (count-1):
            next = index
            
        pVal = array[prev]
        nVal = array[next]
        Val = array[index]
        
        aVal = (pVal + nVal + Val) /3
        bVal = aVal * self.Am.value() + Val * (1 - self.Am.value())
        
        return bVal
        
    def btnBlur(self):
        cmds.undoInfo(openChunk = True)
        selCurve = cmds.keyframe(q=True, name=True)
        
        for cur in range(len(selCurve)):
            animCurve = selCurve[cur] #get animation curve
            
            selFrames = cmds.keyframe(animCurve, q=True, sl=True, timeChange=True) #selected Frames
            selKeysValues = cmds.keyframe(animCurve, q=True, sl=True, valueChange=True) #selected Keys
            
            selKeysCount = len(selKeysValues)
            tempArray = selKeysValues
            
            for int in range(self.Int.value()):
                for i in range(selKeysCount):
                    if i != 0 and i != (selKeysCount - 1):
                        tempArray[i] = self.blur(tempArray, i)
                    
            for i in range(selKeysCount):
                frame = selFrames[i]
                cmds.keyframe(animCurve, edit=True, absolute=True, valueChange=tempArray[i], time=(frame,frame)) 
                 
        cmds.undoInfo(closeChunk = True)

BlurCurve_Dialog = BlurCurve()
BlurCurve_Dialog.show()