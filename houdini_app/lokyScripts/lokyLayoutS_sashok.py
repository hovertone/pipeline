import hou
def bakeAnimKeys():
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

def refitAnimKeys():
	nodes = hou.selectedNodes()
	input = hou.ui.readMultiInput(message = 'Bake Framerange', input_labels =  ['Start Frame', 'End Frame', 'Tolerance'], buttons=('OK','Cancel'), initial_contents = [str(hou.playbar.playbackRange()[0]), str(hou.playbar.playbackRange()[1]), '.001'])
	rangeStart = int(float(input[1][0]))-10
	rangeEnd = int(float(input[1][1]))+10
	tolerance = float(input[1][2])
	for node in nodes:
		nodePath = node.path()
		parms = node.parms()
		for parm in parms:
			keyFrames = parm.keyframes()
			if len(keyFrames)>0:
				startValue = keyFrames[0].value()
				dif = 0
				for keyFrame in keyFrames:
					keyValue = keyFrame.value()
					dif = dif+abs(startValue-keyValue)
				print parm.name()+str(dif)
				if dif>0.00001:
					parm.keyframesRefit(1,tolerance,1,1,1,0.01,0.1,1,rangeStart,rangeEnd,hou.parmBakeChop.KeepExportFlag)
				else:
					parm.deleteAllKeyframes()

def outNodes():				
	nodes = hou.selectedNodes()
	if len(nodes)>0:
		node = nodes[0]
		parent = node.parent()
		nullOut = parent.createNode("null", "Out", run_init_scripts=True)
		nullRender = parent.createNode("null", "Render", run_init_scripts=True)
		nullProxy = parent.createNode("null", "Out_proxy", run_init_scripts=True)
		
		nullOut.setDisplayFlag(True)
		nullOut.setInput(0, node, 0)
		nullRender.setRenderFlag(True)
		nullRender.setInput(0, nullOut, 0)
		nullOut.moveToGoodPosition(relative_to_inputs=True, move_inputs=True, move_outputs=True, move_unconnected=True)
		nullRender.moveToGoodPosition(relative_to_inputs=True, move_inputs=True, move_outputs=True, move_unconnected=True)
		nullProxy.setInput(0, nullOut, 0)
		nullProxy.moveToGoodPosition(relative_to_inputs=True, move_inputs=True, move_outputs=True, move_unconnected=True)
		
		type_color = hou.Color((0.475, 0.812, 0.204))
		nullOut.setColor(type_color)
		nullRender.setColor(type_color)
		nullProxy.setColor(type_color)
	else:
		hou.ui.displayMessage("No node is selected!", buttons=('OK',), severity=hou.severityType.Error)

def objType():		
	typesGeo = ["light", "char", "env", "props", "volume", "fx", "znull", "technical"]
	colors = [(0.976, 0.78, 0.263), (0.89, 0.412, 0.761), (0.145, 0.667, 0.557), (0.55, 0.5, 0), (0.584, 0.776, 1), (0.71, 0.518, 0.004), (0.478, 0.478, 0.478), (0.3, 0.4, 0.42)]
	nodeshapes = ["light", "bone", "pointy", "rect", "cloud", "star", "null", "clipped_right"]
	selectedType = hou.ui.selectFromList(typesGeo, message="Select Type Of Geo")
	prefix = str(typesGeo[selectedType[0]])
	color = hou.Color(colors[selectedType[0]])
	nodeshape = str(nodeshapes[selectedType[0]])
	redcolor = hou.Color((1, .1, .1))
	nodes = hou.selectedNodes()
	for node in nodes:
		nodeName = node.name()
		parent = node.parent()
		parentPath = parent.path()
		testSles = nodeName.split('_')
		if len(testSles) == 1:
			newname = prefix+"_"+nodeName
			check = hou.node(parentPath+"/"+newname)
			if check is None:
				node.setName(newname)
				node.setColor(color)
				node.setUserData("nodeshape", nodeshape)
			else:
				node.setColor(redcolor)
				hou.ui.displayMessage('NODE NAME - "'+newname+'" ALREADY EXIST!', buttons=('OK',), severity=hou.severityType.Error)
		else:
			withoutPrefix = str(testSles[1])
			newname = prefix+"_"+withoutPrefix
			check = hou.node(parentPath+"/"+newname)
			if check is None:
				node.setName(newname)
				node.setColor(color)
				node.setUserData("nodeshape", nodeshape)
			else:
				node.setColor(redcolor)
				hou.ui.displayMessage('NODE NAME - "'+newname+'" ALREADY EXIST!', buttons=('OK',), severity=hou.severityType.Error)
				
