import socket
import getpass
#import W_hotbox
import AnimationMaker

user_id = socket.gethostname()
username = getpass.getuser()

toolbar = nuke.menu("Nuke")
menubar = nuke.menu("Nodes");
m = toolbar.addMenu("&File")
n = toolbar.addMenu("&Edit")
n.addCommand("&Branch", "branch.branch()", "#b")
toolsets_path = 'O:/compToolsets'

# CREATING A LITTLE HELPERS MENU
mymenulh = menubar.addMenu('Little Helpers',icon="Chinaface.png") 
mymenulhUnsued = mymenulh.addMenu('Unused', icon ="08 Music.png")
mymenulhUnsued.addCommand('Set Reads Ranges', 'LH.setRangeForReads()', icon='SetReadRanges.png')
mymenulhUnsued.addCommand('Set Reads Before After BLACK', 'LH.setBeforeAfter("black")')
mymenulhUnsued.addCommand('Set Reads Before After HOLD', 'LH.setBeforeAfter("hold")')
mymenulhUnsued.addCommand('Supressor GREEN', 'nuke.nodes.Expression(expr1="g > (r+b)/2 ? (r+b)/2 : g)", name="Color Supressor", label="GREEN")', icon='SupressorGreen.png')
mymenulhUnsued.addCommand('Supressor BLUE', 'nuke.nodes.Expression(expr2="b > (r+g)/2 ? (r+g)/2 : b))", name="Color Supressor", label="BLUE")', icon='SupressorBlue.png')
#mymenulh.addCommand('TFX Begin Shot', 'filmuaWinPipeline.beginShot()', 'F9', icon='beginShot.png')
mymenulh.addCommand('Toggle Viewer Inputs', 'LH.toggleViewerInput()', 'shift+return', icon='ToggleViewerInput.png')
mymenulh.addCommand('Toggle Selected Input', 'LH.toggleSelectedInput()', 'j', icon='ToggleSelectedInput.png')
mymenulh.addCommand('LineUp selected Nodes', 'LH.lineupNodes()', 'shift+l')
mymenulh.addCommand('LineDown selected Nodes', 'LH.linedownNodes()', 'ctrl+l')
#mymenulh.addCommand('Toggle Merge', 'LH.toggleMerge()', '`')   # ```````````````````````````
mymenulh.addCommand('Link MB', 'LH.linkMB()')
mymenulhUnsued.addCommand('Disable Selected Node', 'LH.ToggleSelNode()') # ```````````````````````````
mymenulh.addCommand('Reload Reads', 'LH.reloadReads()', icon = '14 Reboot.png')
mymenulhUnsued.addCommand('Set Empty Read Labels', 'LH.setLabelEmpty()', icon = '11 Trash Empty.png') 
mymenulhUnsued.addCommand('Set Read Labels', 'LH.setReadLabel()', icon='12 Trash Full.png')
mymenulh.addCommand('FLIP-FLIP', 'LH.mirrorViewer()', 'F2')
mymenulhUnsued.addCommand('Scale Up Selected Nodes', 'LH.scaleNodes(1.1)', ',')
# mymenulh.addCommand('Shot Setup', 'LH.shotSetup()', icon='05 Folder.png')
mymenulh.addCommand('Autocrop', "frames = nuke.getInput('Set Frame Range', '%s-%s' % (int(nuke.root()['first_frame'].value()), int(nuke.root()['last_frame'].value()))).split('-')\nprint frames\nnukescripts.autocrop(first = int(frames[0]), last = int(frames[1]), layer = 'alpha')", 'F4', icon='20_Avast.png')
mymenulhUnsued.addCommand('Collect Files', 'collectFiles.collectFiles()')
mymenulh.addCommand('Colorize Backdrop Nodes', 'LH.colorizeBackdrops()')
mymenulh.addCommand('Colorize Sticky Notes', 'LH.colorizeStickyNotes()')
mymenulh.addCommand('cornerPinToTracker', 'cornerPinToTracker.cornerPinToTrackerRefresh()', 'ctrl+shift+m', icon = 'mocha.png')
mymenulhUnsued.addCommand('3 Color Gradient', 'nuke.createNode("ColorGradient")')
mymenulh.addCommand('Delete Error Reads', 'LH.deleteErrorReads()', 'F3', icon = '13 Shut Down.png')
mymenulh.addCommand('Set Reads to sRGB', 'LH.sRGBReads()', 'F6', icon='sRGB.png')
mymenulh.addCommand('Arrange', 'LH.arrange()')
mymenulh.addCommand('f_Steadines to CornerPin', 'LH.fSteadinessToCornerPin()')
mymenulhUnsued.addCommand('Command Line Render', 'CmdLineRender.CLrender()')
mymenulhUnsued.addCommand('Save Frame', 'saveFrame.saveFrame()' , icon='saveFrame.png')
# mymenulh.addCommand('Backdrop Merge Inputs', 'LH.backdropMergeInputs()')
mymenulhUnsued.addCommand('Project Folders Creator', 'projectFoldersCreator.projectFoldersCreator()')
mymenulh.addMenu('Duplicator')
mymenulh.addCommand('Duplicator/Duplicator', 'duplicator.mainFuncDuplicator()', 'shift+e', icon = 'Star.png')
mymenulh.addCommand('Duplicator/Create Duplicator Knobs (No copying)', 'duplicator.createDuplicatorKnobs(nuke.selectedNode())')
mymenulh.addCommand('Duplicator/Delete duplicator Stuff', 'duplicator.deleteDuplicatorStuff()')
mymenulh.addCommand('Create Proxy', 'duplicator.createProxy(duplicator.getNodeList())')
#mymenulhUnsued.addCommand('Shot Setup', 'shotSetup.shotSetupMainFunc()')
#menubar.addCommand('Duplicator', 'duplicator.mainFuncDuplicator()',  'shift+e',icon = 'Star.png')
mymenulhUnsued.addCommand('Cut edit/From EDL file', 'cutEdit.mainFunc("edl")')
mymenulhUnsued.addCommand('Cut edit/Recognize Cutds', 'cutEdit.mainFunc("rCuts")')
mymenulh.addCommand('Card to Track','CardtoTrack.corn3D()',icon="Camera.png")
mymenulh.addCommand('Split EXR','channelSplit_2.channelSplit(nuke.selectedNode())')
mymenulh.addCommand('Split Arnold Exr','channelSplit_2.arnoldComposite(nuke.selectedNode())', icon = 'Arnold.png')
mymenulhUnsued.addCommand('Flip And Write','flipAndWrite.flipAndWrite(nuke.selectedNodes("Read"))')
mymenulh.addCommand('Rerender EXRs','EXRosl.exrosl(nuke.selectedNodes("Read"), False, False)', 'f10')
mymenulhUnsued.addCommand('RAW to JPEGs (dva Ivana)','RAWtoJPEG.main()')
mymenulh.addCommand('Equalizer 2d Points import (all)','Equalizer2dPointToNuke.main(4)', icon='Eq_2d.png')
mymenulh.addCommand('Equalizer 2d Points import (4 points)','Equalizer2dPointToNuke.main(3)', icon='Eq_2d_4.png')
mymenulh.addCommand('Import Equalizer Track','EqualizerTrack.importScript()', icon='Eq_3d.png')
mymenulh.addCommand("Value Panel", 'valuePanel.getValues()')
mymenulh.addCommand("Wave Panel", 'wavePanel.go()', icon="wavePanel.png")
mymenulh.addCommand("Render Selected Nodes (input frames)", 'LH.renderWrites()', icon="write.png")
mymenulh.addCommand("Render Selected Nodes (global frames)", 'LH.renderWrites(True)', icon="write.png")
mymenulh.addCommand("Offset Padding of folder", 'offsetPadding.offsetPaddingInFolder()')
mymenulh.addCommand("Offset Padding of project\sequence\shot", 'offsetPadding.offsetPaddingFromAbstractPath()')
mymenulh.addCommand("Create Axis From Selected 3d Point", 'Points3DToTracker.createAxis()', 'shift+a')
mymenulh.addCommand("Create Tracker from 3d Points", 'Points3DToTracker.reconcileFrom_4_Axis()', 'ctrl+t')
mymenulh.addCommand("Copy Traking Data to Roto", 'Points3DToTracker.copyTrackingToRoto(True)', 'shift+b')
mymenulh.addCommand("Split ABC", 'LH.splitMultipleAbc()')
#mymenulh.addCommand("Autolife selected shape (roto)", 'autolife.autolifeSelectedShape()', 'shift+w')
mymenulh.addCommand("Normalizer Depth", 'LH.normalizeDepth()', icon = "NormalizeDepth.png")
mymenulh.addCommand("Normalizer RGB", 'LH.normalizeRGB()', icon = "normalizeRGB.png")
mymenulh.addCommand("Create TFX proxy", 'tfxWinPipeline.createProxy()')
#mymenulh.addCommand("Create TFX prerender", 'tfxWinPipeline.createPrerender()', 'F8')
mymenulh.addCommand("Viewer to RGBA", "v = nuke.activeViewer().node().name()\nnuke.toNode(v)['channels'].setValue('rgba')", 'ctrl+`')
#mymenulh.addCommand("Clipboard Link", 'dropLink.TFXDropAction()')
mymenulh.addCommand("CornerPin Stabilize Match-Move", 'CornerPinStabilMM.createKnobs()')
mymenulh.addCommand("Create TFX Slate", 'TFX_slate.mainFunc()', icon = 'TFXSlate.png')
mymenulh.addCommand("Create Master Folders", 'tfxWinPipeline_CreateMasterFolders.createMasterFolders()')
#mymenulh.addCommand("Platform based Switch READ paths", 'LH.platformBasedSwitchReadPath()')
mymenulh.addCommand("Switch to PC version", 'LH.platformBasedSwitchReadPath("pc")')
mymenulh.addCommand("Switch to linux version", "LH.platformBasedSwitchReadPath('linux')")
#mymenulh.addCommand("Find Gizmos", 'LH.findGizmos()')
#mymenulh.addCommand("Convert Gizmos to Groups", 'LH.convertGizmosToGroups()')
mymenulh.addCommand("Send to Platform", 'LH.sendToPlatform()')
mymenulh.addCommand("Save Path Switch", 'LH.saveSwitch()', 'f10')
mymenulh.addCommand('Toggle ovelays', "nuke.menu('Viewer').findItem('Overlay').invoke()", '`')
mymenulh.addCommand('Rerender file (exr, jpg, png)', "rerenderHeavyReads.rerenderMainFunc()", 'alt+r')
mymenulh.addCommand('Mirror nodes', "mirrorNodes.mirrorNodes()")
mymenulh.addCommand('Rename Mocha CornerPins', "CUF.renameMochaCornerPin()")
mymenulh.addCommand('Increment save [FILM.UA]', "filmuaWinPipeline.saveNewVersion()")
mymenulh.addCommand('Set Mix Animation', "setMixAnimation.setMix()")
mymenulh.addCommand('CP BBox', "premultRotoWithBBox.cornerPinFromBBox()")
mymenulh.addCommand('Toggle SPECIAL node', "LH.toggleSpecialNode()", 'alt+`')
mymenulh.addCommand('Make this node SPECIAL', "LH.makeThisNodeSpecial()", 'shift+ctrl+`')
mymenulh.addCommand('Stack IBK colour diplicate', "ibkStackTechnique.ibkStackDuplicate()")
mymenulh.addCommand('Create LOOK AT knob', "addconstraintab.constrain()")
mymenulh.addCommand('Shift nodes down', "LH.shiftNodes('down')", 'shift+down')
mymenulh.addCommand('Shift nodes up', "LH.shiftNodes('up')", 'shift+up')
#mymenulh.addCommand('Precomp create', "createPrerender.createPrerender()")
# mymenulh.addCommand('Render Version UP', 'renderVersioning_v02.Versioning("s", verUp = True)', 'f10')
# mymenulh.addCommand('Render Version DOWN', 'renderVersioning_v02.Versioning("s", verUp = False)', 'f9')
#mymenulh.addCommand('Rerender Missing Frames', 'rerenderMissingFrames.rerenderMissedFrame()')
#mymenulh.addCommand('Shot Setup', 'ShotAndViewerSetup.createShotSetup()')	
mymenulh.addCommand('Look At', 'lookAt.makeAimConstrain(nuke.selectedNodes())')
mymenulh.addCommand('Clear cache', 'nukescripts.cache_clear('')', shortcutContext = 1) # @param shortcutContext: Optional. Sets the shortcut context (0==Window, 1=Application, 2=DAG).
mymenulh.addCommand('Artistic tile color', 'CUF.makeAtristicTielColors()')
mymenulh.addCommand('Color Nodes', 'LH.colorNodes()', 'ctrl+alt+c')
mymenulh.addCommand("Cryptomatte", "import cryptomatte_utilities as cu; cu.cryptomatte_create_gizmo();", 'shift+c')
if user_id == 'sashok':
	mymenulh.addCommand("Copy Node's color", 'LH.copyColor()', 'alt+c')
	

