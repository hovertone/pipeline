import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math

class AnglePlusAngle(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x21827db8)

    aInpyt_Angle_A_Mult = OpenMaya.MObject()

    aInpyt_Angle_A = OpenMaya.MObject()

    aInput_Angle_A_X = OpenMaya.MObject()
    aInput_Angle_A_Y = OpenMaya.MObject()
    aInput_Angle_A_Z = OpenMaya.MObject()

    '''-------------------------------'''

    aInpyt_Angle_B_Mult = OpenMaya.MObject()

    aInpyt_Angle_B = OpenMaya.MObject()

    aInput_Angle_B_X = OpenMaya.MObject()
    aInput_Angle_B_Y = OpenMaya.MObject()
    aInput_Angle_B_Z = OpenMaya.MObject()

    '''-------------------------------'''

    aOutput_Angle = OpenMaya.MObject()

    aOutput_AngleX = OpenMaya.MObject()
    aOutput_AngleY = OpenMaya.MObject()
    aOutput_AngleZ = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data):
        A_Mult = data.inputValue(self.aInpyt_Angle_A_Mult).asFloat()
        In_A_X = (data.inputValue(self.aInput_Angle_A_X).asAngle()).asDegrees()
        In_A_Y = (data.inputValue(self.aInput_Angle_A_Y).asAngle()).asDegrees()
        In_A_Z = (data.inputValue(self.aInput_Angle_A_Z).asAngle()).asDegrees()

        B_Mult = data.inputValue(self.aInpyt_Angle_B_Mult).asFloat()
        In_B_X = (data.inputValue(self.aInput_Angle_B_X).asAngle()).asDegrees()
        In_B_Y = (data.inputValue(self.aInput_Angle_B_Y).asAngle()).asDegrees()
        In_B_Z = (data.inputValue(self.aInput_Angle_B_Z).asAngle()).asDegrees()

        Pi = 3.14

        Out_X = Pi * (In_A_X*A_Mult + In_B_X*B_Mult) / 180.0
        Out_Y = Pi * (In_A_Y*A_Mult + In_B_Y*B_Mult) / 180.0
        Out_Z = Pi * (In_A_Z*A_Mult + In_B_Z*B_Mult) / 180.0

        OutputX = data.outputValue(AnglePlusAngle.aOutput_AngleX)
        OutputY = data.outputValue(AnglePlusAngle.aOutput_AngleY)
        OutputZ = data.outputValue(AnglePlusAngle.aOutput_AngleZ)
        OutputX.setMAngle(OpenMaya.MAngle(Out_X))
        OutputY.setMAngle(OpenMaya.MAngle(Out_Y))
        OutputZ.setMAngle(OpenMaya.MAngle(Out_Z))
        OutputX.setClean()
        OutputY.setClean()
        OutputZ.setClean()
        data.setClean(plug)

def creator():
    return OpenMayaMPx.asMPxPtr(AnglePlusAngle())

