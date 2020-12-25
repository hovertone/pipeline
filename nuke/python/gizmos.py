import os, nuke

def fixPath(path):
    '''
    Fixes path string for Windows. Replaces \ or \\ with /.
    
    Arguments(path)
        {path} string to fix
    '''
    newPath = path.replace('\\\\', '/')
    newPath = path.replace('\\', '/')
    
    return newPath



def findGizmoFolder(paths = nuke.pluginPath()):

    if type(paths) == str:
        paths = [paths]

    fixedPaths = []
    for p in paths:
        fixedPaths.append(fixPath(p))

    paths = fixedPaths
    del(fixedPaths)

    pathsWithGizmos = []
    for p in paths:
        if os.path.exists(p):
            for itm in os.listdir(p):
                if '.' in itm:
                    if '.gizmo' in itm:
                        pathsWithGizmos.append(p) 
                    break

    return pathsWithGizmos


def main(gizmosPaths, menuname = 'Gizmos'):
    gizmos = []

    for gizmosPath in gizmosPaths:
        for i in os.listdir(gizmosPath):
                if '.gizmo' in i:
                    gizmos.append(i)

    #print gizmos

    mymenug = nuke.menu('Nodes').findItem('PNS/Gizmos/autoinstal')
    if not mymenug: mymenug = nuke.menu('Nodes').addMenu('PNS/Gizmos/autoinstal')
    #print '^^^^^^^^^^^^^^^^^^^^ %s' % mymenug
    # help(mymenug)
    # print mymenug.name()    
    for g in gizmos:
        gizmo = os.path.split(g)[-1]
        gizmoName = gizmo[:gizmo.find('.')]
        gizmoQuotes = '"' + gizmo + '"'
        mymenug.addCommand(str(gizmoName), 'nuke.createNode(' + str(gizmoQuotes) + ')')
