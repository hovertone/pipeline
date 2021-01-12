import os
import fnmatch
import nuke
import shutil
from PL_scripts import getPipelineAttrs

# import PL_rendersCleanup
# reload(PL_rendersCleanup)
# PL_rendersCleanup.fixMissingPaths()
# PL_rendersCleanup.main()


def fixMissingPaths():
    needToFix = False
    for r in nuke.allNodes('Read'):
        if r.error():
            needToFix = True
            break

    print 'NEED TO FIX: %s' % needToFix
    if needToFix:
        for r in nuke.allNodes():
            if r.Class() == 'Read' or r.Class() == 'Camera2' or r.Class() == 'DeepRead' or r.Class() == 'ReadGeo2':
                oldVal = r['file'].value()
                newVal = oldVal.replace('P:/vikingsShorts/shots', 'P:/vikings/vikingsShorts/shots')
                r['file'].setValue(newVal)


def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return round(total_size/(1024*1024*1024.0), 2)


def main(remove_precomps = False):
    #fixMissingPaths()
    newSize = 0.0
    root = nuke.root().name()
    try:
        drive, project, seq, shot, assetName, version = getPipelineAttrs()
        path = '%s/%s/sequences/%s/%s/render' % (drive, project, seq, shot)
    except:
        if 'vikings' in root:
            split = root.split('/')
            path = '/'.join(split[:-2]) + '/render'

        else:
            print 'dont have shot attrs. EXIT'
            return


    #print 'path %s' % path
    paths = sorted([i['file'].value() for i in nuke.allNodes('Read') + nuke.allNodes('DeepRead') if path in i['file'].value()])
    #print 'PATHSS %s' % paths
    oldSize = get_size(path)

    # Get a list of all files in directory
    dirsToRemove = []
    for rootDir, subdirs, filenames in os.walk(path):
        # Find the files that matches the given patterm
        if filenames:
            deleteFolder = False
            for f in filenames:
                in_script = False
                for pat in paths:
                    p = pat.split('.')[0]
                    fullpath = '%s/%s' % (rootDir, f)
                    fullpath = fullpath.replace('\\', '/')
                    #print 'FULLPATH %s' % fullpath
                    if p in fullpath:
                        in_script = True
                if in_script:
                    print 'KEEP %s' % fullpath
                else:
                    print 'DELETE %s' % fullpath
                    os.remove(fullpath)
                    folder = os.path.dirname(fullpath)
                    if folder not in dirsToRemove:
                        dirsToRemove.append(folder)

            print '----------------------------------------'

    print 'DIR REMOVING BEGINS'
    if remove_precomps:
        # PRECOMPS PART
        precomps_dir = '%s/%s/sequences/%s/%s/comp/%s/precomp' % (drive, project, seq, shot, assetName)

        for bdn in nuke.allNodes('BackdropNode'):
            for n in bdn.getNodes():
                nuke.delete(n)
            nuke.delete(bdn)
        print 'PRECOMP NODES REMOVED'

        if os.path.exists(precomps_dir):
            newSize += get_size(precomps_dir)
            shutil.rmtree(precomps_dir)
            print 'PRECOMPS FOLDER REMOVED'
    else:
        precomps_dir_size_old = 0

    for d in dirsToRemove:
        try:
            os.removedirs(d)
            print 'REMOVE %s' % d
        except:
            print 'Cant be removed %s' % d

    newSize += get_size(path)
    nuke.message('Old size: %s Gb\nNewSize: %s Gb' % (oldSize, newSize))

def main2():
    print 'inMAIN2'
    try:
        drive, project, seq, shot, assetName, version = getPipelineAttrs()
    except:
        root = nuke.root().name()
        split = root.split('/')
        drive = 'P:'
        project = split[1]
        seq = split[2]
        shot = split[4]

    path = '%s/%s/%s/shots/%s/render' % (drive, project, seq, shot)

    #path = '%s/%s/sequences/%s/%s/render' % (drive, project, seq, shot)
    #print 'path %s' % path
    paths = sorted([i['file'].value() for i in nuke.allNodes('Read') if path in i['file'].value()])
    #print 'pathsss %s' % paths
    oldSize = get_size(path)

    # Get a list of all files in directory
    dirsToRemove = []
    for rootDir, subdirs, filenames in os.walk(path):
        # Find the files that matches the given patterm
        if filenames:
            deleteFolder = False
            for f in filenames:
                in_script = False
                for pat in paths:
                    p = pat.split('.')[0]
                    fullpath = '%s/%s' % (rootDir, f)
                    fullpath = fullpath.replace('\\', '/')
                    #print 'FULLPATH ' + fullpath
                    if p in fullpath:
                        in_script = True
                if in_script:
                    print 'KEEP %s' % fullpath
                else:
                    print 'DELETE %s' % fullpath
                    os.remove(fullpath)
                    folder = os.path.dirname(fullpath)
                    if folder not in dirsToRemove:
                        dirsToRemove.append(folder)

            print '----------------------------------------'

    for d in dirsToRemove:
        try:
            os.removedirs(d)
            print 'REMOVE %s' % d
        except:
            print 'Cant be removed %s' % d

    newSize = get_size(path)
    nuke.message('Old size: %s Gb\nNewSize: %s Gb' % (oldSize, newSize))