# def callShotScripts():
# 	import PL_shotScripts
# 	try:
# 		del(so)
# 	except:
# 		pass
# 	global so
# 	reload(PL_shotScripts)
# 	so = PL_shotScripts.shotScripts()
# 	so.show()
#mymenulh.addCommand('Shot opener', "import PL_shotOpener\nreload(PL_shotOpener)\nso = PL_shotOpener.shotOpener()\nso.show()", 'f8')
#mymenulh.addCommand('Filemanager', "import nk_filemanager\nreload(nk_filemanager)\nf = nk_filemanager.NukeManager()\nf.show()", 'f8')
#mymenulh.addCommand('Filemanager v2', "import nk_filemanager2\nreload(nk_filemanager2)\nf = nk_filemanager2.NukeManager()\nf.show()", 'ctrl+f8')
mymenulh.addCommand('Filemanager v3', "import nk_filemanager3\nreload(nk_filemanager3)\nf = nk_filemanager3.NukeManager()\nf.show()", 'f8')
#mymenulh.addCommand('Shot opener test', "import PL_shotOpener_nextgen\nreload(PL_shotOpener_nextgen)\nso = PL_shotOpener_nextgen.shotOpener()\nso.show()", 'f7')
mymenulh.addCommand('Toolset Loader', "import toolsets_loader\nreload(toolsets_loader)\nt = toolsets_loader.AssetsLoader()\nt.show()", 'f7')
mymenulh.addCommand('Toolset Create', "import toolsets_loader\nreload(toolsets_loader)\ntlc = toolsets_loader.toolsetCreate()\ntlc.show()", 'shift+f7')
mymenulh.addCommand('Shot Scripts', "import PL_shotScripts\nreload(PL_shotScripts)\nglobal ss\nss = PL_shotScripts.shotScripts()\nss.show()\nprint 'done'", 'f9')
mymenulh.addCommand('Glezin Channel Splitter', "import split_layers\nsplit_layers.main()", 'f10')
mymenulh.addCommand('All Scripts', "import PL_scriptsWindow02\nreload(PL_scriptsWindow02)\nglobal sw\nsw = PL_scriptsWindow02.scriptsWindow()\nsw.show()", 'shift+f10')
mymenulh.addCommand('Render Vmax', "import PL_scripts\nreload(PL_scripts)\nPL_scripts.renderVerMax()", 'f11')
mymenulh.addCommand('ACES converters', "PL_scripts.createACESconverters()", 'f12')
mymenulh.addCommand('Call Exr Info Pallete', "nuke.loadToolset('%s/basic/ExrInfoPallete.nk' % toolsets_path)", 'shift+f12')
	
