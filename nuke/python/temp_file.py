#print 'path %s' % path
paths = sorted([i['file'].value() for i in nuke.allNodes('Read') + nuke.allNodes('DeepRead') if path in i['file'].value()])
#print 'PATHSS %s' % paths
oldSize = get_size(path)

# Get a list of all files and directories to remove
self.files_to_remove = list()
dirsToRemove = list()
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
                #os.remove(fullpath)
                self.files_to_remove.append(fullpath)
                folder = os.path.dirname(fullpath)
                if folder not in dirsToRemove:
                    dirsToRemove.append(folder)