def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    uAttr = OpenMaya.MFnUnitAttribute()
    #cAttr = OpenMaya.MFnCompoundAttribute()

    '''------------------------------------------------------------------------------------------------'''

    AnglePlusAngle.aInpyt_Angle_A_Mult = nAttr.create("Multiplier_A", "Multiplier_A", OpenMaya.MFnNumericData.kFloat, 1)
    nAttr.setKeyable(True)
    nAttr.setMin(-1)
    nAttr.setMax(1)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aInpyt_Angle_A_Mult)

    AnglePlusAngle.aInput_Angle_A_X = uAttr.create("Rotate_A_X", "Rotate_A_X", OpenMaya.MFnUnitAttribute.kAngle, 0)
    uAttr.setKeyable(True)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aInput_Angle_A_X)

    AnglePlusAngle.aInput_Angle_A_Y = uAttr.create("Rotate_A_Y", "Rotate_A_Y", OpenMaya.MFnUnitAttribute.kAngle, 0)
    uAttr.setKeyable(True)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aInput_Angle_A_Y)

    AnglePlusAngle.aInput_Angle_A_Z = uAttr.create("Rotate_A_Z", "Rotate_A_Z", OpenMaya.MFnUnitAttribute.kAngle, 0)
    uAttr.setKeyable(True)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aInput_Angle_A_Z)

    AnglePlusAngle.aInpyt_Angle_A = nAttr.create("Rotate_A", "Rotate_A", AnglePlusAngle.aInput_Angle_A_X, AnglePlusAngle.aInput_Angle_A_Y, AnglePlusAngle.aInput_Angle_A_Z)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aInpyt_Angle_A)

    '''------------------------------------------------------------------------------------------------'''

    AnglePlusAngle.aInpyt_Angle_B_Mult = nAttr.create("Multiplier_B", "Multiplier_B", OpenMaya.MFnNumericData.kFloat, 1)
    nAttr.setKeyable(True)
    nAttr.setMin(-1)
    nAttr.setMax(1)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aInpyt_Angle_B_Mult)

    AnglePlusAngle.aInput_Angle_B_X = uAttr.create("Rotate_B_X", "Rotate_B_X", OpenMaya.MFnUnitAttribute.kAngle, 0)
    uAttr.setKeyable(True)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aInput_Angle_B_X)

    AnglePlusAngle.aInput_Angle_B_Y = uAttr.create("Rotate_B_Y", "Rotate_B_Y", OpenMaya.MFnUnitAttribute.kAngle, 0)
    uAttr.setKeyable(True)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aInput_Angle_B_Y)

    AnglePlusAngle.aInput_Angle_B_Z = uAttr.create("Rotate_B_Z", "Rotate_B_Z", OpenMaya.MFnUnitAttribute.kAngle, 0)
    uAttr.setKeyable(True)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aInput_Angle_B_Z)

    AnglePlusAngle.aInpyt_Angle_B = nAttr.create("Rotate_B", "Rotate_B", AnglePlusAngle.aInput_Angle_B_X, AnglePlusAngle.aInput_Angle_B_Y, AnglePlusAngle.aInput_Angle_B_Z)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aInpyt_Angle_B)

    '''------------------------------------------------------------------------------------------------'''

    AnglePlusAngle.aOutput_AngleX = uAttr.create("Output_X", "Output_X", OpenMaya.MFnUnitAttribute.kAngle)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aOutput_AngleX)

    AnglePlusAngle.aOutput_AngleY = uAttr.create("Output_Y", "Output_Y", OpenMaya.MFnUnitAttribute.kAngle)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aOutput_AngleY)

    AnglePlusAngle.aOutput_AngleZ = uAttr.create("Output_Z", "Output_Z", OpenMaya.MFnUnitAttribute.kAngle)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aOutput_AngleZ)

    AnglePlusAngle.aOutput_Angle = nAttr.create("Output", "Output", AnglePlusAngle.aOutput_AngleX, AnglePlusAngle.aOutput_AngleY, AnglePlusAngle.aOutput_AngleZ)
    AnglePlusAngle.addAttribute(AnglePlusAngle.aOutput_Angle)

    '''------------------------------------------------------------------------------------------------'''

    AnglePlusAngle.attributeAffects(AnglePlusAngle.aInput_Angle_A_X, AnglePlusAngle.aOutput_AngleX)
    AnglePlusAngle.attributeAffects(AnglePlusAngle.aInput_Angle_A_Y, AnglePlusAngle.aOutput_AngleY)
    AnglePlusAngle.attributeAffects(AnglePlusAngle.aInput_Angle_A_Z, AnglePlusAngle.aOutput_AngleZ)

    AnglePlusAngle.attributeAffects(AnglePlusAngle.aInput_Angle_B_X, AnglePlusAngle.aOutput_AngleX)
    AnglePlusAngle.attributeAffects(AnglePlusAngle.aInput_Angle_B_Y, AnglePlusAngle.aOutput_AngleY)
    AnglePlusAngle.attributeAffects(AnglePlusAngle.aInput_Angle_B_Z, AnglePlusAngle.aOutput_AngleZ)

    AnglePlusAngle.attributeAffects(AnglePlusAngle.aInpyt_Angle_A_Mult, AnglePlusAngle.aOutput_AngleX)
    AnglePlusAngle.attributeAffects(AnglePlusAngle.aInpyt_Angle_A_Mult, AnglePlusAngle.aOutput_AngleY)
    AnglePlusAngle.attributeAffects(AnglePlusAngle.aInpyt_Angle_A_Mult, AnglePlusAngle.aOutput_AngleZ)

    AnglePlusAngle.attributeAffects(AnglePlusAngle.aInpyt_Angle_B_Mult, AnglePlusAngle.aOutput_AngleX)
    AnglePlusAngle.attributeAffects(AnglePlusAngle.aInpyt_Angle_B_Mult, AnglePlusAngle.aOutput_AngleY)
    AnglePlusAngle.attributeAffects(AnglePlusAngle.aInpyt_Angle_B_Mult, AnglePlusAngle.aOutput_AngleZ)

    '''------------------------------------------------------------------------------------------------'''

def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, "Maxim Vodolazskiy", "1.0", "Any")
    plugin.registerNode("AnglePlusAngle", AnglePlusAngle.kPluginNodeId, creator, initialize)

def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    plugin.deregisterNode(AnglePlusAngle.kPluginNodeId)