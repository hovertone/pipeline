import nuke
import os
from PL_scripts import getPipelineAttrs
import PL_rootPipelineStuff
from CUF import selectOnly

def createHiresWrite():
	if not getPipelineAttrs():
		nuke.message('Current shot is not in pipeline.\n')
		return
	else:
		drive, project, seq, shot, assetName, ver = getPipelineAttrs()
		if nuke.root()['colorManagement'].value() == 'OCIO':
			#ACES workflow
			# c = nuke.createNode('Crop', 'crop 0')
			# c['box'].setValue((0, 0, 3200, 1800))
			#
			# selectOnly(c)
			# ref = nuke.createNode('Reformat')
			# ref['format'].setValue("HD_1080")
			# ref['filter'].setValue('Cubic')


			# ocio = nuke.createNode('OCIOColorSpace')
			# ocio['out_colorspace'].setValue('Output - Rec.2020')
			# ocio['label'].setValue('Output - Rec.2020')

			#selectOnly(ref)
			w = nuke.createNode('Write')
			#w['file'].setValue('%s/%s/sequences/%s/%s/out/hires/%s_%s_hires_acescg.####.exr' % (drive, project, seq, shot, seq, shot))
			w['file'].setValue('%s/%s/sequences/%s/%s/out/hires/sequence.####.exr' % (drive, project, seq, shot))
			w['colorspace'].setValue('ACES - ACEScg')
			w['tile_color'].setValue(255)
			#w['raw'].setValue(True)
			PL_rootPipelineStuff.attachHiddenTabAndStringAttr(w, 'tagstab', 'tags', '#hires')
		else:
			#non ACES workflow
			c = nuke.createNode('Crop', 'crop 0')
			w = nuke.createNode('Write')
			w['file'].setValue('%s/%s/sequences/%s/%s/out/hires/%s_%s_hires.####.dpx' % (drive, project, seq, shot, seq, shot))
			w['colorspace'].setValue('sRGB')
			w['tile_color'].setValue(255)
			PL_rootPipelineStuff.attachHiddenTabAndStringAttr(w, 'tagstab', 'tags', '#hires')


def createPreviewWrite():
	if not getPipelineAttrs():
		nuke.message('Current shot is not in pipeline.\n')
		return
	else:
		drive, project, seq, shot, ver = getPipelineAttrs()
		w = nuke.createNode('Write')
		w['file'].setValue('%s/%s/sequences/%s/%s/comp/precomp/preview/v001/%s_%s_preview_v001.####.jpg' % (drive, project, seq, shot, seq, shot))
		w['_jpeg_quality'].setValue(0.95)
		w['tile_color'].setValue(943247871)	
		PL_rootPipelineStuff.attachHiddenTabAndStringAttr(w, 'tagstab', 'tags', '#preview #precomp')


def makePrecomp(precompName, precompType, switch = True):
	types = {'.exr':{		'channels':'rgb',
							'ext':'exr',
							'file_type':'exr',
							'autocrop':True},

			'.exr Alpha':{	'channels':'rgba',
							'ext':'exr',
							'file_type':'exr',
							'autocrop':True},

			'.exr All':{	'channels':'all',
							'ext':'exr',
							'file_type':'exr',
							'autocrop':True},

			'.jpg':{		'channels':'rgb',
							'ext':'jpg',
							'file_type':'jpeg',
							'_jpeg_quality':0.9},

			'.png Alpha':{	'channels':'rgba',
							'ext':'png',
							'file_type':'png'}}

	root = nuke.root()
	#pcname = root['precompName'].value()

	drive, project, seq, shot, assetName, ver = getPipelineAttrs()
	path = '%s/%s/sequences/%s/%s/comp/%s/precomp/%s/v001/%s_%s_%s_v001.####.%s' % (drive, project, seq, shot, assetName, precompName, seq, shot, precompName, types[precompType]['ext'])
	folder = os.path.dirname(path)
	if not os.path.exists(folder): os.makedirs(folder)

	if switch == True:
		nuke.loadToolset("X:/app/win/Pipeline/nuke/toolsets/basic/precomp.nk")
		nodes = nuke.selectedNodes()
		write = [i for i in nodes if i.Class() == 'Write'][0]
		read = [i for i in nodes if i.Class() == 'Read'][0]
		bd = [i for i in nodes if i.Class() == 'BackdropNode'][0]

		#print pcname, write.name(), read.name(), bd.name()

		#write['file_type'].setValue(types[precompType]['file_type'])
		read['file'].setValue(path)
		first = int(root['first_frame'].value())
		last = int(root['last_frame'].value())
		read['first'].setValue(first)
		read['origfirst'].setValue(first)
		read['last'].setValue(last)
		read['origlast'].setValue(last)
		bd['label'].setValue('PRECOMP\n%s' % precompName)
		PL_rootPipelineStuff.attachHiddenTabAndStringAttr(write, 'tagstab', 'tags', '#precomp')
	else:
		write = nuke.createNode('Write')

	for k in types[precompType].keys():
		if k != 'ext':
			write[k].setValue(types[precompType][k])

	# write['channels'].setValue(types[precompType]['channels'])
	write['file'].setValue(path)
