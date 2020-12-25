# bake a Childs t,r,s values to world Coordinates
# compatible with Maya 2012-2014
# version 1.8
# Steffen Richter
# copyright 2013 //all Rights reserved
# www.richter-steffen.com

import maya.cmds as cmds
import random
import functools

def createUI(pApplyCallback, renameTo):
    # if not getPipelineAttrs():
    #     cmds.deleteUI('framesToBake')
    #     cmds.confirmDialog(message='Not a pipeline scene.')
    #     return
    # else:
    #     drive, project, seq, shot, version = getPipelineAttrs()
    selObj = cmds.ls(sl=True)

    # Check if an object is selected
    if selObj == []:
        cmds.confirmDialog(t='Warning!', message='Please Select min. one Child Object', ds='ok', icn='information')
        return

    start = int(cmds.playbackOptions(q=True, min=True))
    end = int(cmds.playbackOptions(q=True, max=True))

    windowID = 'framesToBake'

    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    cmds.window(windowID, title='Set Frames', height=50, width=50, resizeToFitChildren=True, sizeable=False)
    cmds.columnLayout(adj=True, width=400)

    valueField = cmds.textFieldGrp(l="Frames to Bake:", editable=True, text='%s - %s' % (start, end))

    okOptions = ['YES!', 'Tochnayak', 'To chto nado', 'Ebash!', 'Segodnya mne povezet']
    cmds.button(label=okOptions[random.randrange(len(okOptions))], command=functools.partial(pApplyCallback, valueField, renameTo))

    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)

    cmds.button(label='Cancel', command=cancelCallback)
    cmds.showWindow()

def applyCallback(pValueField, renameTo, *pArgs):
    value = cmds.textFieldGrp(pValueField, q=True, text=True)

    cmds.deleteUI('framesToBake')
    camBake(value, renameTo)

def camBake():
    #cmds.confirmDialog(message='%s, %s' % (value, renameTo))

    renameTo = 'cam1'
    selObj = cmds.ls(sl=True)
    bakeList = []
    for n in selObj:

        # check if selected object is a child of an object
        par = cmds.listRelatives(n, parent=True)
        if par == None:
            cmds.confirmDialog(t='Warning!', message='%s has no Parent Object' % n, ds='ok', icn='information')

        else:
            # Delete old camera if it exists
            if cmds.objExists(renameTo): cmds.delete(renameTo)
            # duplicate object
            duplObj = cmds.duplicate(n, name=renameTo, rc=True, rr=True, un=True)

            #delete image planes if they exists

            # delete doublicated children
            childrenTd = cmds.listRelatives(duplObj, c=True, pa=True)[1:]
            for c in childrenTd:
                cmds.delete(c)
            # unparent object,add constraints and append it to bake List
            toBake = cmds.parent(duplObj, w=True)
            bakeList.append(toBake)
            cmds.parentConstraint(n, toBake, mo=False)
            try:
                cmds.scaleConstraint(n, toBake, mo=False)
            except:
                print 'Scale constraint has not been assigned.'

    # get Start and End Frame of Time Slider
    startFrame = cmds.playbackOptions(q=True, minTime=True)
    endFrame = cmds.playbackOptions(q=True, maxTime=True)

    # bake Animation and delete Constraints

    for i in bakeList:
        cmds.bakeResults(i, t=(startFrame, endFrame))
        cmds.delete(i[0] + '*Constraint*')

        # make sure that key tangents are spline on every key of every animated curve
        animAttributes = cmds.listAnimatable(i)
        for attr in animAttributes:
            numKeyframes = cmds.keyframe(attr, query=True, keyframeCount=True)
            if numKeyframes > 0:
                times = cmds.keyframe(attr, query=True, index=(0, numKeyframes), timeChange=True)
                for k in times:
                    cmds.keyTangent(i, attribute=attr, inTangentType='spline', outTangentType='spline',
                                    time=(int(k), int(k)))



    return renameTo