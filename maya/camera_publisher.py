import maya.cmds as cmds
import maya.mel as mel
import os
import cam_bake
from p_utils.common_utils import getLastCamVersion
import  motionblurKeyframesBake #import addExtraKeys
from p_utils.csv_parser_bak import projectDict
from playblastWithRV import getPipelineAttrs
import telega
reload(telega)

reload(motionblurKeyframesBake)

# drive, project, seq, shot, ver = getPipelineAttrs()[1]
# config = projectDict(project)
# shot_data = config.getAllShotData(seq, shot)
# first = shot_data['first_frame']
# last = shot_data['last_frame']

def exportCamMaya():
    sel = cmds.ls(sl=True)

    if len(sel) > 1:
        cmds.confirmDialog(t='Warning!', message='Only one object should be selected', ds='ok', icn='information')
        return
    elif len(sel) == 0:
        cmds.confirmDialog(t='Warning!', message='Select atleast one camera', ds='ok', icn='information')
    else:
        #check if selected camera is a rig (inside some parent system) object
        par = cmds.listRelatives(sel[0], parent=True)
        # if par != None:
        #     print 'camera rig object'
        #     cam_bake.camBake()
        # else:
        #     print 'root level object selected'


        #if cmds.objExists('cam1') and cmds.objectType('%s|%s' % ('cam1', cmds.listRelatives('cam1')[0])) == 'camera':
        #cmds.select(sel[0])
        try:
            shotPath = os.environ['SHOT']
        except:
            cmds.confirmDialog(message='The scene is not in PIPELINE.')
            return

        drive, project, seq, shot, ver = getPipelineAttrs()
        #print drive, project, seq, shot, ver
        config = projectDict(project)
        shot_data = config.getAllShotData(seq, shot)
        first = shot_data['first_frame']
        last = shot_data['last_frame']

        res = motionblurKeyframesBake.addExtraKeys(int(first), int(last), objs=['cam1'])
        print 'addExtraKeys = %s' % res

        shot = os.path.split(shotPath)[-1]
        # print shot
        camFolder = "%s/cache/cam" % (shotPath)
        exportVersion = getLastCamVersion(camFolder) + 1
        filename = "%s/%s_cam_v%s.fbx" % (camFolder, shot, str(exportVersion).zfill(3))


        if not cmds.objExists("cam1.camVersion"):
            cmds.addAttr(longName='camVersion', shortName='cam_ver', attributeType='double', defaultValue=1)
        cmds.setAttr('cam1.camVersion', lock=0)
        cmds.setAttr('cam1.camVersion', exportVersion)
        cmds.setAttr('cam1.camVersion', lock=1)
        if not cmds.objExists("cam1.camFilepath"):
            cmds.addAttr(longName='camFilepath', shortName='cam_file_path', dataType='string')
        cmds.setAttr('cam1.camFilepath', lock=0)
        cmds.setAttr('cam1.camFilepath', filename, type='string')
        cmds.setAttr('cam1.camFilepath', lock=1)

        mel.eval(('FBXExport -f \"{}\" -s').format(filename))
        cmds.confirmDialog(message='Camera v%s exported successfully!' % str(exportVersion).zfill(3))

        telega.telegramReport(None, tp='cam', args=[str(exportVersion).zfill(3)])
        #else:
        #    cmds.confirmDialog(message='Shits happens. There is no camera in the scene called cam1')
        #    #print '%s exported successfully' % filename


def findPipelineCameraMaya():
    # TRYING TO FIND A PIPELINE CAMERA IN THE SCENE
    try:
        camName = u'cam1'
        cmds.select(camName)
        if cmds.objExists("%s.camVersion" % camName):
            return camName, cmds.getAttr('%s.camVersion' % camName)
    except:
        return None


def importCamMaya(camFolder, lastFBXVersion):
    importPath = '%s/%s_cam_v%s.fbx' % (camFolder, camFolder.split('/')[-3], str(lastFBXVersion).zfill(3))
    print importPath
    newCamImportList = cmds.file(importPath, i=True, rnn=True)
    print 'list %s' % newCamImportList
    newCam = [i for i in newCamImportList if 'translate' not in i and 'rotate' not in i and 'Shape' not in i and 'scale' not in i]
    print 'newcam %s' % newCam

    newCamName = 'cam1'
    cmds.rename(newCam, newCamName)
    cmds.select(newCamName)

    if not cmds.objExists("%s.camVersion" % newCamName):
        cmds.addAttr(longName='camVersion', shortName='cam_ver', attributeType='double', defaultValue=1)
    cmds.setAttr('%s.camVersion' % newCamName, lock=0)
    cmds.setAttr('%s.camVersion' % newCamName, int(lastFBXVersion))
    cmds.setAttr('%s.camVersion' % newCamName, lock=1)
    if not cmds.objExists("%s.camFilepath" % newCamName):
        cmds.addAttr(longName='camFilepath', shortName='cam_file_path', dataType='string')
    cmds.setAttr('%s.camFilepath' % newCamName, lock=0)
    cmds.setAttr('%s.camFilepath' % newCamName, importPath, type='string')
    cmds.setAttr('%s.camFilepath' % newCamName, lock=1)

    group = cmds.group()
    cmds.rename(group, 'cam_group')


    #cmds.setAttr('%s.nearClipPlane' % (cmds.listRelatives(newCamName)[0]), 0.1)
    #cmds.setAttr('%s.farClipPlane' % (cmds.listRelatives(newCamName)[0]), 5000)

    # animPlatePath = '%s/src/animPlate/%s_animPlate.1001.jpg' % ('/'.join(camFolder.split('/')[:-2]), camFolder.split('/')[-3])
    # if os.path.exists(os.path.dirname(animPlatePath)):
    #     imagePlaneName = cmds.createNode("imagePlane")
    #     mel.eval('cameraImagePlaneUpdate "%s" "%s";' % (newCamName, imagePlaneName))
    #     cmds.setAttr("%s.imageName" % imagePlaneName, animPlatePath, type="string")
    #     cmds.setAttr("%s.useFrameExtension" % imagePlaneName, 1)
    #
    #     #print '13131231231' + animPlatePath
    #     #cam.parm('vm_background').set(animPlatePath)
    # else:
    #     print 'ERROR :: There is no folder with animPlates'

    cmds.confirmDialog(message='Successfully imported camera v%s' % str(lastFBXVersion).zfill(3))


def importLastCamVersionMaya(force = True):
    try:
        shotPath = os.environ['SHOT']
    except:
        cmds.confirmDialog(message='The scene is not in PIPELINE.')
        return
    shot = os.path.split(shotPath)[-1]
    camFolder = "%s/cache/cam" % (shotPath)
    lastFBXVersion = getLastCamVersion(camFolder)
    if findPipelineCameraMaya():
        # PIPELINE CAMERA EXISTS
        camName, ver = findPipelineCameraMaya()
        if lastFBXVersion > int(ver):
            # THERE IS NEW CAMERA VERSION
            if not force:
                if cmds.confirmDialog(button = ('Yes', 'No')) == 'Yes':
                    cmds.delete(camName)
                    importCamMaya(camFolder, lastFBXVersion)
                else:
                    pass
            else:
                cmds.delete(camName)
                importCamMaya(camFolder, lastFBXVersion)
        else:
            # THERE IS NO NEW CAMERA VERSION
            cmds.confirmDialog(message='You have the latest camera in the scene. Chill.')
    else:
        # THERE IS NO PIPELINE CAMERA IN THE SCENE
        # print 'no pipe camera in the scene'
        importCamMaya(camFolder, lastFBXVersion)


# exportCamMaya()
#importLastCamVersionMaya()