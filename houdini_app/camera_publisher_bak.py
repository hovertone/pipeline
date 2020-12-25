import os
import hou
import p_utils.common_utils
import cam_bake
import random
#import traceback
from p_utils import csv_parser_bak as parser
from houdini_app.Loader import loader_preferences as prefs


reload(cam_bake)
import recursiveInput


# def getLastCamVersion(path):
#     files = [i for i in os.listdir(path) if '.fbx' in i]
#     if len(files) == 0:
#         return 0
#     else:
#         versions = [int(i[i.index('_v') + 2:i.index('_v') + 5]) for i in files]
#         return sorted(versions)[-1]


def findPipelineCameraHoudini():
    # TRYING TO FIND A PIPELINE CAMERA IN THE SCENE
    if hou.node('/obj/cam1'):
        if 'camVersion' in [i.name() for i in hou.node('/obj/cam1').allParms()]:
            return hou.node('/obj/cam1'), hou.node('/obj/cam1').parm('camVersion').eval()
        else:
            return None
    else:
        return None


def importCamHoudini(camFolder, lastFBXVersion, renameTo = 'cam1', scale = '1', popup = True):
    first_frame = hou.playbar.frameRange()[0]
    last_frame = hou.playbar.frameRange()[1]
    #print first_frame, last_frame
    fbxPath = '%s/%s_cam_v%s.fbx' % (camFolder, camFolder.split('/')[-3], str(lastFBXVersion).zfill(3))
    node = hou.hipFile.importFBX(file_name=fbxPath)
    cam = node[0].children()[0]
    cam =  hou.copyNodesTo([cam], hou.node('/obj'))[0] # copeNodesTo returns tuple. In this case it's camera only. So we take a first item
    node[0].destroy()
    cam.setName(renameTo)

    print '1'

    setGobalFrangeExpr = 'tset `(%d-1)/$FPS` `%d/$FPS`' % (first_frame, last_frame)
    hou.hscript(setGobalFrangeExpr)

    if scale != 1:
        print 'going to scale to %s' % scale
        ns = hou.node('/obj').createNode('null')
        ns.setName('null_scale_up_999')
        cam.setInput(0, ns)
        ns.parm('scale').set(scale)
        cam.setSelected(True, clear_all_selected=True)

        setGobalFrangeExpr = 'tset `(%d-1)/$FPS` `%d/$FPS`' % (first_frame, last_frame)
        hou.hscript(setGobalFrangeExpr)

        bakedNode = cam_bake.bakeAnim_ui(False)
        cam.destroy()
        ns.destroy()
        cam = bakedNode
        cam.setName(renameTo)

    print '2'

    # set attributes part
    ptg = cam.parmTemplateGroup()
    try:
        ptg.remove(ptg.find('fbx_node_path'))
        ptg.remove(ptg.find('fbx_camVersion'))
        ptg.remove(ptg.find('fbx_camFilepath'))
        ptg.remove(ptg.find('camVersion'))
        ptg.remove(ptg.find('camPath'))
    except:
        pass

    cam.setParmTemplateGroup(ptg)
    parm_group = cam.parmTemplateGroup()
    parm_folder = hou.FolderParmTemplate("folder", "Extras")
    parm_folder.addParmTemplate(hou.FloatParmTemplate(name='camVersion', label='cam Version', num_components=1))
    parm_folder.addParmTemplate(hou.StringParmTemplate(name='camFilepath', label='cam Filepath', num_components=1))
    parm_group.append(parm_folder)
    cam.setParmTemplateGroup(parm_group)

    cam.parm('camVersion').set(lastFBXVersion)
    cam.parm('camVersion').lock(True)
    cam.parm('camFilepath').set(fbxPath)
    cam.parm('camFilepath').lock(True)

    cam.parm('near').set(0.1)
    cam.parm('far').set(5000)

    print '3'

    #LIGHT PLATE SEQUENCE TO CAMERA BACKPLATE
    lightPlatePath = '%s/src/lightingPlate/%s_lightingPlate.$F4.exr' % ('/'.join(camFolder.split('/')[:-2]), camFolder.split('/')[-3])
    if os.path.exists(os.path.dirname(lightPlatePath)):
        cam.parm('vm_background').set(lightPlatePath)



    if popup == True:
        hou.ui.displayMessage('Camera v%s successfully imported' % str(lastFBXVersion).zfill(3))


