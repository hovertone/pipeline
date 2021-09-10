import os
import maya.cmds as cmds
import random
import re
import shutil
import datetime
import functools
import socket
import pymel.core as pm
import telega
import glob
from p_utils.csv_parser_bak import projectDict
from time import gmtime, strftime

def getCurrentCamera():
    '''
    Returns the camera that you're currently looking through.
    If the current highlighted panel isn't a modelPanel,
    '''

    panel = cmds.getPanel(withFocus=True)

    if cmds.getPanel(typeOf=panel) != 'modelPanel':
        # just get the first visible model panel we find, hopefully the correct one.
        for p in cmds.getPanel(visiblePanels=True):
            if cmds.getPanel(typeOf=p) == 'modelPanel':
                panel = p
                cmds.setFocus(panel)
                break

    if cmds.getPanel(typeOf=panel) != 'modelPanel':
        OpenMaya.MGlobal.displayWarning('Please highlight a camera viewport.')
        return False

    camShape = cmds.modelEditor(panel, query=True, camera=True)
    if not camShape:
        return False

    camNodeType = cmds.nodeType(camShape)
    if cmds.nodeType(camShape) == 'transform':
        return camShape
    elif cmds.nodeType(camShape) in ['camera', 'stereoRigCamera']:
        return cmds.listRelatives(camShape, parent=True, path=True)[0]

def getPipelineAttrs():
    print 'in get pipeline attrs222222'
    try:
        shotString = os.environ['SHOT'].replace('//', '/')
        print 'shot string assigned based on a os.environ variable'
    except:
        return None
    #print shotString.split('/')
    drive = shotString.split('/')[0]
    project = shotString.split('/')[1]
    seq = shotString.split('/')[-2]
    shot = shotString.split('/')[-1]

    scriptPath = cmds.file(query=True, sn=True)
    scriptName = os.path.split(scriptPath)[-1]#.replace('-', '') # BARONOV NAMING FIX

    match = re.match(r'(\w*)_(\w*)_v(\d*)', scriptName)
    try:
        version = int(match.group(3))
        return drive, project, seq, shot, version
    except AttributeError:
        cmds.confirmDialog(message='Scene naming error.')

def setPrePlaybackAttrs():
    users = {'gleb':'slivko gleb', 'sashok':'gamaiunov alexander', 'jenya':'deshevij zhekan', 'Andrew-PC':'baronov andrey'}
    if cmds.objExists('zshotmask'):
        drive, project, seq, shot, version = getPipelineAttrs()
        # at first make all fields empty
        try:
            for i in ['tlt', 'tct', 'trt', 'bct', 'brt']:
                cmds.setAttr('zshotmask_shape.%s' % i, '', type='string')
            # fill shot field at bottom left
            cmds.setAttr('zshotmask_shape.blt', '%s v%s' % (shot, str(version).zfill(3)), type='string')
            # if user name is in the system - fill the top left field with user name
            #hostname = socket.gethostname()
            #if hostname.lower() in users.keys():
            #    cmds.setAttr('zshotmask_shape.tlt', users[hostname.lower()], type='string')

            cmds.setAttr('zshotmask_shape.fontScale', 0.6)
            cmds.setAttr('zshotmask_shape.fontColorR', 0.2)
            cmds.setAttr('zshotmask_shape.fontColorG', 0.2)
            cmds.setAttr('zshotmask_shape.fontColorB', 0.2)
            cmds.setAttr('zshotmask_shape.fn', 'Sylfaen', type='string')
            cmds.setAttr('zshotmask_shape.ba', 0.2)
        except:
            pass
    else:
        print 'ERROR :: no slate object in the scene'

    try:
        #panel = cmds.getPanel(withFocus=True)
        #camera = cmds.modelPanel(panel, query=True, camera=True)
        camera = getCurrentCamera()
        cam_shp = cmds.listRelatives(camera, type="camera")
        #print cam_shp
        if cam_shp:
            cmds.setAttr(cam_shp[0] + ".overscan", 1)
            # camera lens information to the top right corner
            cmds.setAttr('zshotmask_shape.trt', '%s mm' % (int(cmds.getAttr(cam_shp[0] + '.focalLength'))), type='string')
    except:
        print 'ERROR :: overscan has not been set.'