mymenulh.addCommand("afanasy from writes", 'LH.afanasyFromWrites()')
mymenulh.addCommand("execute afanasy nodes", 'LH.executeAfanasyNodes()')
mymenulh.addCommand("find reduce noise", 'LH.findReducenoise()')
#mymenulh.addCommand("Find Shot", 'LH.findReadWithPattern()', 'f6')
mymenulh.addCommand("HotBox", 'reload(channelHotbox)\nchannelHotbox.start()', "alt+q")
mymenulh.addCommand('autoComper', 'autoComper.autoComper()', icon='autoComper.png')
mymenulh.addCommand('Pass Separator', "pass_sep.callPassSep()", '^+a', icon='Pass_Sep.png')
mymenulh.addCommand('Split EXR Glezin', "split_layers.main()")


# ASSIGNING A HOTKEY
if (user_id != 'paul') and (username != 'd.ovcharenko'):
	nuke.menu('Nodes').addCommand('Channel/ChannelMerge', 'nuke.createNode("ChannelMerge")', 'ctrl+shift+c', icon='ChannelMerge.png')
	nuke.menu('Nodes').addCommand('Merge/Premult', 'nuke.createNode("Premult")', 'y', icon='Premult.png')
	nuke.menu('Nodes').addCommand('Merge/Unpremult', 'nuke.createNode("Unpremult")', 'shift+y', icon='Unpremult.png')
	nuke.menu('Nodes').addCommand('Other/Expression', 'nuke.createNode("Expression")', 'e',)
	nuke.menu('Nodes').addCommand('Channel/Shuffle', 'nuke.createNode("Shuffle")', 'h', icon='Shuffle.png', shortcutContext = 2)
	nuke.menu('Nodes').addCommand('Channel/ShuffleCopy', 'nuke.createNode("ShuffleCopy")', 'shift+h', icon='ShuffleCopy.png')
	nuke.menu('Nodes').addCommand('Transform/Reformat', 'LH.createReformat()', 'shift+r', icon='Reformat.png')
	nuke.menu('Nodes').addCommand('Transform/Crop', 'nuke.createNode("Crop")', 'ctrl+r', icon='Crop.png')
	nuke.menu('Nodes').addCommand('Transform/Tracker', 'nuke.createNode("Tracker4")', 'v', icon='Tracker.png', shortcutContext = 2)
	nuke.menu('Nodes').addCommand('Transform/Tracker v6', 'nuke.createNode("Tracker3")', 'shift+v', icon='Tracker.png')
	#nuke.menu('Nodes').addCommand('Color/ColorLookup', 'nuke.createNode("ColorLookup")', 'shift+c', icon='ColorLookup.png')
	nuke.menu("Nodes").addCommand("Other/Keyer Bind", "nuke.createNode('Keyer')", 'z', icon='Keyer.png')
	nuke.menu("Nodes").addCommand("Merge/KeyMix", "nuke.createNode('Keymix')", 'ctrl+shift+d', icon='KeyMix.png')
	nuke.menu("Nodes").addCommand("Other/Backdrop", "nukescripts.autoBackdrop()", 'shift+z', icon='Backdrop.png')
	nuke.menu('Nodes').addCommand('Image/CheckerBoard', 'nuke.createNode("CheckerBoard2")', 'shift+q', icon='CheckerBoard2.png')
	nuke.menu('Nodes').addCommand('Image/Constant', 'nuke.createNode("Constant")', 'q', icon='Constant.png')
	nuke.menu('Nodes').addCommand('Merge/Merges/Multiply', 'nuke.createNode("Multiply")', 'n', icon='Merge.png')
	nuke.menu('Nodes').addCommand('Merge/Merges/Plus', 'nuke.createNode("Merge2", "operation plus name Plus", False)', 'shift+n', icon='Merge.png')
	nuke.menu('Nodes').addCommand('Merge/Merges/Stencil', 'nuke.loadToolset("%s/basic/Stencil.nk" % toolsets_path)' , 'shift+m', icon='Merge.png')
	nuke.menu('Nodes').addCommand('Merge/Merges/Mask', 'nuke.loadToolset("%s/basic/mask.nk")' % toolsets_path, 'ctrl+m', icon='Merge.png')
	nuke.menu('Nodes').addCommand('Merge/Merges/Mask with bbox', 'premultRotoWithBBox.createSubset()', 'alt+o', icon='Merge.png')
	nuke.menu('Nodes').addCommand('Draw/Roto Premult', 'LH.createRotoPremult()', 'shift+o', icon='Roto.png')
	nuke.menu('Nodes').addCommand('Time/Time Offset', 'LH.createTimeOffset()', 'shift+t', icon='TimeOffset.png')
	nuke.menu('Nodes').addCommand('Filter/Erode (fast)', 'nuke.createNode("Erode")', 'ctrl+e', icon='Dilate.png')
	nuke.menu('Nodes').addCommand('Filter/Erode (filter)', 'nuke.createNode("FilterErode")', 'ctrl+shift+e', icon='Dilate.png')

	nuke.menu('Nodes').addCommand('Time/FrameHold', 'nuke.createNode("FrameHold")', 'shift+f', icon='FrameHold.png')
	#premult_roto_with_bbox

	menu = nuke.menu('Nuke')
	menu.addCommand('Nodes/Autoplace', 'LH.autoplace()', 'l')