def importLastCamVersionHoudini(force=True):
    first_frame = hou.playbar.playbackRange().x()
    last_frame = hou.playbar.playbackRange().y()
    try:
        shotPath = os.environ['SHOT']
    except:
        hou.ui.displayMessage('Scene not in PIPELINE')
        return
    shot = os.path.split(shotPath)[-1]
    camFolder = "%s/cache/cam" % (shotPath)
    lastFBXVersion = p_utils.common_utils.getLastCamVersion(camFolder)
    if findPipelineCameraHoudini():
        cam, ver = findPipelineCameraHoudini()
        if lastFBXVersion > int(ver):
            # THERE IS NEW CAMERA VERSION
            cam.destroy()
            importCamHoudini(camFolder, lastFBXVersion, scale = 0.01)
        else:
            # THERE IS NO NEW CAMERA VERSION
            hou.ui.displayMessage('You have the latest camera in the scene. Chill.')
    else:
        # THERE IS NO PIPELINE CAMERA IN THE SCENE
        # print 'no pipe camera in the scene'
        try:
            hou.node('/obj/cam1').destroy()
        except:
            pass
        importCamHoudini(camFolder, lastFBXVersion, scale = 0.01)
    setGobalFrangeExpr = 'tset `(%d-1)/$FPS` `%d/$FPS`' % (first_frame, last_frame)
    hou.hscript(setGobalFrangeExpr)


def importLastCamAtStartup():
    first_frame = hou.playbar.playbackRange().x()
    last_frame = hou.playbar.playbackRange().y()
    shotPath = os.environ['SHOT']
    shot = os.path.split(shotPath)[-1]
    camFolder = "%s/cache/cam" % (shotPath)
    lastFBXVersion = p_utils.common_utils.getLastCamVersion(camFolder)
    if findPipelineCameraHoudini():
        cam, ver = findPipelineCameraHoudini()
        print cam, ver
        if lastFBXVersion > int(ver):
            # THERE IS NEW CAMERA VERSION
            okOptions = ['Spasibo, zhelezka', 'Oy, davaj ne zaebuvaj', 'Mne pohuy']
            sayOptions = ['Tvoya kamera prosrochena, chuvak.', 'Nuzhno perezamenit kameru, kozhanuj meshok.']
            hou.ui.displayMessage(sayOptions[random.randrange(len(sayOptions))], buttons=[okOptions[random.randrange(len(okOptions))]])


def bakeWithScale(cam):
    ns = hou.node('/obj').createNode('null')
    ns.setName('null_scale_up_888')
    topNode = recursiveInput.getMostUpperInputNode(hou.node('/obj/cam1'))
    topNode.setInput(0, ns)
    ns.setPosition((topNode.position()[0], topNode.position()[1] + 1))
    ns.parm('scale').set(100)
    cam.setSelected(True, clear_all_selected=True)
    bakedNode = cam_bake.bakeAnim_ui(False)
    cam.setName(cam.name() + '_temp')
    bakedNode.setName('cam1')

# ==============================================================================================
# ==============================================================================================
# ==============================================================================================

def exportOtherShotCamerasHoudini():
    environ = os.environ['SHOT']
    drive = prefs.LoaderPrefs().load()['storage']['projects']
    seq = environ.split('/')[-2]
    project = environ.split('/')[1]
    nodes = ' '.join([i.path() for i in hou.selectedNodes()])
    if not nodes:
        hou.ui.displayMessage('Select something please')
        return
    #print 'NODES %s' % str(nodes)

    p_dict = parser.projectDict(project)
    shots = p_dict.getShots(seq)
    toExport = hou.ui.selectFromList(shots)
    exportedShots = []
    for i in toExport:
        shot = shots[i]
        first_frame = p_dict.getSpecificShotData(seq, shot, 'first_frame')
        last_frame = p_dict.getSpecificShotData(seq, shot, 'last_frame')
        camFolder = "%s/%s/sequences/%s/%s/cache/cam" % (drive, project, seq, shot)
        exportVersion = p_utils.common_utils.getLastCamVersion(camFolder) + 1
        filename = "%s/%s_cam_v%s.fbx" % (camFolder, shot, str(exportVersion).zfill(3))
        #print '%s :: %s' % (shot, filename)

        fbx_rop = hou.node('/out').createNode('filmboxfbx')
        fbx_rop.parm('trange').set(1)
        fbx_rop.parm('f1').deleteAllKeyframes()
        fbx_rop.parm('f1').set(first_frame)
        fbx_rop.parm('f2').deleteAllKeyframes()
        fbx_rop.parm('f2').set(last_frame)
        fbx_rop.parm('sopoutput').set(filename)
        #obj_path = hou.node('/obj/cam1').path()
        fbx_rop.parm('startnode').set(nodes)
        fbx_rop.render()
        exportedShots.append(shot)
    hou.ui.displayMessage('Success! Cams exported for shots %s' % ' '.join(exportedShots))


