import os


def getLastCamVersion(path, ext='.fbx'):
    files = [i for i in os.listdir(path) if ext in i]
    if len(files) == 0:
        return 0
    else:
        versions = [int(i[i.index('_v')+2:i.index('_v')+5]) for i in files]
        return sorted(versions)[-1]