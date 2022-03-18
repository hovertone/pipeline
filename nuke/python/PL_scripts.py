import nuke
import os
import re
from scripts import selectOnly
import shutil
import subprocess as sp
from houdini_app.Loader import loader_preferences as prefs

def inPipeline():
    root = nuke.root()
    if 'shot' in root.knobs().keys() and 'project' in root.knobs().keys():
        return True
    else:
        return False

def labelRender(nodes = None):
    if nodes == None:
        nodes = nuke.selectedNodes()

    for n in nodes:
        filePath = n['file'].value()
        filePathSplitted = filePath.split('/')
        #print filePathSplitted
        shot = filePathSplitted[4]
        layer = filePathSplitted[-3].upper()
        ver = filePathSplitted[-2]
        ff = n['first'].value()
        lf = n['last'].value()
        #print shot, layer, ff, lf, ver
        
        n['tile_color'].setValue(255)
        label = '%s\n%s\n%s\n%s - %s' % (shot, layer, ver, ff, lf)
        n['label'].setValue(label)
    

def renderVer(direction = 'up'):
    nodes = nuke.selectedNodes('Read')
    for n in nodes:
        filePath = n['file'].value()
        splitted = filePath.split('/')
        versionsFolder = '/'.join(splitted[:-2])
        curVer = splitted[-2]
        versions = sorted(os.listdir(versionsFolder))
        i = versions.index(curVer)
        if direction == 'up':
            if i == len(versions) - 1:
                nuke.message('This is a last version')
                return
            else:
                newVer = versions[i + 1]
        elif direction == 'down':
            if i == 0:
                nuke.message("This is an earliest version")
                return
            else:
                newVer = versions[i - 1]
        elif direction == 'max':
            i = len(versions) - 1
            newVer = versions[i]

        newPath = filePath.replace(curVer, newVer)
        n['file'].setValue(newPath)
        # curVer = int(splitted[-2].strip('v'))
        # print 'curVer is %s' % curVer
        # if direction == 'up':
        #     newVer = 'v%s' % str(curVer + 1).zfill(3)
        # else:
        #     newVer = 'v%s' % str(curVer - 1).zfill(3)
        #
        #
        #
        # splitted[-2] = newVer
        # n['file'].setValue('/'.join(splitted))
        #
        selectOnly(n)
        labelRender()

def renderVerMax():
    nodes = nuke.selectedNodes('Read')
    for n in nodes:
        filePath = n['file'].value()
        splitted = filePath.split('/')
        
        curVer = splitted[-2]
        allVersionsSorted = sorted(os.listdir('/'.join(splitted[:splitted.index('render')+2])))
        maxVer = allVersionsSorted[-1]
        if maxVer > curVer:
            MaxVerFilePath = filePath.replace(curVer, maxVer)
            print '### SUCCESS'
            print '#   %s   #   %s ' % (maxVer, '/'.join(MaxVerFilePath.split('/')[MaxVerFilePath.split('/').index('render')+1:]))
            print '###'
            #print MaxVerFilePath    

            n['file'].setValue(MaxVerFilePath )
        else:
            print '### No newer versions. %s' % curVer

        selectOnly(n)
        labelRender()
        
def getShotInfo():
    scriptsSave = nuke.root().name()
    if 'P:/' in scriptsSave and 'shots' in scriptsSave and 'comp/scripts' in scriptsSave:
        splitted = scriptsSave.split('/')
        project, shot = splitted[1], splitted[3]
        return project, shot
    else:
        return None

def getPipelineAttrs():
    # for i in ('project', 'seq', 'shot'):
    #     if i not in nuke.root().knobs().keys():
    #         return None

    r = nuke.root()
    #project = r['project'].value()
    #seq = r['seq'].value()
    #shot = r['shot'].value()
    #assetName = r['assetName'].value()

    scriptPath = nuke.root().name()
    sp = scriptPath.split('/')
    shotPath = '/'.join(sp[:-3])
    scriptName = os.path.split(scriptPath)[-1]

    project = sp[5]
    seq = sp[7]
    shot = sp[-4]
    assetName = 'my ass'

    try:
        match = re.match(r'(\w*)_(\w*)_v(\d*)', scriptName)
        version = int(match.group(3))
    except:
        version = -1

    drive = prefs.LoaderPrefs().load()['storage']['projects']
    drive = '//loky.plarium.local/project' # HARDCODE

    return drive, project, seq, shot, assetName, version

def getPipelineAttrsFromPath(path):
    path = path.replace('\\', '/')

    if 'sequences' not in path:
        print 'not pipeline path, buddy'
        return None
    else:
        ret = dict()
        sp = path.split('/')
        ret['project'] = sp[1]
        ret['seq'] = sp[3]
        ret['shot'] = sp[4]

        return ret

