import nuke
from PL_scripts import inPipeline, getPipelineAttrs, addFavoriteFolders, labelRender
import PL_rootPipelineStuff
from p_utils.csv_parser_bak import projectDict

def testCallback():
	if inPipeline():
		root = nuke.root()
		addFavoriteFolders([root['project'].value(), root['shot'].value()])
	else:
		print "NOT A PIPELINE SCENE"

def fixProjectShotAttr():
	# PREVENTS FROM EMPTY SHOT AND PROJECT KNOBS IN ROOT BY REFILLINGS THEM
	if inPipeline():
		print "FIXING ROOT FROM CALLBACK"
		if nuke.root()['shot'].value() == '':
			PL_rootPipelineStuff.fixRootTab(assignShotInfo = True)
	else:
		print "NOT A PIPELINE SCENE"

def set24fps():
	nuke.root()['fps'].setValue(24)
	print 'Scene fps set to 24'

def fixNonACESscene():
	try:
		drive, project, seq, shot, ver = getPipelineAttrs()
		exceptShots = ['sh000', 'sh060', 'sh120', 'sh130', 'sh020']
		if shot not in exceptShots and nuke.root()['colorManagement'].value() == 'Nuke':
			root = nuke.root()
			root['colorManagement'].setValue('OCIO')
			root['OCIO_config'].setValue('aces_1.0.1')
			root['monitorLut'].setValue('ACES/Rec.709')

			for n in nuke.allNodes('Viewer'):
				nuke.delete(n)

			v = nuke.createNode('Viewer')
			v['viewerProcess'].setValue('Rec.709')

			for w in nuke.allNodes('Write'):
				if w['tile_color'].value() == 255 and '.dpx' in w['file'].value():
					nuke.message('Recreate Hires write')
	except:
		print 'Non pipeline script'

def setInOutFrames():
	try:
		drive, project, seq, shot, ver = getPipelineAttrs()
		p = projectDict('Arena')
		first = p.getSpecificShotData(seq, shot, 'first_frame')
		last = p.getSpecificShotData(seq, shot, 'last_frame')

		#print first, last

		r = nuke.root()
		r['first_frame'].setValue(int(first))
		r['last_frame'].setValue(int(last))
		print 'first and last frames were set to %s and %s' % (first, last)
	except:
		print 'Non pipeline script'

#rules = {'render':}

def readFileKnobChanged():
	k = nuke.thisKnob()
	#nuke.tprint('knob changed\n%s' % k.value())
	if k.name() == 'file':
		f = nuke.thisNode()['file'].value()
		n = nuke.thisNode()
		if '/render/' in f:
			labelRender([n])
			n['colorspace'].setValue('ACES - ACEScg')
		elif 'forDaily' in f:
			n['colorspace'].setValue('Output - Rec.709')
		elif 'src' in f:
			labelRender([n])

def updateUiForRead():
	f = nuke.thisNode()['file'].value()
	n = nuke.thisNode()
	#nuke.tprint('upfate UI\n%s' % f)
	if '/render/' in f:
		labelRender([n])
		n['colorspace'].setValue('ACES - ACEScg')
	elif 'forDaily' in f:
		pass
		#n['colorspace'].setValue('Output - Rec.709')
	elif 'src' in f:
		labelRender([n])

def updateWriteBeforeRenderPython():
	n = nuke.thisNode()
	nuke.tprint('CALLBACK :: update write before render python :: %s' % n.name())
	if 'forDaily' in n['file'].value():
		nuke.tprint('CALLBACK :: in 1')
		if "if not os.path.exists(os.path.dirname(nuke.thisNode()['file'].value())): os.makedirs(os.path.dirname(nuke.thisNode()['file'].value()))" in n['beforeRender'].value():
			nuke.tprint('CALLBACK :: in 2')
			n['beforeRender'].setValue('PL_writeChecks.checkBeforeRender()')

def marikLut():
	#print 'IN MARIK LUT CALLBACK'
	root = nuke.root()

	# VIEWERS SETUP
	if 'UnderTheSea' in root['project'].value():
		vv = [i for i in nuke.allNodes() if i.Class() == 'Viewer']
		for v in vv:
			print v['viewerProcess'].setValue('Rec.709 D60')

	# DAILY WRITES
	ww = [i for i in nuke.allNodes() if i.Class() == 'Write' and '/forDaily/' in i['file'].value()]
	for w in ww:
		# print w['colorspace'].value()
		w['colorspace'].setValue('Output - Rec.709')
