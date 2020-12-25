import os, sys
import nuke
import time
import socket
# t = time.time()
#nuke.pluginAddPath('X:/app/win/Pipeline')
paths = ['X:/app/win/Pipeline', 'X:/app/win/Pipeline/uis222', 'X:/app/win/Pipeline/p_utils', 'X:/app/win/Pipeline/bot']

for path in paths:
	if not path in sys.path:
		sys.path.append(path)

os.environ['OFX_PLUGIN_PATH'] = 'X:/app/win/Pipeline/nuke/ofx'

if nuke.GUI:
	from getpass import getuser

	cwd = os.path.dirname(__file__)
	gizmosPath = os.path.join(cwd, 'gizmos')
	pyPath = os.path.join(cwd, 'python')
	toolsetsPath = os.path.join(cwd, 'toolsets')
	iconsPath = os.path.join(cwd, 'icons')
	hotboxPath = os.path.join(cwd, 'hotbox')
	libPath = os.path.join(cwd, 'lib').replace('\\', '/')


	#hotboxPath = os.path.join(cwd, 'Python/hotbox')
	#timelog = os.path.join(cwd, 'Python/timelog')

	bgBokehPath = os.path.join(cwd, 'python', 'Bokeh-v1.4.6')
	cryptoPath = os.path.join(cwd, 'python', 'cryptomatte') #cryptoPath,
	survivalKit = os.path.join(cwd, 'python', 'NukeSurvivalToolkit')

	nuke.tprint('PATHS ADDING:')
	for i in (gizmosPath, pyPath, iconsPath, hotboxPath, libPath, cryptoPath, './python/dNoice', './python/shared_toolsets', './python/split_layers', './Gizmos/autoinstal', './Gizmos/VectorInstal', './OpticalFlares', './nukeExternalControl', './pw_multiScriptEditor', './lenses'):
		nuke.tprint('\t %s' % str(i))
		nuke.pluginAddPath(i)
	import CUF

	# t = CUF.noteTime(t, 'before import 1')
	#import callbacks #callback in it (disabled)
	import scripts
	import Points3DToTracker
	import Pto2dTrack
	import W_scaleTree
	import batchrenamer
	import CornerPinStabilMM
	import knobExpressionCurve
	import HouAxisToNuke
	import animatedSnap3D
	import autolife
	import rerenderMissingFrames
	import deepDefocusSlicer
	import deleteFilesFromWrite

	# t = CUF.noteTime(t, 'before import 2')
	import LH
	import OhuIO
	import CUF
	import cornerPinToTracker
	import duplicator
	import CardtoTrack
	import RAWtoJPEG
	import Equalizer2dPointToNuke
	import EqualizerTrack
	import viewerInputNodes
	#import W_hotbox
	import mirrorNodes
	import setMixAnimation
	import premultRotoWithBBox
	import branch
	import lookAt
	import addMultKnob 
	import ibkStackTechnique
	import addconstraintab
	import collectFiles
	import gizmos as gzm
	import channelHotbox
	import channelSplit_2
	import autoComper
	import pass_sep
	import split_layers
	import createReadFromWrite
	import folderImport

	# t = CUF.noteTime(t, 'before import 3')
	import PL_scripts
	import PL_callbacks
	import PL_writeChecks
	import toolsets_loader

	import viewerBinding
	import nk_filemanager3

	for i in (0.3, 0.5, 0.6, 0.7, 0.8, 0.8, 1):
	  nuke.addFormat("%s %s -.- %s" % (int(2048*i), int(858*i), i)) #ceil
	nuke.addFormat( '2048 858 0 0 2048 858 1 2.39 Aspect' )
	nuke.addFormat('3200 1800 0 0 3200 1800 1 PL 3k')

	# nuke.knobDefault('Read.raw', 'True')
	nuke.knobDefault('Shuffle.label', "[knob in]")
	nuke.knobDefault('ShuffleCopy.label', "[knob in]")
	#nuke.knobDefault('Merge2.bbox', "B")
	nuke.knobDefault('AdjBBox.numpixels', '10')
	nuke.knobDefault('Switch.which', '1')
	nuke.knobDefault('Reformat.filter', 'Cubic')
	nuke.knobDefault('Read.auto_alpha', 'True')
	nuke.knobDefault('RotoPaint.toolbar_lifetime_type', '0')
	nuke.knobDefault('OFXuk.co.thefoundry.tinderbox3.t_mattetool_v201.radius', '0')
	nuke.knobDefault('OFXuk.co.thefoundry.tinderbox3.t_mattetool_v201.processRed', '0')
	nuke.knobDefault('OFXuk.co.thefoundry.tinderbox3.t_mattetool_v201.processGreen', '0')
	nuke.knobDefault('OFXuk.co.thefoundry.tinderbox3.t_mattetool_v201.processBlue', '0')
	nuke.knobDefault('LayerContactSheet.showLayerNames', 'True')
	nuke.knobDefault('Constant.channels', 'rgba')
	nuke.knobDefault('Tracker4.label', '[knob transform] [knob reference_frame]')
	nuke.knobDefault('Tracker3.label', '[knob transform] [knob reference_frame]')
	nuke.knobDefault('Soften.channels', 'rgba')
	#nuke.knobDefault('Write.beforeRender', "if not os.path.exists(os.path.dirname(nuke.thisNode()['file'].value())): os.makedirs(os.path.dirname(nuke.thisNode()['file'].value()))")
	nuke.knobDefault('Write.beforeRender', "PL_writeChecks.checkBeforeRender()")
	nuke.knobDefault('Remove.operation', 'keep')
	nuke.knobDefault('Remove.channels', 'rgba')
	nuke.knobDefault('PositionToPoints2.P_channel', 'P')
	nuke.knobDefault('PositionToPoints2.N_channel', 'N')
	nuke.knobDefault('PositionToPoints2.render_mode', 'off')
	nuke.knobDefault('P_Matte.gizmo.p_matte_in', 'P')



	nuke.addOnUserCreate(LH.frameHoldSet, nodeClass="FrameHold") 
	nuke.addOnUserCreate(LH.setAlphaChannel, nodeClass="Blur")
	nuke.addOnUserCreate(LH.setAlphaChannel, nodeClass="Dilate")
	nuke.addOnUserCreate(LH.setAlphaChannel, nodeClass="Roto")

	nuke.addOnUserCreate(LH.addOpenEButton, nodeClass='Read')
	nuke.addOnUserCreate(LH.addCreateReadFromWriteButton, nodeClass='Write')
	nuke.addOnUserCreate(LH.addOpenEButton, nodeClass='Write')

	# if socket.gethostname() == 'sashok':
	# 	nuke.addKnobChanged(PL_callbacks.readFileKnobChanged, nodeClass="Read")
	# 	#nuke.addOnUserCreate(PL_callbacks.readChangeFileKnob, nodeClass="Read")
	# 	nuke.addUpdateUI(PL_callbacks.updateUiForRead, nodeClass="Read")

	nuke.toNode('preferences')['maxPanels'].setValue(1)
	# t = CUF.noteTime(t, 'end')

	nuke.addOnScriptLoad(PL_callbacks.updateWriteBeforeRenderPython, nodeClass="Write")
	nuke.addOnScriptLoad(PL_callbacks.marikLut)