def addHdaVersion():
	node = hou.selectedNodes()[0] #grab the first selected node
	definition = node.type().definition()
	hdaFile = definition.libraryFilePath() #find the hda file path
	versions = []
	for d in hou.hda.definitionsInFile(hdaFile):
		versions.append(d.nodeTypeName().split('::')) #I name the definition myAsset::1.4
	latestVersion = 0

	if len(versions[-1])>1:
		latestVersion = int(versions[-1][-1]) # from myAsset::1.4 -> 1
		
	hdaNewVersion = str((latestVersion+1)).zfill(3)

	hdaNewName = versions[-1][0]+"::"+hdaNewVersion
	newDefinition = definition.copyToHDAFile(hdaFile, new_name=hdaNewName ) #return None no matter what but set for readability
	latestDefinition = hou.hda.definitionsInFile(hdaFile)
	node = node.changeNodeType(hdaNewName , keep_network_contents=False)
	last = latestDefinition[-1]
	last.setVersion(str(hdaNewVersion))
	print "Latest version:"+hdaNewVersion
	
def selHdaVersion():
	node = hou.selectedNodes()[0]
	definition = node.type().definition()
	hdaFile = definition.libraryFilePath() #find the hda file path
	versions = []
	names = []
	versionNames = []
	selectuins = []
	for d in hou.hda.definitionsInFile(hdaFile):
		splited = d.nodeTypeName().split('::')
		if len(splited)<2:
			names.append(splited[0])
			versions.append("000")
		else:
			names.append(splited[0])
			versions.append(splited[-1])
	selected = hou.ui.selectFromList(versions, message="Select version of HDA")
	assetName = names[(selected[0])]
	version = versions[(selected[0])]
	if int(version)<1:
		newNodeTypeName = assetName
	else:
		newNodeTypeName = assetName+"::"+version
	node.changeNodeType(newNodeTypeName, keep_name=True, keep_parms=True, keep_network_contents=True, force_change_on_node_type_match=False)
	nodePost = hou.selectedNodes()[0]
	nodePost.matchCurrentDefinition()
	

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

        return bakedNode

