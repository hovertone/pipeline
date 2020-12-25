import hou

def bakeAnim(node, frameRange, bakeParms = [], parentNode = hou.node('/obj'), byChop = False):
        position = node.position()
        #bake anim to keyframe by chop
        if byChop:
                tempChopnet = hou.node('/obj').createNode('chopnet')
                objectChop = tempChopnet.createNode('object')
                [objectChop.parm(k).set(v) for k, v in zip(['targetpath', 'compute', 'samplerate', 'start', 'end', 'units'], [node.path(), 'fullxform', hou.fps(), frameRange[0], frameRange[1], 'frames']) ]

        trsParms = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']

        if node.type().name() == 'cam':
                bakedNode = parentNode.createNode('cam', node_name = node.name() + "_bake")
                [bakedNode.parm('resx').set(node.parm('resx').eval()), bakedNode.parm('resy').set(node.parm('resy').eval())]
                bakedNode.setPosition(hou.Vector2((position[0] + 1, position[1] - 1)))
        elif not node.type().name() == 'cam':
                bakedNode = hou.copyNodesTo([node], parentNode)[0]
                bakedNode.setInput(0, None)
                [[bakedNode.parm(parmName).deleteAllKeyframes(), bakedNode.parm(parmName).set(0)] for parmName in bakeParms]
                bakedNode.setName('animation:' + node.name(), unique_name = True)
                bakedNode.parm("keeppos").set(0)
                bakedNode.movePreTransformIntoParmTransform()
                bakedNode.setPosition(hou.Vector2((position[0] + 1, position[1] + 1)))

        for frame in xrange(int(frameRange[0]), int(frameRange[1]) + 1):
                time = (frame - 1)/hou.fps()

                tsrMatrix = node.worldTransformAtTime(time)
                for parm, value in zip(trsParms, (list(tsrMatrix.extractTranslates('srt')) + list(tsrMatrix.extractRotates(transform_order='srt', rotate_order='xyz')) + list(tsrMatrix.extractScales(transform_order='srt')) ) ):
                        if parm in bakeParms:
                                if not byChop:
                                        bakedNode.parm(parm).setKeyframe(hou.Keyframe(value, time))
                                else:
                                        bakedNode.parm(parm).setKeyframe(hou.Keyframe(objectChop.track(parm).evalAtFrame(frame), time))

                if bakeParms != []:
                        for parm, value in zip(bakeParms, [node.parm(p).evalAtFrame(frame) for p in bakeParms]):
                                if not parm in trsParms:
                                        bakedNode.parm(parm).setKeyframe(hou.Keyframe(value, time))

        if byChop:
                tempChopnet.destroy()
        #print bakedNode.name()
        return bakedNode

def bakeAnim_ui(askFrames=True):
        nodes = hou.selectedNodes()
        if nodes:
                if askFrames:
                        frameRangeUserInput = hou.ui.readMultiInput('Bake Framerange', ['Start Frame', 'End Frame'], buttons=('OK','Cancel'), initial_contents = [str(hou.playbar.playbackRange()[0]), str(hou.playbar.playbackRange()[1])])
                else:
                        frameRangeUserInput = (0, (str(hou.playbar.playbackRange()[0]), str(hou.playbar.playbackRange()[1])))
                if bool(1 - frameRangeUserInput[0]):
                        frameRange = frameRangeUserInput[1]
                        bakedNodes = []
                        for node in nodes:
                                #bake non cam objects
                                if not node.type().name() == 'cam':
                                        parms = [parm.name() for parm in node.parms() if not parm.isHidden() and not 'vm_' in parm.name()]
                                        #bake one object
                                        if len(nodes) == 1:
                                                print 'PARMS %s' % parms
                                                #bakedParmsList = hou.ui.selectFromList(parms, default_choices=(0,), exclusive=False, message=None, title = 'Select Baked Parms', column_header=None, num_visible_rows=10)
                                                #bakedParmsList = parms[]
                                                bakedParmsList = tuple(range(len(parms)))
                                                print 'BAKED PARMS LIST %s ' % str(bakedParmsList)
                                                if len(bakedParmsList) != 0:
                                                        if bakedParmsList[0] != 0:
                                                                bakeAnim(node, [int(float(frameRange[0])), int(float(frameRange[1]))], bakeParms = [parms[x] for x in bakedParmsList], parentNode = node.parent(), byChop = True)
                                        #bake mass objects
                                        if len(nodes) > 1:
                                                bakedNodes.append(bakeAnim(node, [int(float(frameRange[0])), int(float(frameRange[1]))], bakeParms = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'], parentNode = node.parent(), byChop = True))
                                #bake cam objects
                                elif node.type().name() == 'cam':
                                        return bakeAnim(node, [int(float(frameRange[0])), int(float(frameRange[1]))], bakeParms = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'focal', 'aperture', 'resx', 'resy'], byChop = True)
                        if len(bakedNodes) > 1:
                                if bool(1 - hou.ui.displayMessage('Move baked objects to new subnet ?', buttons=('Yes','No'), title = 'Bake Animation')):
                                        if nodes[0].parent() == hou.node('/obj'):
                                                newParentNode = hou.node('/obj').createNode('subnet')
                                                if nodes[0].parent().name() == 'obj':
                                                        newParentNodeName = 'animation:' + nodes[0].name() + '_BAKE'
                                                else:
                                                        newParentNodeName = 'animation:' + nodes[0].parent().name()
                                                newParentNode.setName(newParentNodeName, unique_name = True)
                                        else:
                                                newParentNode = nodes[0].parent().parent().createNode('subnet')
                                                newParentNode.setName('animation:' + nodes[0].parent().name(), unique_name = True)
                                        hou.moveNodesTo(bakedNodes, newParentNode)
                                        newParentNode.layoutChildren()
                                        position = nodes[0].parent().position()
                                        newParentNode.setPosition(hou.Vector2((position[0] + 3, position[1])))
        else:
                hou.ui.displayMessage('Select Node for Baking', buttons=('OK',), title = 'Warning')


#bakeAnim_ui()