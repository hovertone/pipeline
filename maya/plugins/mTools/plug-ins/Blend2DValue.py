import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math

class Blend2DValue(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x70c03ea0)

    aInput_X = OpenMaya.MObject()
    aInput_Y = OpenMaya.MObject()

    aX_Maximum_Value = OpenMaya.MObject()
    aY_Maximum_Value = OpenMaya.MObject()

    aUse_X_Negative_Value = OpenMaya.MObject()
    aUse_Y_Negative_Value = OpenMaya.MObject()

    """-----------------------"""
    aOutput_X = OpenMaya.MObject()

    aOutput_X_Value_1 = OpenMaya.MObject()
    aOutput_X_Value_2 = OpenMaya.MObject()

    """-----------------------"""

    aOutput_Y = OpenMaya.MObject()

    aOutput_Y_Value_1 = OpenMaya.MObject()
    aOutput_Y_Value_2 = OpenMaya.MObject()

    """-----------------------"""

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data):
        Input_X = data.inputValue(self.aInput_X).asFloat()
        Input_Y = data.inputValue(self.aInput_Y).asFloat()

        X_Maximum = data.inputValue(self.aX_Maximum_Value).asFloat()
        Y_Maximum = data.inputValue(self.aY_Maximum_Value).asFloat()

        Use_X_Negative_Value = data.inputValue(self.aUse_X_Negative_Value).asBool()
        Use_Y_Negative_Value = data.inputValue(self.aUse_Y_Negative_Value).asBool()

        X_1 = 0
        X_2 = 0
        Y_1 = 0
        Y_2 = 0

        if Input_X > 0:
            if Input_X != 0:
                if Input_X > X_Maximum:
                    X_1 = X_Maximum
                else:
                    X_1 = 1/(X_Maximum/Input_X)
        else:
            if Use_X_Negative_Value == 1:
                if Input_X != 0:
                    Input_X = Input_X * -1

                    if Input_X > X_Maximum:
                        X_2 = X_Maximum
                    else:
                        X_2 = 1 / (X_Maximum / Input_X)

        if Input_Y > 0:
            if Input_Y != 0:
                if Input_Y > Y_Maximum:
                    Y_1 = Y_Maximum
                else:
                    Y_1 = 1/(Y_Maximum/Input_Y)
        else:
            if Use_Y_Negative_Value == 1:
                if Input_Y != 0:
                    Input_Y = Input_Y * -1

                    if Input_Y > Y_Maximum:
                        Y_2 = Y_Maximum
                    else:
                        Y_2 = 1 / (Y_Maximum / Input_Y)

        Output_X_Value_1 = data.outputValue(Blend2DValue.aOutput_X_Value_1)
        Output_X_Value_1.setFloat(X_1)
        Output_X_Value_1.setClean()

        Output_X_Value_2 = data.outputValue(Blend2DValue.aOutput_X_Value_2)
        Output_X_Value_2.setFloat(X_2)
        Output_X_Value_2.setClean()

        Output_Y_Value_1 = data.outputValue(Blend2DValue.aOutput_Y_Value_1)
        Output_Y_Value_1.setFloat(Y_1)
        Output_Y_Value_1.setClean()

        Output_Y_Value_2 = data.outputValue(Blend2DValue.aOutput_Y_Value_2)
        Output_Y_Value_2.setFloat(Y_2)
        Output_Y_Value_2.setClean()

        data.setClean(plug)

def creator():
    return OpenMayaMPx.asMPxPtr(Blend2DValue())

