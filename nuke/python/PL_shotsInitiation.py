# THIS SCRIPT WILL INITIATE A NUKE WORKFLOW BASED ON A .CSV FILE IN A PROJECT ROOT FOLDER
# MAINLY THE .NK FILES WILL BE CREATED WITH AN APPROPRIATE DATA BURNED IN AND THE HIRES WRITE INSIDE THE SCRIPT

import nuke
import os
from PL_scripts import inPipeline
import PL_writesCreate
import PL_rootPipelineStuff
from p_utils.csv_parser_bak import projectDict



def main(project):
	drive = 'P:'
	path = "%s/%s/project_config.csv" % (drive, project)
	shotsFolder = '%s/%s/shots' % (drive, project)
	root = nuke.root()
	pd = projectDict(project)

	for seq in pd.getSequences():
		for shot in pd.getShots(seq):
			#cur_line = [i for i in lines if s in i][0]
			#cur_line_splitted = cur_line.split(',')
			first_frame = pd.getSpecificShotData(seq, shot, 'first_frame')
			last_frame = pd.getSpecificShotData(seq, shot, 'last_frame')

			#print '%s %s %s %s' % (seq, shot, first_frame, last_frame)

			# Cleaning the nodes except Viewers
			for i in [e for e in nuke.allNodes() if e.Class() != 'Viewer']:
				nuke.delete(i)

			# SHOT STUFF
			root['lock_range'].setValue(True)
			root['fps'].setValue(24)
			root['format'].setValue('HD_1080')
			root['first_frame'].setValue(int(first_frame))
			root['last_frame'].setValue(int(last_frame))

			# PIPELINE STUFF
			attachTab(nuke.root(),'PIPELINE')
			attachStringAttr('project', project, enabled = False)
			attachStringAttr('seq', seq, enabled = False)
			attachStringAttr('shot', shot, enabled = False)

			PL_writesCreate.createHiresWrite()
			PL_writesCreate.createPreviewWrite()

			pathToSave = '%s/%s/sequences/%s/%s/comp/%s_%s_mainComp_sashok_v001.nk' % (drive, project, seq, shot, seq, shot)
			dirName = os.path.dirname(pathToSave)

			if not os.path.exists(dirName):
				# If directory doesn't exists we create it and save .nk there
				os.makedirs(dirName)
				nuke.scriptSave(pathToSave)
				print '%s %s \t folder has been created, project saved' % (seq, shot)
			elif os.path.exists(dirName) and len([i for i in os.listdir('%s/%s/sequences/%s/%s/comp' % (drive, project, seq, shot)) if '.' in i]) == 0:
				# If directory already exists but there is no .nk files save first version of comp
				nuke.scriptSave(pathToSave)
				print '%s %s \t project saved' % (seq, shot)
			else:
				# If directory exists with atleast 1 .nk file in it then scripts assume that the comp work has already begun and doesn't save anything
				print '%s %s \t nothing happend' % (seq, shot)
				pass

def attachStringAttr(attrName, attrValue, enabled = True, visible = True):
	root = nuke.root()
	if attrName not in root.knobs().keys():
		attr = nuke.EvalString_Knob(attrName, attrName)
		attr.setValue(attrValue)
		attr.setEnabled(enabled)
		#attr.setVisible(visible)
		nuke.root().addKnob(attr)
	else:
		attr = root[attrName]
		attr.setValue(str(attrValue))
		attr.setEnabled(enabled)
		#attr.setVisible(visible)

def attachTab(node, tabName):
	if tabName not in node.knobs().keys():
		t = nuke.Tab_Knob(tabName, tabName)
		#t.setFlag(nuke.INVISIBLE)
		node.addKnob(t)
		print '%s tab added' % tabName
	else:
		print 'There is one %s tab already. Dissmiss!' % tabName