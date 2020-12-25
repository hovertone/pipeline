## Create camera and animation form *.exr files
 
import math, nuke

## Get Camera Transformation Matrix from EXR

def getMetadataMatrix(meta_list):
    m = nuke.math.Matrix4()
    preMatrix = meta_list[1:-1].replace(")", ", ").split(",")
    try: 
        for i in range(0,16):
          m[i] = float(preMatrix[i])
    except:
          m.makeIdentity()
    return m

## Get Camera FocalLength from EXR

def getMetadataFocal(meta_list):
     preMatrix = meta_list[1:-1].replace(")", ", ").split(",")
     try: 
          m = float(preMatrix[16])
     except:
          m = 50
     return m
     
## Get Camera Aperture from EXR

def getMetadataAperture(meta_list):
     preMatrix = meta_list[1:-1].replace(")", ", ").split(",")
     try: 
          app = float(preMatrix[17])
     except:
          app = 41.4214
     return app

def camDataToDict(camData):
    d = dict()
    splitted = camData.split(',')
    return splitted


## Create Scene asset with camera and animation

def CamExp(): 
    selectedNodes = nuke.selectedNodes('Read')
        # either nothing or too much is selected
    if (len(selectedNodes) != 1):
        nuke.message("Select Read node!")
        return "Fail"
    
    n=selectedNodes[0]

    if 'exr/camData' not in n.metadata().keys():
        print "'exr/camData' is not in a metadata of %s" % n.name()
        return

    b1 = nuke.nodes.Camera2()
    b1['label'].setValue('Cam from EXR')
    b1['tile_color'].setValue(1949872639)

    #position camera
    b1['xpos'].setValue(n.xpos()+110)
    b1['ypos'].setValue(n.ypos()+110)

    tk = b1['translate']
    rk = b1['rotate']
    fk = b1['focal']
    hapk = b1['haperture']
    vapk = b1['vaperture']
    xOrdk = b1['xform_order']
    rOrdk = b1['rot_order']
    for i in (tk, rk, fk, hapk, vapk):
        i.setAnimated()

    fistFF=nuke.Node.firstFrame(n)
    lastFF=nuke.Node.lastFrame(n)

    #aspect = float(n.format().width())/n.format().height()
    aspect = 1.77777777
    #print fistFF, lastFF
    
    for i in range(fistFF, lastFF+1):
        camData = n.metadata(key = 'exr/camData', time = i).split(',')
        #print i, '\n\t\t%s' % camData

        t = (float(camData[0]), float(camData[1]), float(camData[2]))
        r = (float(camData[3]), float(camData[4]), float(camData[5]))
        f = float(camData[6])
        ap = float(camData[7])
        xOrd = int(camData[8])
        rOrd = int(camData[9])

        #print 'translate ', t
        #print 'rotate', r
        #print 'focal %s, aperture %s' % (f, ap)

        tk.setValue(float(camData[0]), 0, time=i)
        tk.setValue(float(camData[1]), 1, time=i)
        tk.setValue(float(camData[2]), 2, time=i)

        rk.setValue(float(camData[3]), 0, time=i)
        rk.setValue(float(camData[4]), 1, time=i)
        rk.setValue(float(camData[5]), 2, time=i)

        fk.setValue(f, time = i)
        hapk.setValue(ap, time = i)
        #print 'aspect = %s' % aspect
        #print 'vap = %s' % (ap/aspect)
        vapk.setValue(ap/aspect, time = i)

        xOrdk.setValue(xOrd)
        rOrdk.setValue(rOrd)

        #return
        #
        # c1.setValue(camFocal, time = i)
        #
        # camAperture = getMetadataAperture(n.metadata('exr/comment',i))
        # app1.setValue(camAperture, time = i)
        # app2.setValue(camAperture/aspect, time = i)
        #
        # camMatrix = getMetadataMatrix(n.metadata('exr/comment',i))
        #
        # transposedMatrix = nuke.math.Matrix4(camMatrix)
        # transposedMatrix.transpose()
        # resMatrix = transposedMatrix
        #
        # k1.setValue(resMatrix[0], 0, time = i)
        # k1.setValue(resMatrix[1], 1, time = i)
        # k1.setValue(resMatrix[2], 2, time = i)
        # k1.setValue(resMatrix[3], 3, time = i)
        # k1.setValue(resMatrix[4], 4, time = i)
        # k1.setValue(resMatrix[5], 5, time = i)
        # k1.setValue(resMatrix[6], 6, time = i)
        # k1.setValue(resMatrix[7], 7, time = i)
        # k1.setValue(resMatrix[8], 8, time = i)
        # k1.setValue(resMatrix[9], 9, time = i)
        # k1.setValue(resMatrix[10], 10, time = i)
        # k1.setValue(resMatrix[11], 11, time = i)
        # k1.setValue(resMatrix[12], 12, time = i)
        # k1.setValue(resMatrix[13], 13, time = i)
        # k1.setValue(resMatrix[14], 14, time = i)
        # k1.setValue(resMatrix[15], 15, time = i)