def addFavoriteFolders():
    print 'in add favourite folders'
    if getPipelineAttrs():
        drive, project, seq, shot, assetName, ver= getPipelineAttrs()
        if 'assetBuilds' not in seq:
            shotPath = '%s/%s/sequences/%s/%s' % (drive, project, seq, shot)
            rendersPath = '%s/%s/sequences/%s/%s/render' % (drive, project, seq, shot)
            compPath = '%s/%s/sequences/%s/%s/comp/%s' % (drive, project, seq, shot, assetName)
            precompPath = '%s/%s/sequences/%s/%s/comp/%s/precomp' % (drive, project, seq, shot, assetName)
            srcPath = '%s/%s/sequences/%s/%s/src' % (drive, project, seq, shot)

            nuke.addFavoriteDir('_shot', shotPath)
            nuke.addFavoriteDir('_renders', rendersPath)
            nuke.addFavoriteDir('_comp', compPath)
            nuke.addFavoriteDir('_precomp', precompPath)
            nuke.addFavoriteDir('_src', srcPath)
            print 'shot favourite folders added'
        else:
            shotPath = '%s/%s/%s/%s' % (drive, project, seq, shot)
            rendersPath = '%s/%s/%s/%s/lookdev/render' % (drive, project, seq, shot)
            compPath = '%s/%s/%s/%s/%s' % (drive, project, seq, shot, assetName)
            precompPath = '%s/%s/%s/%s/%s/precomp' % (drive, project, seq, shot, assetName)
            for p in [shotPath, rendersPath, compPath, precompPath]:
                print p

            nuke.addFavoriteDir('_shot', shotPath)
            nuke.addFavoriteDir('_renders', rendersPath)
            nuke.addFavoriteDir('_comp', compPath)
            nuke.addFavoriteDir('_precomp', precompPath)
            print 'assetbuilds favourite folders added'
    else:
        print "can't add favourite folders"

def callBackCheckAndAdd():
    #nuke.tprint('callback workd')
    if getShotInfo():
        #nuke.tprint('pipeline shot')
        l = getShotInfo()
        addFavoriteFolders(l)
    else:
        nuke.tprint('Not pipeline shot')

def movRenderAndMove():
    nodes = nuke.selectedNodes('Write')
    for n in nodes:
        fileFullPath = n['file'].value()
        if 'P:/' in fileFullPath:
            localPath = fileFullPath.replace('P:/', 'D:/')
            if not os.path.exists(os.path.split(localPath)[0]):
                os.makedirs(os.path.split(localPath)[0])

            panelResult = nuke.getFramesAndViews('Render frame range', default = '%s-%s' % (n.firstFrame(), n.lastFrame()))
            firstFrame, lastFrame = panelResult[0].split('-')
            n['file'].setValue(localPath)
            nuke.execute(n.name(), int(firstFrame), int(lastFrame))
            n['file'].setValue(fileFullPath)

            shutil.copy2(localPath, fileFullPath)



def getLastCamVersions():
    n = nuke.thisNode()
    path = n['shotsDir'].value()
    cameras = n.getNodes('Camera2')
    for c in cameras:
        shot = c['label'].value()
        abcs = [i for i in os.listdir('%s/%s/cache/cam' % (path, shot)) if '.abc' in i]
        lastVer = '%s/%s/cache/cam/%s' % (path, shot, sorted(abcs)[-1])
        c['file'].setValue(lastVer)

def camsTick():
    n = nuke.thisNode()
    cameras = n.getNodes('Camera2')
    for c in cameras:
        c['read_from_file'].setValue(True)
        c['frame_rate'].setValue(25)

def camsUntick():
    n = nuke.thisNode()
    cameras = n.getNodes('Camera2')
    for c in cameras:
        c['read_from_file'].setValue(False)

def createACESconverters():
    ocio = nuke.createNode('OCIOColorSpace')
    ocio['out_colorspace'].setValue('Output - Rec.2020')
    ocio['label'].setValue('ACEScg to Rec.2020')

    ocio1 = nuke.createNode('OCIOColorSpace')
    ocio1['in_colorspace'].setValue('Output - Rec.2020')
    ocio1['label'].setValue('Rec.2020 to ACEScg')

    ocio1.setInput(0, None)
    ocio1.setXYpos(ocio.xpos() + 110, ocio.ypos())

def get_last_version(path, filter = None):
    if filter:
        list = [i for i in os.listdir(path) if filter in i]
    else:
        list = os.listdir(path)

    if len(list) == 0:
        return 0
        #no saves found
    files = []
    versions = []

    for f in list:
        ff = os.path.join(path, f).replace("\\", "/")
        #nuke.tprint(ff)
        if os.path.isfile(ff):
            files.append(f)

    for f in files:
        if "~" in f or '.autosave' in f:
            pass
        else:
            match = re.match(r'(\w*)_(\w*)_v(\d*)', f)
            versions.append(int(match.group(3)))

    versions = sorted(versions)
    #nuke.message(str(versions))
    return versions[-1] #integer type