def bakeAnim_ui():
        nodes = hou.selectedNodes()
        if nodes:
                frameRangeUserInput = hou.ui.readMultiInput('Bake Framerange', ['Start Frame', 'End Frame'], buttons=('OK','Cancel'), initial_contents = [str(hou.playbar.playbackRange()[0]), str(hou.playbar.playbackRange()[1])])
                if bool(1 - frameRangeUserInput[0]):
                        frameRange = frameRangeUserInput[1]
                        bakedNodes = []
                        for node in nodes:
                                #bake non cam objects
                                if not node.type().name() == 'cam':
                                        parms = [parm.name() for parm in node.parms() if not parm.isHidden() and not 'vm_' in parm.name()]
                                        #bake one object
                                        if len(nodes) == 1:
                                                bakedParmsList = hou.ui.selectFromList(parms, default_choices=(0,), exclusive=False, message=None, title = 'Select Baked Parms', column_header=None, num_visible_rows=10)
                                                if len(bakedParmsList) != 0:
                                                        if bakedParmsList[0] != 0:
                                                                bakeAnim(node, [int(float(frameRange[0])), int(float(frameRange[1]))], bakeParms = [parms[x] for x in bakedParmsList], parentNode = node.parent(), byChop = True)
                                        #bake mass objects
                                        if len(nodes) > 1:
                                                bakedNodes.append(bakeAnim(node, [int(float(frameRange[0])), int(float(frameRange[1]))], bakeParms = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'], parentNode = node.parent(), byChop = True))
                                #bake cam objects                               
                                elif node.type().name() == 'cam':
                                        bakeAnim(node, [int(float(frameRange[0])), int(float(frameRange[1]))], bakeParms = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'focal', 'aperture', 'resx', 'resy'], byChop = True)
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
				
def makeDailise():
	import os, shutil
    import subprocess as sp
	import datetime
    from modules.pyseq import pyseq
    date = datetime.datetime.now().strftime("%y-%m-%H-%M-%S")
	shotEnv = hou.getenv("SHOT")
	hip = hou.getenv("HIP")
	if shotEnv is None:
		print shotEnv
		#out_path = hou.ui.selectFile(title="Select project path", file_type=hou.fileType.Directory)
		out_path = hip.rsplit("/", 1)[0]+"/out/allDailies"
		print out_path
	else:
		out_path = shotEnv+"/out/allDailies"
	if not os.path.exists(out_path): 
		os.makedirs(out_path)
	hipname = hou.getenv("HIPNAME")
	out_file = hipname+'_'+date+".mov"
	shotNumber = hou.getenv("SN")
	mpg = "X:/app/win/ffmpeg/bin/ffmpeg"
	sequence_path = os.path.expanduser("~") + "/allDailies"
	try:
		os.stat(sequence_path)
	except:
		os.makedirs(sequence_path)
	#hou.hipFile.save(hip+"/dailiesHip/"+hipname+"_"+date, save_to_recent_files=False)
	if hou.ui.displayMessage('Would you like to save scene before daily?', buttons = ('Yes', 'No')) == 0:
		hou.hipFile.save(file_name=None, save_to_recent_files=True)
	fromPath = os.environ["HIPFILE"]
	toPath = hip+"/dailiesHip"
	try:
		os.stat(toPath)
	except:
		os.makedirs(toPath)
	shutil.copy(fromPath, toPath + "/" +hipname+"_"+date+".hip")
	hou.hscript("viewwrite -f $FSTART $FEND -r 1920 1080 -c -R current -q 3 Build.panetab1.world.persp1 " + "'"+sequence_path+"/dailies.$F.jpg'")

	seqs = pyseq.get_sequences(sequence_path)

	files = os.listdir(sequence_path)
	f = os.path.join(sequence_path, files[0]).replace("\\", "/")
	for s in seqs:
		print "SQ PATH: ", sequence_path
		print "SEQUENCE: ", (s.format('%h%p%t'))
		sq = os.path.join(sequence_path, s.format('%h%p%t'))
		# Create string command to create mov
		cmd = mpg + " -threads 8 -r 25 -start_number " + s.format('%s') + " -i " + sq + " -threads 8 -y -framerate 24 -c:v libx264 -pix_fmt yuv420p -preset ultrafast -crf 20 " + out_path + "/"+out_file
		sp.call(cmd, shell=True)
		files = os.listdir(sequence_path)
		for f in files:
			f_remov = os.path.join(sequence_path, f)
			if os.path.isfile(f_remov):
				os.remove(f_remov)

	deiliespath = "Deilies path - "+out_path + "/"+out_file
	print deiliespath
	finalpath = out_path + "/"+out_file
	return finalpath
	

	
	
	
	
	
	
	

	
def telegramMove(filePath=""):
	if len(filePath)>=0:
		import sys
		path = "X:/app/win/Pipeline/bot"
		if not path in sys.path:
			sys.path.append(path)
		import telegram
		tokenFile = open("X:/app/win/Pipeline/bot"+'/token.txt', 'r')
		tokenData = tokenFile.read()
		chatidFile = open("X:/app/win/Pipeline/bot"+'/chatid.txt', 'r')
		chatidData = chatidFile.read()
		bot = telegram.Bot(token=tokenData)
		filePath.replace("P:", "\\NAS\project")
		file = open(filePath, 'rb')
		bot.send_video("-262780274", file, width=99, height=51)
		bot.send_message(chat_id=chatidData, text='<i>Zacenite: '+filePath+'</i>', parse_mode=telegram.ParseMode.HTML)

def envImport():
	import hou
	import os
	import re
	shotEnv = hou.getenv("SHOT")
	objPath = shotEnv+"/env/envProxy/main/geo/"
	def setLastVersion(objPath):
		if os.path.isdir(objPath):
			objList = os.listdir(objPath)
			for version in objList:
				digits = re.findall('(\d+)', version)
				version = max(digits)
		else:
			version = "001"
		return version
	version = setLastVersion(objPath)
	abcPath = objPath+"v"+version+"/envProxy_main_v"+version+".abc"
	import _alembic_hom_extensions as abc
	hierarchy = abc.alembicGetSceneHierarchy(abcPath, "/")
	def analis(c, ojectslist=[]):
		if any(c):
			if type(c[0]) is tuple:
				for index, cc in enumerate(c):
					analis(cc)
					if cc[1] == "polymesh":
						ojectslist.append(str(cc[0]))
			else:
					analis(c[2], ojectslist=ojectslist)
		return ojectslist
	abcObjects = analis(hierarchy)
	paths = abc.alembicGetObjectPathListForMenu(abcPath)
	objectPaths = []
	objects = []
	for index, p in enumerate(paths):
		if index%2==0:
			spl = p.rsplit("/", 1)
			if spl[-1] in abcObjects:
				spl0 = spl[0]
				objects.append(spl0.rsplit("/", 1)[1].split(":")[-1])
				objectPaths.append(spl0)
	print objectPaths
	tsrMatrixs = []            
	for objectPath in objectPaths:
		tsrMatrixs.append(abc.getWorldXform(abcPath, objectPath, 0)[0])
	mayaFixMatrix = hou.Matrix4((.01, 0, 0, 0, 0, .01, 0, 0, 0, 0, .01, 0, 0, 0, 0, 1))
	selected = hou.selectedNodes()
	allnodes = selected
	for sel in selected:
		allnodes=allnodes+sel.allSubChildren()
	for node in allnodes:
		for index, objectname in enumerate(objects):
			if node.name()==objectname:
				if node.type().name() == 'geo':
					matrix = hou.Matrix4(tsrMatrixs[index])*mayaFixMatrix
					node.setWorldTransform(matrix)
	print "Transforms from: "+abcPath+" Imported"
	hou.ui.displayMessage("Transforms from: "+abcPath+" Imported", buttons=('OK',), severity=hou.severityType.ImportantMessage)


def envExport():	
	import hou
	import os
	import re
	
	shotEnv = hou.getenv("SHOT")
	curentShot = hou.getenv("SN")
	sequencePath = shotEnv.rsplit("/", 1)[0]
	shots = os.listdir(sequencePath)
	print shots
	defChoices = shots.index(curentShot)
	print defChoices
	selectedIndex = hou.ui.selectFromList(shots, default_choices=(defChoices,), exclusive=False, message=None, title=None, column_header="Choices", num_visible_rows=10, clear_on_cancel=False, width=0, height=0)
	
	
	
	
	
	for index in selectedIndex:
		#shotEnv = hou.getenv("SHOT")
		objPath = sequencePath+"/"+str(shots[index])+"/env/envProxy/main/geo/"
		def setLastVersion(objPath):
			if os.path.isdir(objPath):
				objList = os.listdir(objPath)
				for version in objList:
					digits = re.findall('(\d+)', version)
					version = str(int(max(digits))+1).zfill(3)
			else:
				version = "001"
			return version
		version = setLastVersion(objPath)

		selected = hou.selectedNodes()
		allnodes = selected
		for sel in selected:
			allnodes=allnodes+sel.allSubChildren()
		def nInputs(node, hyerarhyNodePath="", layoutEnv=None):
			hou.parm(node.path()+"/keeppos").set(0)
			nInput = node.inputs()
			parent = node.parent()
			parentName = parent.name()
			if any(nInput):
				hyerarhyNodePath=hyerarhyNodePath+nInput[0].path()+" "
				nInputs(node=nInput[0], hyerarhyNodePath=hyerarhyNodePath, layoutEnv=layoutEnv)

			elif parentName!="obj":
				hyerarhyNodePath=hyerarhyNodePath+parent.path()+" "
				subnetinputpath = node.parent().path()+'/1'
				node.setInput(0, hou.item(subnetinputpath), 0)
				nInputs(node=parent, hyerarhyNodePath=hyerarhyNodePath, layoutEnv=layoutEnv)
				
			elif node!=layoutEnv:
				node.setInput(0, layoutEnv, 0)    
			return hyerarhyNodePath
				
		layoutEnv = hou.node("/obj").createNode("null", "layout", run_init_scripts=True)
		hou.parm(layoutEnv.path()+'/scale').set(100)
		ropNode = hou.node("/out").createNode("alembic", "exportEnv", run_init_scripts=True)
		nodesPaths = ""

		for node in allnodes:
			context = node.type().category().name()
			if context=="Object":
				nodeType = node.type().name()
				if nodeType == "geo":
					if node.name().split("_")[0] == "env":
						if node.isDisplayFlagSet():
							hou.parm(node.path()+"/keeppos").set(0)
							parent = node.parent() ##### only visible
							if parent.name()!="obj":
								if parent.isDisplayFlagSet():
									#nodesPaths=nodesPaths+node.path()+" "+nInputs(node=node, hyerarhyNodePath="", layoutEnv=layoutEnv)
									nodesPaths=nodesPaths+node.path()+" "
									nInputs(node=node, hyerarhyNodePath="", layoutEnv=layoutEnv)
							else:
								#nodesPaths=nodesPaths+node.path()+" "+nInputs(node=node, hyerarhyNodePath="", layoutEnv=layoutEnv)
								nodesPaths=nodesPaths+node.path()+" "
								nInputs(node=node, hyerarhyNodePath="", layoutEnv=layoutEnv)
		nodesPaths=nodesPaths+layoutEnv.path()
		hou.parm(ropNode.path()+"/objects").set(nodesPaths)
		hou.parm(ropNode.path()+"/pointAttributes").set("")
		hou.parm(ropNode.path()+"/vertexAttributes").set("N")
		hou.parm(ropNode.path()+"/primitiveAttributes").set("path")
		hou.parm(ropNode.path()+"/detailAttributes").set("")
		filePath = '%s/%s' % (sequencePath, shots[index]) + "/env/envProxy/main/geo/v"+version+"/envProxy_main_v"+version+".abc"
		hou.parm(ropNode.path()+"/filename").set(filePath)
		ropNode.render()
		layoutEnv.destroy()
		ropNode.destroy()
		print "Layout exported to: "+filePath
		hou.ui.displayMessage("Layout exported to: "+filePath, buttons=('OK',), severity=hou.severityType.ImportantMessage)
	
def makeImageNode(texType, colorSpace, surfaceInput, _colorcorect, normalmap, _imageColor, _corectColor, _arnold_vopnet, _textureFolder, _assetname, _texExt, _standart_surface):

    ### BaseColor ###
    imagenode = _arnold_vopnet.createNode("image", texType, run_init_scripts=True)
    imagenode.setColor(_imageColor)
    hou.parm(imagenode.path()+"/filename").set("$ASSETBUILDS/")
    if _colorcorect == 1:
        imagenodeCorect = _arnold_vopnet.createNode("color_correct", texType+"Corect", run_init_scripts=True)
        imagenodeCorect.setColor(_corectColor)
        imagenodeCorect.setInput(0, imagenode, 0)
        _standart_surface.setInput(surfaceInput, imagenodeCorect, 0)
    if normalmap == 1:
        NormalMap = _arnold_vopnet.createNode("normal_map", "NormalMap", run_init_scripts=True)
        NormalMap.setInput(0, imagenode, 0)
        standart_surface.setInput(33, NormalMap, 0)

def createShader():
		### color ###
	imageColor = hou.Color((0.475, 0.812, 0.204))
	surfaceColor = hou.Color((0.475, 0.812, 0.204))
	corectColor = hou.Color((0.478, 0.478, 0.478))
	matColor = hou.Color((0.45, 0.308, 0.45))
	
	assetname = "assetName" ####!!!!
	net_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	selecteds = hou.selectedNodes()
	parent = net_editor.pwd()
	if len(selecteds)>0:
		selected = selecteds[0]
		if selected.type().category().name() == "Object":
			parent = selecteds[0]
	
	childrens = parent.children()
	shopnet = None
	for child in childrens:
		if child.type().name() == "shopnet":
			shopnet = child
	if shopnet is None:
		shopnet = parent.createNode("shopnet", "shopnet1", run_init_scripts=True)
	materialNode = parent.createNode("material", "material_"+parent.name().split("_")[-1], run_init_scripts=True)
	materialNode.setColor(matColor)
	hou.parm(materialNode.path()+"/shop_materialpath1").set("../shopnet1/"+parent.name().split("_")[-1])      
	arnold_vopnet = shopnet.createNode("arnold_vopnet", parent.name().split("_")[-1], run_init_scripts=True)
	arnold_vopnet.setColor(imageColor)
	arnold_vopnetPath = arnold_vopnet.path()

	#parm_group = arnold_vopnet.parmTemplateGroup()
	#parm_folder = hou.FolderParmTemplate("mat_setting", "Mat Setting")
	#textureVersion = hou.IntParmTemplate(name="tex_version", label="Texture Version", num_components=1, default_value=[1])
	#texturePath = hou.StringParmTemplate(name='texture_folder', label='Texture Folder', num_components=1, default_value=["$ASSETBUILDS/geo/"+"char/"+"/tex/v`padzero(3, chsop('"'tex_version'"'))`/"], naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, file_type=hou.fileType.Directory)
	#textureExtParm = hou.StringParmTemplate(name='texture_ext', label='Texture Ext', num_components=1, default_value=["exr"]) 
	#parm_folder.addParmTemplate(textureVersion)
	#parm_folder.addParmTemplate(texturePath)
	#parm_folder.addParmTemplate(textureExtParm)
	#parm_group.append(parm_folder)
	#arnold_vopnet.setParmTemplateGroup(parm_group)
	textureFolder = "`chs('"'../../texture_folder'"')`"
	texExt = "`chs('"'../../texture_ext'"')`"

	out_material = hou.node(arnold_vopnetPath+"/OUT_material")
	standart_surface = arnold_vopnet.createNode("standard_surface", "standard_surface", run_init_scripts=True)
	standart_surface.setColor(surfaceColor)
	out_material.setInput(0, standart_surface, 0)

	makeImageNode(texType="BaseColor", colorSpace="sRGB", surfaceInput=1, _colorcorect=1, normalmap=0, _imageColor=imageColor, _corectColor=corectColor, _arnold_vopnet=arnold_vopnet, _textureFolder=textureFolder, _assetname=assetname, _texExt=texExt, _standart_surface=standart_surface)
	makeImageNode(texType="Metalness", colorSpace="linear", surfaceInput=3, _colorcorect=1, normalmap=0, _imageColor=imageColor, _corectColor=corectColor, _arnold_vopnet=arnold_vopnet, _textureFolder=textureFolder, _assetname=assetname, _texExt=texExt, _standart_surface=standart_surface)    
	makeImageNode(texType="Roughness", colorSpace="linear", surfaceInput=6, _colorcorect=1, normalmap=0, _imageColor=imageColor, _corectColor=corectColor, _arnold_vopnet=arnold_vopnet, _textureFolder=textureFolder, _assetname=assetname, _texExt=texExt, _standart_surface=standart_surface)    
	makeImageNode(texType="Specular", colorSpace="linear", surfaceInput=4, _colorcorect=1, normalmap=0, _imageColor=imageColor, _corectColor=corectColor, _arnold_vopnet=arnold_vopnet, _textureFolder=textureFolder, _assetname=assetname, _texExt=texExt, _standart_surface=standart_surface)    

	### Normal ###
	Normal = arnold_vopnet.createNode("image", "Normal", run_init_scripts=True)
	Normal.setColor(imageColor)
	hou.parm(Normal.path()+"/filename").set("$ASSETBUILDS/")        
	#hou.parm(Normal.path()+"/color_space").set("linear")
	NormalMap = arnold_vopnet.createNode("normal_map", "NormalMap", run_init_scripts=True)
	NormalMap.setInput(0, Normal, 0)
	standart_surface.setInput(33, NormalMap, 0)

	### Height ###        
	Height = arnold_vopnet.createNode("image", "Height", run_init_scripts=True)
	Height.setColor(imageColor)
	hou.parm(Height.path()+"/filename").set("$ASSETBUILDS/")        
	out_material.setInput(1, Height, 0)
				
	Emissive = arnold_vopnet.createNode("image", "Emissive", run_init_scripts=True)
	Emissive.setColor(imageColor)
	hou.parm(Emissive.path()+"/filename").set("$ASSETBUILDS/")        
	#hou.parm(Emissive.path()+"/color_space").set("sRGB")
	EmissiveCorect = arnold_vopnet.createNode("color_correct", "EmissiveCorect", run_init_scripts=True)
	EmissiveCorect.setColor(corectColor)
	EmissiveCorect.setInput(0, Emissive, 0)
	standart_surface.setInput(31, EmissiveCorect, 0)
	shopnet.layoutChildren((), -1.0, -1.0)
	arnold_vopnet.layoutChildren((), -1.0, -1.0)	
	
def geoToFileCache():
	nodes = hou.selectedNodes()
	for node in nodes:
		if node.type().name().split("::")[0] == "geo":
			nodePath = node.path()
			parent = node.parent()
			file=hou.parm(node.path()+"/sopoutput").rawValue()
			loadfromdisk=hou.parm(node.path()+"/load_from_disk").eval()
			f1=hou.parm(node.path()+"/f1").eval()
			f2=hou.parm(node.path()+"/f2").eval()
			f3=hou.parm(node.path()+"/f3").eval()
			trange = hou.parm(node.path()+"/trange").eval()
			objectname = hou.parm(node.path()+"/objectname").eval()
			component = hou.parm(node.path()+"/component").eval()
			
			intput = node.inputs()[0]
			outputs = node.outputs()
			node.setInput(0, None, 0)
			filecache = parent.createNode("filecache", "cache_"+objectname+"_"+component, run_init_scripts=True)
			hou.parm(filecache.path()+"/file").set(file)
			hou.parm(filecache.path()+"/loadfromdisk").set(loadfromdisk)
			hou.parm(filecache.path()+"/f1").deleteAllKeyframes()
			hou.parm(filecache.path()+"/f1").set(f1)
			hou.parm(filecache.path()+"/f2").deleteAllKeyframes()
			hou.parm(filecache.path()+"/f2").set(f2)
			hou.parm(filecache.path()+"/f3").deleteAllKeyframes()
			hou.parm(filecache.path()+"/f3").set(f3)
			hou.parm(filecache.path()+"/trange").set(trange)
			filecache.setInput(0, intput, 0)
			for output in outputs:
				output.setInput(0, filecache, 0)
			node.destroy()
			filecache.moveToGoodPosition(relative_to_inputs=True, move_inputs=True, move_outputs=True, move_unconnected=True)	
	
def makeProxyTextures():
	print 'makeProxy Textures2'
	import os
	import subprocess as sp
	hou.hipFile.saveAndIncrementFileName()
	allnodes = []
	selectedNodes = hou.selectedNodes()
	for seleted in selectedNodes:
		childrens = seleted.allSubChildren()
		for child in childrens:
			allnodes.append(child)
	folderList = []
	index = 0
	for node in allnodes:
		if node.type().name()=='arnold::image':
			imagePath = hou.parm(node.path()+"/filename").eval()
			# TWEAK
			imagePath = imagePath.replace('<udim>', '1001')
			textureFolder = os.path.split(imagePath)[0]
			if textureFolder not in folderList:
				folderList.append(textureFolder)
	for folder in folderList:
		proxyFolder = folder+'/proxy'
		try:
			os.stat(proxyFolder)
		except:
			os.makedirs(proxyFolder)
		files = os.listdir(folder)
		for file in files:
			ext = os.path.splitext(file)
			filename = os.path.split(file)
			if (ext[1] == ".exr") or (ext[1] == ".png") or (ext[1] == ".jpg") or (ext[1] == ".tif") or (ext[1] == ".jpeg"):
				inp = folder+'/'+file
				outp = proxyFolder+'/'+ext[0]+'.jpg'

				cmd = 'X:/app/win/ffmpeg/bin/ffmpeg -i '+folder+'/'+file+' -n -s 512x512 '+proxyFolder+'/'+ext[0].replace(' ', '_')+'.jpg'
				if 'Diffuse Color_EyeBall' in file:
					sp.call(cmd, shell=True)
					index=index+1
					print "---------\nin: "+inp+"\nout: "+outp
					print 'working on : %s ' % file
				else:
					print 'skipped : %s' % file

	hou.ui.displayMessage(str(index)+" Proxy finished", buttons=('OK',), severity=hou.severityType.ImportantMessage)
	
	
def out_null():
    input = hou.ui.readInput("ENTER NAME", buttons=('OK',), severity=hou.severityType.Message)
    name = input[1]
    if input[1] != 0:
        nodeColor = hou.Color((0.475, 0.812, 0.204))
        net_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
        selecteds = hou.selectedNodes()
        parent = net_editor.pwd()
        nullNode = parent.createNode("null", "Out_"+name, run_init_scripts=True)
        if len(selecteds)>0:
            nullNode.setInput(0, selecteds[0], 0)
        nullNode.setColor(nodeColor)
        nullNode.moveToGoodPosition(relative_to_inputs=True, move_inputs=True, move_outputs=True, move_unconnected=True)
		
def splitGeo():
    import toolutils
    input = hou.ui.readInput("ENTER NAME", buttons=('OK',), severity=hou.severityType.Message)
    name = input[1]
    if input[1] != 0:
		if(len(name)>0):
			groupColor = hou.Color((0.188, 0.529, 0.459))
			blastColor = hou.Color((0.384, 0.184, 0.329))
			node = hou.selectedNodes()[0]
			parent = node.parent()
			groupNode = parent.createNode("group", "gr_"+name, run_init_scripts=True)
			groupNode.setColor(groupColor)  
			groupNode.setInput(0, node, 0)
			groupNode.moveToGoodPosition(relative_to_inputs=True, move_inputs=True, move_outputs=True, move_unconnected=True)
			groupNode.setDisplayFlag(True)
			blastNode = parent.createNode("blast", "select_"+name, run_init_scripts=True)
			blastNode.setColor(blastColor)
			hou.parm(blastNode.path()+"/group").set("gr_"+name)
			hou.parm(blastNode.path()+"/negate").set(1)
			blastNode.setInput(0, groupNode, 0)
			blastNode.moveToGoodPosition(relative_to_inputs=True, move_inputs=True, move_outputs=True, move_unconnected=True)
			groupNode.setSelected(on=True, clear_all_selected=True, show_asset_if_selected=False)
			viewer = toolutils.sceneViewer()
			geo = viewer.selectGeometry()
			hou.parm(groupNode.path()+"/crname").set("gr_"+name)
			hou.parm(groupNode.path()+"/pattern").set(str(geo))
			geo = " "