else:
	print '+++ No hotkey has been assigned'

gzm.main(['X:/app/win/nuke/gizmos/autoinstal'])


########################


cwd = os.path.dirname(__file__)

gizmosPath = os.path.join(cwd, 'Gizmos')
pyPath = os.path.join(cwd, 'Python')
toolsetsPath = os.path.join(cwd, 'Toolsets')
iconsPath = os.path.join(cwd, 'Icons')

pnsmenu = nuke.menu('Nodes').addMenu('PNS', icon = 'Chinaface.png')
pnsGizmosMenu = pnsmenu.addMenu('Gizmos')
toolsetsMenu = pnsmenu.addMenu('Toolsets')
pyMenu = pnsmenu.addMenu('Python')

#FORMATS
nuke.addFormat( '2880 2160 0 0 2880 2160 2 AlexaXT Anamorph' )
nuke.addFormat( '2880 1080 0 0 2880 1080 1 AlexaXT Squeezed' )

#GIZMOS
for p in os.listdir(gizmosPath):
    #nuke.tprint(p)
    if '.gizmo' in p:
        name = p.replace('.gizmo', '')
        #print name
        if 'PxF' in name:
            #nuke.tprint('%s with PxF inside' % name)
            pnsGizmosMenu.addCommand('PxF/%s' % name, 'nuke.createNode("%s")' % p)
        else:
            pnsGizmosMenu.addCommand('%s' % name, 'nuke.createNode("%s")' % p)
    elif 'deprecated' in p:
        pass
    elif os.path.isdir('/'.join([gizmosPath, p])):
        #nuke.tprint('%s dir found' % p)
        pnsGizmosMenu.addMenu(p)
        for e in os.listdir('/'.join([gizmosPath, p])):
            if '.gizmo' in e:
                pnsGizmosMenu.addCommand('%s/%s' % (p, e), 'nuke.createNode("%s")' % '/'.join([gizmosPath, p, e]))