def renameScriptWithMyName():
    user = os.environ['COMPUTERNAME'].lower()
    oldPath = nuke.root().name()
    folder, file = os.path.split(oldPath)
    splitted = file.split('_')
    splitted[-2] = user
    curVer = splitted[-1]
    match = re.match(r'v(\d*)', curVer)
    #newVer = get_last_version(path = folder, filter = user)

    all_files = os.listdir(folder)
    versions = []

    for f in all_files:
        if not "afanasy" in f:
            if ".nk" in f:
                v = f.split(".")[0][-3:]
                if v.isdigit() == True:
                    versions.append(int(v))

    print versions
    versions = sorted(versions)
    up_version = str(versions[-1] + 1).zfill(3)

    replaced = curVer.replace(match.group(1), up_version)
    splitted[-1] = replaced
    file_path = os.path.join(folder, '_'.join(splitted)).replace("\\", "/")
    nuke.scriptSaveAs(file_path)
    print 'Script has been renamed to %s' % file_path

def callRV():
    path_RV = 'X:/app/win/rv/rv7.1.1/bin/rv.exe'

    if nuke.selectedNodes() == []:
        nuke.message('Select READ or WRITE node to proceed to RV')
        return

    paths = []
    for n in [i for i in nuke.selectedNodes() if i.Class() == 'Read' or i.Class() == 'Write']:
        paths.append(n['file'].value())

    paths_set = set(paths)
    for p in paths_set:
        sp.Popen('%s %s' % (path_RV, p))

def substitutePaths():
    if nuke.selectedNodes() == []:
        nuke.message('Select nodes to replace paths')
        return
    else:
        curShot = nuke.root()['shot'].value()
        nodesReplaced = []
        for n in nuke.selectedNodes():
            if n.Class() == 'Read' or n.Class() == 'Write':
                oldPath = n['file'].value()
                match = re.search(r'sh(\d{3})', oldPath)
                newPath = oldPath.replace(match.group(), curShot)
                n['file'].setValue(newPath)
                nodesReplaced.append(n.name())

        nuke.message('Replaced paths for %s nodes' % ', '.join(nodesReplaced))

# #############################################
#
#  FOR REVIEW SESSIONS  :: NUKE SCRIPTS
#
# #############################################

def createReviewWrite(srcName, ext='exr'):
    import os
    from CUF import selectOnly, getMostBottomNode
    #srcName = 'animPlate'

    for n in nuke.selectedNodes('Read'):
        selectOnly(n)
        toConnect = getMostBottomNode()
        selectOnly(toConnect)
        path = n['file'].value()
        splitted = path.split('/')
        shot = splitted[4]
        newPath = '%s/src/%s/%s_%s.####.%s' % ('/'.join(splitted[:5]), srcName, shot, srcName, ext)
        #print newPath
        w = nuke.createNode('Write')
        w['file'].setValue(newPath)

def createHiresWrite(srcName):
    for n in nuke.selectedNodes('Read'):
        selectOnly(n)
        toConnect = getMostBottomNode()
        selectOnly(toConnect)
        path = n['file'].value()
        splitted = path.split('/')
        seq = splitted[-6]
        shot = splitted[4]
        newPath = '%s/out/hires/%s_%s_hires_acescg.####.exr' % ('/'.join(splitted[:5]), seq, shot)
        print newPath
        w = nuke.createNode('Write')
        w['file'].setValue(newPath)

def importSequenceHireses(shots=None):
    if not shots:
        if nuke.selectedNodes():
            lowestYpos = sorted(nuke.allNodes(), key=lambda x: x.ypos(), reverse=True)[0].ypos()
            for n in nuke.selectedNodes():
                path = n['file'].value()
                drive = prefs.LoaderPrefs().load()['storage']['projects']
                attrs = getPipelineAttrsFromPath(path)
                writePath = '%s/%s/sequences/%s/%s/out/hires/%s_%s_hires_acescg.####.exr' % (drive, attrs['project'], attrs['seq'], attrs['shot'], attrs['seq'], attrs['shot'])
                print '%s' % attrs['shot'].upper()
                print writePath
                r = nuke.nodes.Read()
                r['file'].setValue(writePath)
                r.setXYpos(r.xpos(), lowestYpos+80)

def fixDailyWrite():
    for n in nuke.allNodes('Write'):
        if 'DAILIES' in n['file'].value():
            n['colorspace'].setValue('Output - Rec.709')
            print "Daily write's colorspace set to Rec.709"