import os
import maya.cmds as cmds
import random
import re
import shutil
import datetime
import functools

def createUI(pWindowTitle, pApplyCallback):
    windowID = 'assetDailyMaker'

    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    cmds.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True)
    cmds.columnLayout(adj=True)

    drive = 'P:'
    scriptPath = cmds.file(query=True, sn=True)
    project = scriptPath.split('/')[1]
    scriptName = os.path.split(scriptPath)[-1]
    match = re.match(r'(\w*)_(\w*)_v(\d*)', scriptName)
    if not match:
        print 'invalid scene name.1'
        cmds.deleteUI('assetDailyMaker')
        return
    else:
        assetName = match.group(1)
        valueField = cmds.textFieldGrp(l="Asset Name:", editable=True, text=assetName)

        okOptions = ['YES!', 'Tochnayak', 'To chto nado', 'Ebash!', 'Segodnya mne povezet']
        cmds.button(label=okOptions[random.randrange(len(okOptions))], command=functools.partial(pApplyCallback, valueField))

        def cancelCallback(*pArgs):
            if cmds.window(windowID, exists=True):
                cmds.deleteUI(windowID)

        cmds.button(label='Cancel', command=cancelCallback)
        cmds.showWindow()

def applyCallback(pValueField, *pArgs):
    #print 'Apply button pressed.'
    value = cmds.textFieldGrp(pValueField, q=True, text=True)
    #print 'value: %s' % (value)

    cmds.deleteUI('assetDailyMaker')
    proceedToMov(value)

def proceedToMov(pValue):
    drive = 'P:'
    scriptPath = cmds.file(query=True, sn=True)
    project = scriptPath.split('/')[1]
    scriptName = os.path.split(scriptPath)[-1]
    match = re.match(r'(\w*)_(\w*)_v(\d*)', scriptName)
    if not match:
        print 'invalid scene name.2'
    else:
        assetNameNew = pValue
        assetNameOrig = match.group(1)
        user = match.group(2)
        ver = int(match.group(3))#
        # print 'project: %s\tscriptName: %s\tAssetname: %s\tuser: %s\tver: %s' % (project, scriptName, assetName, user, ver)

        dailiesPath = '%s/%s/assetBuilds/char/%s/dailies/%s_%s_v%s' % (drive, project, assetNameOrig, assetNameNew, user, str(ver).zfill(3))
        now = datetime.datetime.now().strftime("%y%m%d")
        ftrackPath = '%s/%s/dailies/%s/DAILIES_%s' % (drive, project, now, assetNameNew)

        for i in (dailiesPath, ftrackPath):
            print i
            if not os.path.exists(os.path.dirname(i)):
                # os.makedirs(os.path.dirname(i))
                print '%s folder created' % os.path.dirname(i)

        # MOVIE CREATION PART. MAKE ONE INTO ASSET DAILIES. AND THEN COPY IT'S TO A ROOT PROJECT FOLDER
        try:
            cmds.playblast(f=dailiesPath, format='qt', percent=100, quality=90, width=1280, height=720)
            shutil.copy2(dailiesPath + '.mov', ftrackPath + '.mov')
            print dailiesPath + '.mov'
        except:
            print 'SANEK NAPISAL KAKAYU-TO HUJNYU V CODE)))'

#createUI('Make Asset Daily', applyCallback)
#assetDailies.createUI('Make Daily', assetDailies.applyCallback)