def createUI(pApplyCallback):
    if not getPipelineAttrs():
        cmds.deleteUI('previzToMontage')
        cmds.confirmDialog(message='Not a pipeline scene.')
        return
    else:
        drive, project, seq, shot, version = getPipelineAttrs()

    #start = int(cmds.playbackOptions(q=True, min=True)) + 1
    #end = int(cmds.playbackOptions(q=True, max=True)) - 1


    pd = projectDict(project)
    start = pd.getSpecificShotData(seq, shot, 'first_frame')
    end = pd.getSpecificShotData(seq, shot, 'last_frame')

    windowID = 'previzToMontage'

    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    cmds.window(windowID, title='Set Frames', height=50, width=50, resizeToFitChildren=True, sizeable=False)
    cmds.columnLayout(adj=True, width=400)

    valueField = cmds.textFieldGrp(l="Frames for Playblast:", editable=True, text='%s - %s' % (start, end))

    okOptions = ['YES!', 'Tochnayak', 'To chto nado', 'Ebash!', 'Segodnya mne povezet']
    cmds.button(label=okOptions[random.randrange(len(okOptions))], command=functools.partial(pApplyCallback, valueField))

    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)

    cmds.button(label='Cancel', command=cancelCallback)
    cmds.showWindow()

def applyCallback(pValueField, *pArgs):
    value = cmds.textFieldGrp(pValueField, q=True, text=True)

    cmds.deleteUI('previzToMontage')

    hwr = pm.PyNode("hardwareRenderingGlobals")
    hwr.multiSampleEnable.set(1)

    proceedToMov(value)

    hwr.multiSampleEnable.set(0)

def proceedToMov(pValue):
    start, end = pValue.strip(' ').split('-')
    setPrePlaybackAttrs()
    drive, project, seq, shot, version = getPipelineAttrs()

    curTime = strftime("%Y-%m-%d_%H-%M-%S", gmtime())

    shotPath = '%s/%s/sequences/%s/%s/out/allDailies/%s_previz_v%s_%s.mov' % (drive, project, seq, shot, shot, str(version).zfill(3), curTime )
    shotFtrackPath = '%s/%s/sequences/%s/%s/out/DAILIES_%s_previz.mov' % (drive, project, seq, shot, shot)
    previzMontagePath = '%s/%s/preproduction/previz/out/%s_v%s.mov' % (drive, project, shot, str(version).zfill(3))

    for i in (shotPath, shotFtrackPath, previzMontagePath):
        #print i
        if not os.path.exists(os.path.dirname(i)):
            os.makedirs(os.path.dirname(i))
            #print '%s folder created' % os.path.dirname(i)

    #SOUND
    if cmds.ls(type='audio') != []:
        sd = cmds.ls(type='audio')[-1]
        soundExists = True
        print 'SOUND IS %s' % sd
    else:
        soundExists = False
        print 'No audio nodes in scene. Playblasting without sound'

    # SOUND
    # soundFolder = '%s/%s/sequences/%s/%s/sound/' % (drive, project, seq, shot)
    # if os.path.exists(soundFolder):
    #     files = filter(os.path.isfile, glob.glob(soundFolder + "*.wav"))
    #     files.sort(key=lambda x: os.path.getmtime(x))
    #     lastSoundFile = files[-1].replace('\\', '/')
    # else:
    #     print 'There is no folder for sound'
    #     lastSoundFile = False

    if soundExists:
        cmds.playblast(f="C:/temp/preview.mov", format='qt', percent=100, quality=75, width=1920, height=1080, startTime=int(start), endTime=int(end), forceOverwrite=True, s=sd)
    else:
        cmds.playblast(f="C:/temp/preview.mov", format='qt', percent=100, quality=75, width=1920, height=1080, startTime = int(start), endTime = int(end), forceOverwrite=True)

    # print 'mpg ' + mpg
    # print 'lastSoundFile ' + str(lastSoundFile)
    # print 'start ' + start
    # print 'temp_mov ' + temp_mov
    # print 'shotPath ' + shotPath
    #
    # mpg = "X:/app/win/ffmpeg/bin/ffmpeg"
    #
    # if lastSoundFile:
    #     #if sound exists
    #     cmd = mpg + " -threads 8 -r 24 -i " + lastSoundFile + " -i C:/temp/preview.mov -threads 8 -y -r 24 -c:v libx264 -pix_fmt yuv420p -vf scale=1920:1080 -preset ultrafast -crf 30 " + shotPath
    # else:
    #     cmd = mpg + " -threads 8 -r 24 -i C:/temp/preview.mov -threads 8 -y -r 24 -c:v libx264 -pix_fmt yuv420p -vf scale=1920:1080 -preset ultrafast -crf 30 " + shotPath
    #

    #except:
    #cmds.confirmDialog(message='SANEK NAPISAL KAKAYU-TO HUJNYU V CODE)))')

#createUI('Set Frames', applyCallback)
#assetDailies.createUI('Make Daily', assetDailies.applyCallback)