def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()

    Blend2DValue.aInput_X = nAttr.create('Input_X', 'Input_X', OpenMaya.MFnNumericData.kFloat, 0)
    nAttr.setKeyable(True)
    Blend2DValue.addAttribute(Blend2DValue.aInput_X)

    Blend2DValue.aInput_Y = nAttr.create('Input_Y', 'Input_Y', OpenMaya.MFnNumericData.kFloat, 0)
    nAttr.setKeyable(True)
    Blend2DValue.addAttribute(Blend2DValue.aInput_Y)

    """----------------------------------------------------------------------------------------"""

    Blend2DValue.aY_Maximum_Value = nAttr.create('Maximum_Y', 'Maximum_Y', OpenMaya.MFnNumericData.kFloat, 1)
    nAttr.setMin(0)
    nAttr.setKeyable(True)
    Blend2DValue.addAttribute(Blend2DValue.aY_Maximum_Value)

    Blend2DValue.aX_Maximum_Value = nAttr.create('Maximum_X', 'Maximum_X', OpenMaya.MFnNumericData.kFloat, 1)
    nAttr.setMin(0)
    nAttr.setKeyable(True)
    Blend2DValue.addAttribute(Blend2DValue.aX_Maximum_Value)

    """----------------------------------------------------------------------------------------"""

    Blend2DValue.aUse_Y_Negative_Value = nAttr.create('Use_Y_Negative', 'Use_Y_Negative', OpenMaya.MFnNumericData.kBoolean, 1)
    nAttr.setKeyable(True)
    Blend2DValue.addAttribute(Blend2DValue.aUse_Y_Negative_Value)

    Blend2DValue.aUse_X_Negative_Value = nAttr.create('Use_X_Negative', 'Use_X_Negative',
                                                      OpenMaya.MFnNumericData.kBoolean, 1)
    nAttr.setKeyable(True)
    Blend2DValue.addAttribute(Blend2DValue.aUse_X_Negative_Value)

    """----------------------------------------------------------------------------------------"""

    Blend2DValue.aOutput_X_Value_1 = nAttr.create('Value_X_1', 'Value_X_1', OpenMaya.MFnNumericData.kFloat)
    Blend2DValue.addAttribute(Blend2DValue.aOutput_X_Value_1)

    Blend2DValue.aOutput_X_Value_2 = nAttr.create('Value_X_2', 'Value_X_2', OpenMaya.MFnNumericData.kFloat)
    Blend2DValue.addAttribute(Blend2DValue.aOutput_X_Value_2)

    Blend2DValue.aOutput_X = nAttr.create("Output_X", "Output_X", Blend2DValue.aOutput_X_Value_1, Blend2DValue.aOutput_X_Value_2)
    Blend2DValue.addAttribute(Blend2DValue.aOutput_X)

    """----------------------------------------------------------------------------------------"""

    Blend2DValue.aOutput_Y_Value_1 = nAttr.create('Value_Y_1', 'Value_Y_1', OpenMaya.MFnNumericData.kFloat)
    Blend2DValue.addAttribute(Blend2DValue.aOutput_Y_Value_1)

    Blend2DValue.aOutput_Y_Value_2 = nAttr.create('Value_Y_2', 'Value_Y_2', OpenMaya.MFnNumericData.kFloat)
    Blend2DValue.addAttribute(Blend2DValue.aOutput_Y_Value_2)

    Blend2DValue.aOutput_Y = nAttr.create("Output_Y", "Output_Y", Blend2DValue.aOutput_Y_Value_1, Blend2DValue.aOutput_Y_Value_2)
    Blend2DValue.addAttribute(Blend2DValue.aOutput_Y)

    '''------------------------------------------------------------------------------------------------'''

    Blend2DValue.attributeAffects(Blend2DValue.aInput_X, Blend2DValue.aOutput_X)
    Blend2DValue.attributeAffects(Blend2DValue.aInput_Y, Blend2DValue.aOutput_Y)

    Blend2DValue.attributeAffects(Blend2DValue.aX_Maximum_Value, Blend2DValue.aOutput_X)
    Blend2DValue.attributeAffects(Blend2DValue.aY_Maximum_Value, Blend2DValue.aOutput_Y)

    Blend2DValue.attributeAffects(Blend2DValue.aUse_X_Negative_Value, Blend2DValue.aOutput_X)
    Blend2DValue.attributeAffects(Blend2DValue.aUse_Y_Negative_Value, Blend2DValue.aOutput_Y)

    '''------------------------------------------------------------------------------------------------'''

def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, "Maxim Vodolazskiy", "1.0", "Any")
    plugin.registerNode("Blend2DValue", Blend2DValue.kPluginNodeId, creator, initialize)

def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    plugin.deregisterNode(Blend2DValue.kPluginNodeId)