#TOOLSETS
toolsetException = ['~', 'SkyOverlay']
for t in os.listdir(toolsetsPath):
    add = True
    for i in toolsetException:
        if i in t:
            add = False

    if add:
        name = t.replace('.nk', '')
        toolsetsMenu.addCommand(name, 'nuke.loadToolset("%s")' % os.path.join(toolsetsPath, t))

#PY
try:
	pyMenu.addCommand('Find and convert gizmos to groups', 'scripts.findAndConvertGizmosToGroups()')
	pyMenu.addCommand("Create Tracker from 3d Points", 'Points3DToTracker.reconcileFrom_4_Axis()', 'ctrl+t')
	pyMenu.addCommand("Copy Traking Data to Roto", 'Points3DToTracker.copyTrackingToRoto(True)', 'shift+b')
	pyMenu.addCommand('Set Reads to sRGB', 'scripts.sRGBReads()', 'F6')
	pyMenu.addCommand('Axis from 2dPos', 'Pto2dTrack.positionNodeCreate()')
	if socket.gethostname() == 'sashok':
	    pyMenu.addCommand('W_scaleTree', 'W_scaleTree.scaleTreeFloatingPanel()', 'f5')
	else:
	    pyMenu.addCommand('W_scaleTree', 'W_scaleTree.scaleTreeFloatingPanel()')
	pyMenu.addCommand('Unlock Knobs', 'scripts.unlockKnobs()')
	pyMenu.addCommand('Rename Mocha CornerPins', "scripts.renameMochaCornerPin()")
	pyMenu.addCommand("CornerPin Stabilize Match-Move", 'CornerPinStabilMM.createKnobs()')
	pyMenu.addCommand('CornerPin To Tracker', 'cornerPinToTracker.cornerPinToTracker()', 'ctrl+shift+m', icon = 'mocha.png')
	pyMenu.addCommand("Line up nodes verticaly", 'scripts.lineupNodes()', 'shift+l')
	pyMenu.addCommand("Line up nodes horizontaly", 'scripts.linedownNodes()', 'ctrl+l')
	pyMenu.addCommand("Autoplace", 'scripts.autoplace()', 'l')  
	pyMenu.addCommand('Batch renamer', 'import batchrenamer; batchrenamer.main()')
	pyMenu.addCommand('import Houdini axis', 'HouAxisToNuke.importHouAxis()')
	pyMenu.addCommand('Find gizmos', 'scripts.findGizmos()')
	pyMenu.addCommand('Convert Gizmos to Groups', 'scripts.convertGizmosToGroups()')
	#pyMenu.addCommand('AutoBBox', 'nuke.createNode("%s/autoBBox.gizmo" % gizmosPath)', 'F4')
	pyMenu.addCommand("Autolife selected shape (roto)", 'autolife.autolifeSelectedShape()', 'shift+w', shortcutContext = 1)
	pyMenu.addCommand("afanasy from writes", 'scripts.afanasyFromWrites()') 
	pyMenu.addCommand("execute afanasy nodes", 'scripts.executeAfanasyNodes()')
	pyMenu.addCommand("Rerender Missing Frames", 'rerenderMissingFrames.rerenderMissedFrame()')
	pyMenu.addCommand("Import multiple abc cameras", 'scripts.splitCamsFromAbc(nuke.getFilename("'"Select an .abc file"'"))')
	pyMenu.addCommand("Deep Defocus Slicer", 'deepDefocusSlicer.deepDefocus()')
	pyMenu.addCommand("Delete Files from Write path", 'deleteFilesFromWrite.deleteFilesFromWritePath(nuke.selectedNode())')
	pyMenu.addCommand("Folder Import", 'folderImport.seqloader()', 'alt+r')


	m = nuke.menu('Nodes').addMenu('PNS/Python/AnimatedSnap3d')
	m.addCommand('Match position - ANIMATED', 'animatedSnap3D.translateThisNodeToPointsAnimated()')
	m.addCommand('Match position, orientation - ANIMATED', 'animatedSnap3D.translateRotateThisNodeToPointsAnimated()')
	m.addCommand('Match position, orientation, scale - ANIMATED', 'animatedSnap3D.translateRotateScaleThisNodeToPointsAnimated()')


	nuke.tprint('PNS menu.py is loaded correctly.')
