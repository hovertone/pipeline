import maya.cmds as cmds

def addExtraKeys(first, last, moveFrames = True, objs = cmds.ls(selection=True)):
    #objs = cmds.ls(selection=True)
    #obj = objs[0]

    for obj in objs:
        animAttributes = cmds.listAnimatable(obj)
        print obj, animAttributes
        if animAttributes:
            for attribute in animAttributes:
                try:
                    numKeyframes = cmds.keyframe(attribute, query=True, keyframeCount=True)
                    #print '%s has %s keyframes' % (attribute, numKeyframes)
                    if (numKeyframes > 0):
                        #print attribute, ' has a keyframes'
                        # get a lists of a keyframe position (time) and value
                        times = cmds.keyframe(attribute, query=True, index=(0,numKeyframes), timeChange=True)
                        values = cmds.keyframe(attribute, query=True, index=(0,numKeyframes), valueChange=True)
                        cFirst = times[0]
                        cLast = times[-1]

                        # If there is a keyframe on non-integer position (ex. 1001.5) then place it on a integer position
                        if moveFrames:
                            try:
                                if abs(cFirst - first) < 1:
                                    #print 'close to first'
                                    cmds.keyframe(time=(cFirst,cFirst),timeChange=first)
                                    times[0]=first
                                    #print '%s -> %s keyframe set of %s attribute' % (cFirst, first, attribute)

                                if abs(cLast - last) < 1:
                                    #print 'close to first'
                                    cmds.keyframe(time=(cLast,cLast),timeChange=last)
                                    times[-1]=last
                                    #print '%s -> %s keyframe set of %s attribute' % (cLast, last, attribute)
                            except RuntimeError:
                                #cmds.confirmDialog(m = 'Deselect keyframes selection')
                                #return
                                print 'frame didnt move for some reason'
                                #pass

                        # create frame before first frame of the shot
                        if times[0] == first:
                            difference = cmds.getAttr('%s' % attribute,time=times[0]) - cmds.getAttr('%s' % attribute,time=times[0]+1)
                            cmds.setKeyframe(attribute, value=values[0]+difference, time=times[0]-1)
                            cmds.keyTangent(obj, attribute=attribute, inTangentType='spline', outTangentType='spline', time=(int(times[0]-1), int(times[0]-1)))
                            print 'Created a keyframe on %s frame for %s attribute' % (times[0]-1, attribute)

                        # create frame after last frame of the shot
                        if times[-1] == last:
                            difference = cmds.getAttr('%s' % attribute,time=times[-1]-1) - cmds.getAttr('%s' % attribute,time=times[-1])
                            cmds.setKeyframe(attribute, value=values[-1]-difference, time=times[-1]+1)
                            cmds.keyTangent(obj, attribute=attribute, inTangentType='spline', outTangentType='spline', time=(int(times[-1]+1), int(times[-1]+1)))
                            print 'Created a keyframe on %s frame for %s attribute' % (times[-1]+1, attribute)
                except:
                    print '------------- %s' % attribute
                    break
    cmds.confirmDialog(m='Pohodu srabotalo!')

def addExtraKeys2():
    first = 1082
    last = 1101
    acs = cmds.listConnections(t='animCurve')

    for attribute in acs:
        numKeyframes = cmds.keyframe(attribute, query=True, keyframeCount=True)

        if numKeyframes > 0:
            print attribute
            times = cmds.keyframe(attribute, query=True, index=(0, numKeyframes), timeChange=True)
            values = cmds.keyframe(attribute, query=True, index=(0, numKeyframes), valueChange=True)

            cFirst = times[0]
            cLast = times[-1]

            # create frame before first frame of the shot
            #try:
            if times[0] == first:
                valA = cmds.getAttr(attribute, time=times[0])
                valB = cmds.getAttr(attribute, time=times[0])
                difference = cmds.getAttr(attribute, time=times[0]) - cmds.getAttr(attribute.replace('_', '.'), time=times[0] + 1)
                #cmds.setKeyframe(attribute, value=values[0] + difference, time=times[0] - 1)
                #cmds.keyTangent(obj, attribute=attribute, inTangentType='spline', outTangentType='spline', time=(int(times[0] - 1), int(times[0] - 1)))
                #print 'Created a keyframe on %s frame for %s attribute' % (times[0] - 1, attribute)
            #except:
            #    print 'FAILED %s' % attribute

            #create frame after last frame of the shot
            # if times[-1] == last:
            #     difference = cmds.getAttr(attribute.replace('_', '.'), time=times[-1] - 1) - cmds.getAttr(attribute.replace('_', '.'), time=times[-1])
            #     cmds.setKeyframe(attribute, value=values[-1] - difference, time=times[-1] + 1)
            #     #cmds.keyTangent(obj, attribute=attribute, inTangentType='spline', outTangentType='spline', time=(int(times[-1] + 1), int(times[-1] + 1)))
            #     print 'Created a keyframe on %s frame for %s attribute' % (times[-1] + 1, attribute)