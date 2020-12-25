# HOUDINI

import os
from houdini_app.Loader import loader_preferences as prefs
from p_utils import csv_parser_bak as parser


def getLastFBXVersion(path, name, ext='.fbx'):
    files = [i for i in os.listdir(path) if ext in i]
    if len(files) == 0:
        return 0
    else:
        versions = [int(i[i.index('_v') + 2:i.index('_v') + 5]) for i in files if name in i]
        return sorted(versions)[-1]


environ = os.environ['SHOT']
drive = prefs.LoaderPrefs().load()['storage']['projects']
seq = environ.split('/')[-2]
shot = environ.split('/')[-1]
project = environ.split('/')[1]

nodes = ' '.join([i.path() for i in hou.selectedNodes()])
if nodes:
    res = hou.ui.readInput("Enter name:", buttons=("OK", "Cancel"))
    if res[0] == 0:
        name = res[1]
        p_dict = parser.projectDict(project)
        first_frame = p_dict.getSpecificShotData(seq, shot, 'first_frame')
        last_frame = p_dict.getSpecificShotData(seq, shot, 'last_frame')
        locFolder = "%s/%s/sequences/%s/%s/comp/_dataFrom3d" % (drive, project, seq, shot)
        if not os.path.exists(locFolder): os.makedirs(locFolder)
        locName = '%s_v%s.fbx' % (name, str(getLastFBXVersion(locFolder, name) + 1).zfill(3))
        print locName
        filename = os.path.join(locFolder, locName).replace('\\', '/')

        fbx_rop = hou.node('/out').createNode('filmboxfbx')
        fbx_rop.parm('trange').set(1)
        fbx_rop.parm('f1').deleteAllKeyframes()
        fbx_rop.parm('f1').set(first_frame)
        fbx_rop.parm('f2').deleteAllKeyframes()
        fbx_rop.parm('f2').set(last_frame)
        fbx_rop.parm('sopoutput').set(filename)
        # obj_path = hou.node('/obj/cam1').path()
        fbx_rop.parm('startnode').set(nodes)
        fbx_rop.render()
        fbx_rop.destroy()
    else:
        pass
else:
    hou.ui.displayMessage('Select subnet with locators inside')





# NUKE

from PL_scripts import getPipelineAttrs
from houdini_app.Loader import loader_preferences as prefs

def getLastFBXVersion(path, name, ext='.fbx'):
    files = [i for i in os.listdir(path) if ext in i]
    if len(files) == 0:
        return 0
    else:
        versions = [int(i[i.index('_v')+2:i.index('_v')+5]) for i in files if name in i]
        return sorted(versions)[-1]

drive, project, seq, shot, assetName, ver = getPipelineAttrs()
locsFolder = '%s/%s/sequences/%s/%s/comp/_dataFrom3d' % (drive, project, seq, shot)
files = os.listdir(locsFolder)
names = []
for f in files:
    names.append(f.split('_v')[0])

names = list(set(names))
print 'names %s' % names
p = nuke.Panel('my custom panel')
p.addEnumerationPulldown('Which one?', ' '.join(names))
ret = p.show()
if ret:
    #print '111'
    nameToFind = p.value('Which one?')
    #print nameToFind
    fbxToImport = getLastFBXVersion(locsFolder, nameToFind)
    p = os.path.join(locsFolder, '%s_v%s.fbx' % (nameToFind, str(fbxToImport).zfill(3))).replace('\\', '/')
    #print p
    a = nuke.createNode('Axis2')
    a['read_from_file'].setValue(True)
    a['file'].setValue(p)
    a['label'].setValue('%s %s' % (nameToFind, 'v' + str(fbxToImport).zfill(3)))
else:
    #print 'cancel'
    pass