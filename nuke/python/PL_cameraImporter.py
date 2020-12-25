import os
import nuke
from PL_scripts import inPipeline

def getCamera(shotPath):
	cam_path = os.path.join(shotPath, "cache/cam")
	cameras = [i for i in os.listdir(cam_path) if '.abc' in i]
	if cameras == []:
		return
	else:
		cam_file = os.path.join(cam_path, cameras[-1])
		#print "SHOT_CAMERA", cam_file
		return cam_file



def importCam():
	if not inPipeline:
		nuke.message("Not in pipeline")
		return
	else:
		project = nuke.root()['project'].value()
		seq = nuke.root()['seq'].value()
		shot = nuke.root()['shot'].value()
		camPath = getCamera('P:/%s/sequences/%s/%s' % (project, seq, shot))
		if not camPath:
			nuke.message('There is no camera for comp. Use camToComp inside houdini.')
			return

		ver = camPath[camPath.index('_v')+2:camPath.index('_v')+5]
		#print ver
		#print camPath, os.path.exists(camPath)
		c = nuke.createNode('Camera2')
		c['read_from_file'].setValue(True)
		c['file'].setValue(camPath.replace('\\', '/'))
		c['frame_rate'].setValue(24)
		c['label'].setValue("%s v%s" % (shot.upper(), ver))
		c['tile_color'].setValue(1784020991)