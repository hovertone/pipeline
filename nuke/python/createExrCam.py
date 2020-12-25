import nuke
import math
 
def createExrCam():
    '''Creates a camera from exr metadata of selected node'''

    node = nuke.selectedNode()
    data = node.metadata()
    reqFields = ['exr/camera%s' % i for i in ('Aperture', 'Transform')]
    if not set( reqFields ).issubset( data ):
        nuke.message( 'Insufficient metadata for camera found' )
        return
   
    first = node.firstFrame()
    last = node.lastFrame()
    ret = nuke.getFramesAndViews( 'Create Camera from Metadata', '%s-%s' %( first, last )  )
    fRange = nuke.FrameRange( ret[0] )
   
    cam = nuke.createNode( 'Camera2' )
    cam['useMatrix'].setValue( False )
    cam['label'].setValue('IMPORTED FROM EXR')
   
    for k in ( 'focal', 'haperture', 'translate', 'rotate'):
        cam[k].setAnimated()
   
    task = nuke.ProgressTask( 'Baking camera' )
   
    for curTask, frame in enumerate( fRange ):

        if task.isCancelled():
            nuke.executeInMainThread( nuke.message, args=( "Phew!" ) )
            break;
        task.setMessage( 'processing frame %s' % frame )

        #get horizontal aperture and FOV, calculate focal
        val = node.metadata( 'exr/cameraAperture', frame)
        fov = node.metadata( 'exr/cameraFov', frame)
        focal = val / (2 * math.tan(math.radians(fov)/2.0))
 
        cam['focal'].setValueAt(float(focal),frame)
        cam['haperture'].setValueAt(float(val),frame)
 
        #set camera matrix
        matrixCamera = node.metadata( 'exr/cameraTransform', frame)
        matrixCreated = nuke.math.Matrix4()
       
        for k,v in enumerate(matrixCamera):
            matrixCreated[k] = v
       
        translate = matrixCreated.transform(nuke.math.Vector3(0,0,0))

        #flip rotation axis
        matrixCreated.rotateX(math.radians(90))
        matrixCreated.rotationOnly()
        invMatrix = matrixCreated.inverse()
        rotate = invMatrix.rotationsZXY()

        eulerRot = [float(math.degrees(rotate[0])), 180.0 - float(math.degrees(rotate[2])), 180.0 - float(math.degrees(rotate[1]))]

        #Avoid rotations flipping across thresholds (multiples of 360) to avoid Motion blur artifacts
        #if it crosses a threshold, put current rotation in same threshold, and keep if it's closer
        if frame > fRange.first():
            for i in range(3):
                if math.ceil(eulerRot[i]/360) != math.ceil(lastRot[i]/360):
                    temp = eulerRot[i] + 360 * (math.ceil(lastRot[i]/360) - math.ceil(eulerRot[i]/360))
                    if abs(lastRot[i] - temp) < 180:
                        eulerRot[i] = temp
        lastRot = [x for x in eulerRot]

        cam['translate'].setValueAt(float(translate.x),frame,0)
        cam['translate'].setValueAt(float(translate.z),frame,1) #swap z and y
        cam['translate'].setValueAt(float(-translate.y),frame,2) #swap z and y, invert y
        cam['rotate'].setValueAt(eulerRot[0],frame,0)
        cam['rotate'].setValueAt(eulerRot[1],frame,1)
        cam['rotate'].setValueAt(eulerRot[2],frame,2)
 
        task.setProgress( int( float(curTask) / fRange.frames() *100) )