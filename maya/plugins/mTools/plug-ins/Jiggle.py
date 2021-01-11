import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math


class JigglePoint(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x3e64d7d9)

    aOutput = OpenMaya.MObject()
    aToggle = OpenMaya.MObject()
    aGoal = OpenMaya.MObject()
    aJiggleAmount = OpenMaya.MObject()
    aDamping = OpenMaya.MObject()
    aStiffness = OpenMaya.MObject()
    aTime = OpenMaya.MObject()
    aParentInverse = OpenMaya.MObject()
    aUseDis = OpenMaya.MObject()
    aDistance = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        self._initialized = False
        self._currentPosition = OpenMaya.MPoint()
        self._previousPosition = OpenMaya.MPoint()
        self._previousTime = OpenMaya.MTime()

    def compute(self, plug, data):
        if plug != JigglePoint.aOutput:
            return OpenMaya.kUnknownParameter

        Toggle = data.inputValue(self.aToggle).asBool()
        goal = OpenMaya.MPoint(data.inputValue(self.aGoal).asFloatVector())
        jiggleAmount = data.inputValue(self.aJiggleAmount).asFloat()
        damping = data.inputValue(self.aDamping).asFloat()
        stiffness = data.inputValue(self.aStiffness).asFloat()
        currentTime = data.inputValue(self.aTime).asTime()
        parrentInverse = data.inputValue(self.aParentInverse).asMatrix()
        UseDis = data.inputValue(self.aUseDis).asBool()
        Distance = data.inputValue(self.aDistance).asFloat()

        if not self._initialized:
            self._previousTime = currentTime
            self._currentPosition = goal
            self._previousPosition = goal
            self._initialized = True

        timeDifference = currentTime.value() - self._previousTime.value()

        if timeDifference > 1.0 or timeDifference < 0.0:
            self._initialized = False
            self._previousTime = currentTime
            data.setClean(plug)
            return

        if Toggle == True:
            velocity = (self._currentPosition - self._previousPosition) * (1.0 - damping)
            newPosition = self._currentPosition + velocity
            goalForce = (goal - newPosition) * stiffness
            newPosition += goalForce

            if UseDis == 1:
                CurrrentDistance = goal.distanceTo(newPosition)
                Direction = (newPosition - goal).normal()

                if CurrrentDistance > Distance:
                    ComputePosition = goal + Direction * Distance
                else:
                    ComputePosition = newPosition
            else:
                ComputePosition = newPosition

            self._previousPosition = OpenMaya.MPoint(self._currentPosition)
            self._currentPosition = OpenMaya.MPoint(ComputePosition)
            self._previousTime = OpenMaya.MTime(currentTime)

            ComputePosition = goal + ((ComputePosition - goal) * jiggleAmount)

            ComputePosition *= parrentInverse
        else:
            ZPosition = OpenMaya.MVector(0, 0, 0)

            self._previousPosition = OpenMaya.MPoint(goal)
            self._currentPosition = OpenMaya.MPoint(goal)
            self._previousTime = OpenMaya.MTime(currentTime)

            ComputePosition = ZPosition * parrentInverse

        hOutput = data.outputValue(JigglePoint.aOutput)
        outVector = OpenMaya.MFloatVector(ComputePosition.x, ComputePosition.y, ComputePosition.z)
        hOutput.setMFloatVector(outVector)
        hOutput.setClean()
        data.setClean(plug)

def creator():
    return OpenMayaMPx.asMPxPtr(JigglePoint())

def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    uAttr = OpenMaya.MFnUnitAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    JigglePoint.aOutput = nAttr.createPoint("output", "out")
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    JigglePoint.addAttribute(JigglePoint.aOutput)

    JigglePoint.aGoal = nAttr.createPoint("goal", "goal")
    JigglePoint.addAttribute(JigglePoint.aGoal)
    JigglePoint.attributeAffects(JigglePoint.aGoal, JigglePoint.aOutput)

    JigglePoint.aToggle = nAttr.create("toggle", "toggle", OpenMaya.MFnNumericData.kBoolean, 1)
    nAttr.setKeyable(True)
    JigglePoint.addAttribute(JigglePoint.aToggle)
    JigglePoint.attributeAffects(JigglePoint.aToggle, JigglePoint.aOutput)

    JigglePoint.aJiggleAmount = nAttr.create("jiggle", "jiggle", OpenMaya.MFnNumericData.kFloat, 1.0)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    JigglePoint.addAttribute(JigglePoint.aJiggleAmount)
    JigglePoint.attributeAffects(JigglePoint.aJiggleAmount, JigglePoint.aOutput)

    JigglePoint.aStiffness = nAttr.create("stiffness", "stiffness", OpenMaya.MFnNumericData.kFloat, 1.0)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    JigglePoint.addAttribute(JigglePoint.aStiffness)
    JigglePoint.attributeAffects(JigglePoint.aStiffness, JigglePoint.aOutput)

    JigglePoint.aDamping = nAttr.create("damping", "damping", OpenMaya.MFnNumericData.kFloat, 1.0)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    JigglePoint.addAttribute(JigglePoint.aDamping)
    JigglePoint.attributeAffects(JigglePoint.aDamping, JigglePoint.aOutput)

    JigglePoint.aUseDis = nAttr.create("useDistance", "useDistance", OpenMaya.MFnNumericData.kBoolean, 0)
    nAttr.setKeyable(True)
    JigglePoint.addAttribute(JigglePoint.aUseDis)
    JigglePoint.attributeAffects(JigglePoint.aUseDis, JigglePoint.aOutput)

    JigglePoint.aDistance = nAttr.create("distance", "distance", OpenMaya.MFnNumericData.kFloat, 1.0)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    JigglePoint.addAttribute(JigglePoint.aDistance)
    JigglePoint.attributeAffects(JigglePoint.aDistance, JigglePoint.aOutput)

    JigglePoint.aTime = uAttr.create("time", "time", OpenMaya.MFnUnitAttribute.kTime, 0.0)
    JigglePoint.addAttribute(JigglePoint.aTime)
    JigglePoint.attributeAffects(JigglePoint.aTime, JigglePoint.aOutput)

    JigglePoint.aParentInverse = mAttr.create("parentInverse", "parentInverse")
    JigglePoint.addAttribute(JigglePoint.aParentInverse)

def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, "Maxim Vodolazskiy", "1.0", "Any")
    plugin.registerNode("JigglePoint", JigglePoint.kPluginNodeId, creator, initialize)

def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    plugin.deregisterNode(JigglePoint.kPluginNodeId)