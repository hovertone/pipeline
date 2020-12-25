import nuke
import os, sys

knobNames = ['precomp', 'precompName', 'cam', 'hires', 'daily', 
				'shot', 'project',
				'PIPELINE']

def shotInfoFromName():
	root = nuke.root()
	path = root.name()
	project = path.split('/')[1]
	shot = path.split('/')[3].strip('sh_')
	return project, shot

def attachWriteButtons():
	dailyB = nuke.PyScript_Knob('daily', 'Make dailies', 'import PL_dailiesMaker\nreload(PL_dailiesMaker)\nPL_dailiesMaker.makeDailyFromRead()')
	hiresB = nuke.PyScript_Knob('hires', 'Hires Write', 'import PL_writesCreate\nreload(PL_writesCreate)\nPL_writesCreate.createHiresWrite()')
	precompName = nuke.EvalString_Knob('precompName', '')
	precompName.setFlag(nuke.STARTLINE)
	precompB = nuke.PyScript_Knob('precomp', 'Create Precomp', 'import PL_writesCreate\nreload(PL_writesCreate)\nPL_writesCreate.makePrecomp()')
	root = nuke.root()
	for i in (dailyB, hiresB, precompName, precompB):
		root.addKnob(i)

def attachHiddenTabAndStringAttr(node, tabName, attrName, attrValue):
	if 'tags' not in node.knobs().keys():
		t = nuke.Tab_Knob(tabName, tabName)
		t.setFlag(nuke.INVISIBLE)
		attr = nuke.EvalString_Knob(attrName, attrName)
		attr.setValue(attrValue)
		attr.setFlag(nuke.INVISIBLE)

		node.addKnob(t)
		node.addKnob(attr)
		#print '%s knob added' % attrName
	else:
		pass
		#print 'There is a tags knobs. Dissmiss!'

def attachStringAttr(attrName, attrValue, enabled = True, visible = True):
	attr = nuke.EvalString_Knob(attrName, attrName)
	attr.setValue(attrValue)
	attr.setEnabled(enabled)
	attr.setVisible(visible)
	nuke.root().addKnob(attr)

def detachPipelinieStuffFromRoot():
	#global knobNames
	defKnobs = ['frame_increment', 'transfer_default', 'frame', 'onScriptSave', 'workingSpaceLUT', 'customOCIOConfigPath', 'int8Lut', 'curve_editor', 'monitorLut', 'lut', 'title', 'free_type_font_path', 'hero_view', 'views', 'label', 'last_frame', 'int16Lut', 'window', 'lock_connections', 'lookup', 'Script_directory', 'fps', 'logLut', 'OCIO_config', 'proxy_type', 'luts', 'lock_range', 'project_directory', 'format', 'views_button', 'views_colours', 'proxy', 'OCIOConfigPath', 'proxy_scale', 'proxy_to_format', 'onScriptLoad', 'panel', 'playback_fps', 'name', 'proxySetting', 'floatLut', 'mapsize', 'onScriptClose', 'viewerLut', 'proxy_format', 'first_frame', 'RescanFreeTypeMappingPaths', 'setlr', 'transfer', 'defaultViewerLUT', 'free_type_system_fonts', 'LUT_default', 'colorManagement', 'ocio_config_error_knob']
	root = nuke.root()
	rootKnobs = root.knobs().keys()
	difference = sorted(list(set(rootKnobs) - set(defKnobs)), reverse = True)
	for k in difference:
		try:
			root.removeKnob(root.knob(k))
			print '%s knob succesfully removed' % k
		except:
			print '%s knob has not been found' % k

def attachPipelineStuffToRoot():
	root = nuke.root()
	t = nuke.Tab_Knob('PIPELINE', 'PIPELINE')
	root.addKnob(t)
	attachStringAttr('project', '', False, False)
	attachStringAttr('shot', '', False, False)
	attachWriteButtons()
	attachCameraImporterButton()

def fixRootTab(assignShotInfo = False):
	detachPipelinieStuffFromRoot()
	root = nuke.root()
	t = nuke.Tab_Knob('PIPELINE', 'PIPELINE')
	root.addKnob(t)
	if assignShotInfo:
		project, shot = shotInfoFromName()
		attachStringAttr('project', project, False, False)
		attachStringAttr('shot', shot, False, False)
	else:
		attachStringAttr('project', '', False, False)
		attachStringAttr('shot', '', False, False)
	attachWriteButtons()
	attachCameraImporterButton()

def reattachPipelineStuffToRoot():
	detachPipelinieStuffFromRoot()
	attachPipelineStuffToRoot()

def attachCameraImporterButton():
	camImportB = nuke.PyScript_Knob('camImport', 'Import Cam', 'import PL_cameraImporter\nreload(PL_cameraImporter)\nPL_cameraImporter.importCam()')
	camImportB.setFlag(nuke.STARTLINE)
	root = nuke.root()
	root.addKnob(camImportB)