def exportCamHoudini():
    bakeWithScale(hou.node('/obj/cam1'))
    first_frame = hou.playbar.playbackRange().x()
    last_frame = hou.playbar.playbackRange().y()
    try:
        shotPath = os.environ['SHOT']
    except:
        hou.ui.displayMessage('Scene not in PIPELINE')
        return
    shot = os.path.split(shotPath)[-1]
    camFolder = "%s/cache/cam" % (shotPath)
    if not hou.node('/obj/cam1'):
        hou.ui.displayMessage('There is no cam1 object')
        return
    else:
        exportVersion = p_utils.common_utils.getLastCamVersion(camFolder) + 1
        filename = "%s/%s_cam_v%s.fbx" % (camFolder, shot, str(exportVersion).zfill(3))

        cam = hou.node('/obj/cam1')

        fbx_rop = hou.node('/out').createNode('filmboxfbx')
        fbx_rop.parm('trange').set(1)
        fbx_rop.parm('sopoutput').set(filename)
        obj_path = hou.node('/obj/cam1').path()
        fbx_rop.parm('startnode').set(obj_path)
        fbx_rop.render()
        # fbx_rop.destroy()

        setGobalFrangeExpr = 'tset `(%d-1)/$FPS` `%d/$FPS`' % (first_frame, last_frame)
        hou.hscript(setGobalFrangeExpr)

        for i in ('null_scale_up_888', 'cam1'):
            hou.node('/obj/%s' % i).destroy()

        cam = hou.node('/obj/cam1_temp')
        cam.setName('cam1')

        if 'camVersion' not in [i.name() for i in cam.allParms()] and 'camFilepath' not in [i.name() for i in
                                                                                            cam.allParms()]:
            parm_group = cam.parmTemplateGroup()
            parm_folder = hou.FolderParmTemplate("folder", "Extras")
            parm_folder.addParmTemplate(hou.FloatParmTemplate(name='camVersion', label='cam Version', num_components=1))
            parm_folder.addParmTemplate(
                hou.StringParmTemplate(name='camFilepath', label='cam Filepath', num_components=1))
            parm_group.append(parm_folder)
            cam.setParmTemplateGroup(parm_group)

        cam.parm('camVersion').lock(False)
        cam.parm('camVersion').set(exportVersion)
        cam.parm('camVersion').lock(True)
        cam.parm('camFilepath').lock(False)
        cam.parm('camFilepath').set(filename)
        cam.parm('camFilepath').lock(True)

        hou.ui.displayMessage('Camera v%s successfully exported!' % str(exportVersion).zfill(3))

def importMultipleCameras():
    #first_frame = hou.expandString('$FSTART')
    first_frame = hou.playbar.frameRange()[0]
    last_frame = hou.playbar.frameRange()[1]
    print 'at begining %s %s' % (str(first_frame), str(last_frame))

    seqPath = '/'.join(os.environ['SHOT'].split('/')[:-1]) # GET SEQUENCE FOLDER PATH
    env = os.environ['SHOT']
    splitted = env.split('/')
    project = splitted[1]
    seq = splitted[3]
    allShots = os.listdir(seqPath) # SUKA NU ETO NADO POPRAVIT
    shotsToImport = hou.ui.selectFromList(allShots)
    #print shotsToImport
    for i in shotsToImport:
        shot = allShots[i]
        print shot
        camPath = 'P:/%s/sequences/%s/%s/cache/cam' % (project, seq, shot)
        lastFBXVersion = p_utils.common_utils.getLastCamVersion(camPath)

        setGobalFrangeExpr = 'tset `(%d-1)/$FPS` `%d/$FPS`' % (int(first_frame), last_frame)
        hou.hscript(setGobalFrangeExpr)

        if lastFBXVersion:
            print '\t ' + camPath, lastFBXVersion
            importCamHoudini(camPath, lastFBXVersion, renameTo = '%s_cam' % shot, popup=False, scale = '0.01')
        else:
            print 'There is no camera in %s' % shot

def exportCamToComp():
    if not hou.node('/obj/cam1'):
        hou.ui.displayMessage('There is no cam1 object in the scene')
    else:
        try:
            obj = hou.node('/obj')
            g = obj.createNode('geo')
            r = g.createNode('rop_alembic')
            shot = os.environ['SHOT']
            ver = p_utils.common_utils.getLastCamVersion('%s/cache/cam' % shot, ext='.abc')
            path = '$SHOT/cache/cam/%s_cam_v%s.abc' % (shot.split('/')[-1], str(ver+1).zfill(3))
            r.parm('filename').set(path)
            r.parm('trange').set(1)
            r.parm('objects').set('cam1')
            r.render()

            g.destroy()
            hou.ui.displayMessage('Camera v%s exported to comp!' % str(ver+1).zfill(3))
        except:
           g.destroy()
           hou.ui.displayMessage('Something goes wrong')




# importLastCamVersionHoudini()
# exportCamHoudini()








