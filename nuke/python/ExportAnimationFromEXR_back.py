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

## Create Scene asset with camera and animation

def CamExp(): 
    selectedNodes = nuke.selectedNodes()
        # either nothing or too much is selected
    if (len(selectedNodes) != 1):
        nuke.message("Select Read node!")
        return "Fail"
    
    nodeType = selectedNodes[0].Class()
    
    if (nodeType != "Read"):
        nuke.message("Select Read node!")
        return "Fail"
    
    n=nuke.toNode(nuke.selectedNode().name())

    b1 = nuke.nodes.Camera2()
    axis = nuke.nodes.Axis2()
    b1['label'].setValue('Cam from EXR')

    #position camera
    b1['xpos'].setValue(n.xpos()+110)
    b1['ypos'].setValue(n.ypos()+110)
    b1.setInput(0, axis)

    axis.setXYpos(b1.xpos(), b1.ypos() - 100)
    axis['uniform_scale'].setValue(100)
    
    k1 = b1['matrix']
    b1['useMatrix'].setValue(1)
    c1 = b1['focal']
    app1 = b1['haperture']
    app2 = b1['vaperture']
    k1.setAnimated()
    c1.setAnimated()
    app1.setAnimated()
    app2.setAnimated()

    fistFF=nuke.Node.firstFrame(nuke.selectedNode())
    lastFF=nuke.Node.lastFrame(nuke.selectedNode())

    aspect = float(b1.format().width())/b1.format().height()
    
    for i in range(fistFF, lastFF+1):

        camFocal = getMetadataFocal(n.metadata('exr/comment',i))
        c1.setValue(camFocal, time = i)
        
        camAperture = getMetadataAperture(n.metadata('exr/comment',i))
        app1.setValue(camAperture, time = i)
        app2.setValue(camAperture/aspect, time = i)
    
        camMatrix = getMetadataMatrix(n.metadata('exr/comment',i))
    
        transposedMatrix = nuke.math.Matrix4(camMatrix)
        transposedMatrix.transpose()
        resMatrix = transposedMatrix 
        
        k1.setValue(resMatrix[0], 0, time = i)
        k1.setValue(resMatrix[1], 1, time = i)
        k1.setValue(resMatrix[2], 2, time = i)
        k1.setValue(resMatrix[3], 3, time = i)
        k1.setValue(resMatrix[4], 4, time = i)
        k1.setValue(resMatrix[5], 5, time = i)
        k1.setValue(resMatrix[6], 6, time = i)
        k1.setValue(resMatrix[7], 7, time = i)
        k1.setValue(resMatrix[8], 8, time = i)
        k1.setValue(resMatrix[9], 9, time = i)
        k1.setValue(resMatrix[10], 10, time = i)
        k1.setValue(resMatrix[11], 11, time = i)
        k1.setValue(resMatrix[12], 12, time = i)
        k1.setValue(resMatrix[13], 13, time = i)
        k1.setValue(resMatrix[14], 14, time = i)
        k1.setValue(resMatrix[15], 15, time = i)
