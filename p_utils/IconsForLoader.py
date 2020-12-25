
try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *
import sys, subprocess, os



def createIcons(sequencePath):
    path = sequencePath

    if os.path.exists(path):
        shots = os.listdir(path)

        for shot in shots:
            shp = os.path.join(path, shot)
            hires = shp + "/comp/mainComp/precomp/forDaily"
            frame = None

            if os.path.exists(hires):
                frame = os.listdir(hires)[0]
            else:
                hires = shp + "/src/lightingPlate"
                if os.path.exists(hires):
                    frame = os.listdir(hires)[0]

            if frame:
                proxyFolder = shp+"/out/proxy"
                if not os.path.exists(proxyFolder):
                    os.makedirs(proxyFolder)
                if os.path.isfile(proxyFolder+"/proxy.jpg"):
                    os.remove(proxyFolder+"/proxy.jpg")

                cmd = 'X:/app/win/ffmpeg/bin/ffmpeg -gamma 2.2 -i ' + hires + '/' + frame + ' -n -s 512x320 ' + proxyFolder + "/proxy.jpg"
                subprocess.call(cmd, shell=True)


def createAssetIcons(path):
    dirs = os.listdir(path)
    #print dirs
    for dir in dirs:
        ppath = path + "/" + dir + "/main/_lookdev/render"
        try:
            ppath = ppath + "/" + os.listdir(ppath)[0]
            print ppath
        except:
            ppath = None
        if ppath:
            ppath = ppath + "/v001"
            frame = os.listdir(ppath)[0]
            if frame:
                proxyFolder = path + "/" + dir + "/out/proxy"
                if not os.path.exists(proxyFolder):
                    os.makedirs(proxyFolder)
                cmd = 'X:/app/win/ffmpeg/bin/ffmpeg -gamma 2.2 -i ' + ppath + '/' + frame + ' -n -s 512x380 ' + proxyFolder + "/proxy.jpg"
                subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    sqs = os.listdir("P:/Raid/sequences")
    for s in sqs:
        sq = os.path.join("P:/Raid/sequences", s)
        createIcons(sq)