except:
    nuke.tprint('PNS menu.py has not been loaded correctly')

#VIEWER BINDS
# for i in xrange(10):
# 	pyMenu.addCommand('Set input attr to %s' % str(i), 'viewerBinding.addInputAttr(nuke.selectedNode(), %s)' % str(i), 'ctrl+%s' % str(i))
#nuke.addOnCreate(viewerBinding.connectViewer, nodeClass="Viewer")

#nk_filemanager
#nuke.addOnScriptLoad(nk_filemanager3.sceneUnwrap)

#CALLBACKS
#nuke.addOnScriptLoad(PL_scripts.addFavoriteFolders)

# 3DE
nuke.menu("Nodes").addCommand("3DE4/LD_3DE4_Anamorphic_Standard_Degree_4", "nuke.createNode('LD_3DE4_Anamorphic_Standard_Degree_4')")
nuke.menu("Nodes").addCommand("3DE4/LD_3DE4_Anamorphic_Rescaled_Degree_4", "nuke.createNode('LD_3DE4_Anamorphic_Rescaled_Degree_4')")
nuke.menu("Nodes").addCommand("3DE4/LD_3DE4_Anamorphic_Degree_6", "nuke.createNode('LD_3DE4_Anamorphic_Degree_6')")
nuke.menu("Nodes").addCommand("3DE4/LD_3DE4_Radial_Standard_Degree_4", "nuke.createNode('LD_3DE4_Radial_Standard_Degree_4')")
nuke.menu("Nodes").addCommand("3DE4/LD_3DE4_Radial_Fisheye_Degree_8", "nuke.createNode('LD_3DE4_Radial_Fisheye_Degree_8')")
nuke.menu("Nodes").addCommand("3DE4/LD_3DE_Classic_LD_Model", "nuke.createNode('LD_3DE_Classic_LD_Model')")

# OPTICAL FLARES
toolbar = nuke.toolbar("Nodes")
toolbar.addMenu("VideoCopilot", icon="VideoCopilot.png")
toolbar.addCommand( "VideoCopilot/OpticalFlares", "nuke.createNode('OpticalFlares')", icon="OpticalFlares.png")