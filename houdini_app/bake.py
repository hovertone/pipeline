import os, sys
import hou
def bb():
	nodes = hou.selectedNodes()
	trsParms = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
	color = hou.Color(0.976, 0.78, 0.263)
	UserInput = hou.ui.readMultiInput('Bake Framerange', ['Start Frame', 'End Frame', 'Substeps'], buttons=('OK','Cancel'), initial_contents = [str(hou.playbar.playbackRange()[0]), str(hou.playbar.playbackRange()[1]), "1"])
	if bool(1 - UserInput[0]):
		frameRange = [UserInput[1][0], UserInput[1][1],  UserInput[1][2]]
	for node in nodes:
		parentNode = node.parent()
		nodeName = node.name()
		bakedNode = parentNode.createNode('null',  node_name = "bake_"+node.name().split('_')[-1])
		bakedNode.setColor(color)
		bakedNode.setInput(0, node, 0)
		bakedNode.moveToGoodPosition(relative_to_inputs=True, move_inputs=True, move_outputs=True, move_unconnected=True)
		bakedNode.setInput(0, None, 0)
		fstart = int(float(frameRange[0]))-1
		fend = int(float(frameRange[1]))+1
		substep = 1/float(frameRange[2])
		rrange = fend-fstart
		counts = int(float(rrange)/substep)
		for f in range(counts+1):
			frame = float(fstart+substep*float(f))
			print frame
			time = ((frame - 1)/hou.fps())
			tsrMatrix = node.worldTransformAtTime(time)
			for parm, value in zip(trsParms, (list(tsrMatrix.extractTranslates('srt')) + list(tsrMatrix.extractRotates(transform_order='srt', rotate_order='xyz')) + list(tsrMatrix.extractScales(transform_order='srt')) ) ):
				bakedNode.parm(parm).setKeyframe(hou.Keyframe(value, time))
