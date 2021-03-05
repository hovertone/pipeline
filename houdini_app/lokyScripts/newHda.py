import hou
import os
from shutil import copyfile
import subprocess as sp


try:
	from PySide2.QtGui import *
	from PySide2.QtCore import *
	from PySide2.QtWidgets import *
	import hou
except:
	from PySide.QtGui import *
	from PySide.QtCore import *



def newHda(pipeLinePath="X:/app/win/Pipeline"):
	node = hou.selectedNodes()[0]
	sedNodes = hou.selectedNodes()

	enterName = hou.ui.readInput("Asset Name", buttons=('OK', 'CANCEL'), severity=hou.severityType.Message, default_choice=0, close_choice=1, help=None, title="ASSET NAME", initial_contents=None)
	assetName = enterName[1]
	enterComment = hou.ui.readInput("Comment: ", buttons=('OK',), severity=hou.severityType.Message)
	# COMMENT
	usr = os.environ["COMPUTERNAME"].lower()
	comment = usr + ":: " + enterComment[1]

	assetTypes = ["char", "env", "props", "fx"]
	colors = [(0.89, 0.412, 0.761), (0.145, 0.667, 0.557), (0.55, 0.5, 0), (0.71, 0.518, 0.004)]
	nodeshapes = ["bone", "pointy", "rect", "star"]
	
	selType = hou.ui.selectFromList(assetTypes, exclusive=False, message=None, title=None, column_header="Choices", num_visible_rows=4, clear_on_cancel=False, width=1, height=6)
	assetType = assetTypes[selType[0]]
	assetLibrary = "O:/"
	filePath = assetLibrary+assetType+'/'+assetName+'.hda'
	
	
	node = sedNodes[0].parent().createNode("subnet", node_name=assetName, run_init_scripts=True, load_contents=True, exact_type_name=False)
	copedNodes = node.copyItems(sedNodes, channel_reference_originals = False, relative_references = True, connect_outputs_to_multi_inputs = True)
	sedNodes[0].parent().deleteItems(sedNodes)
	
	
	
	master = node.createNode("null", node_name="Master", run_init_scripts=True, load_contents=True, exact_type_name=False)
	master.setColor(hou.Color((.8, 0.1, .1)))
	hou.parm(master.path()+"/controltype").set("circles")
	hou.parm(master.path()+"/orientation").set("y")
	hou.parm(master.path()+"/dcolorr").set(.8)
	hou.parm(master.path()+"/dcolorg").set(.1)
	hou.parm(master.path()+"/dcolorb").set(.1)
	subnetinputpath = node.path()+'/1'
	master.setInput(0, hou.item(subnetinputpath), 0)
	for copedNode in copedNodes:
		if len(copedNode.inputs())==0:
			copedNode.setInput(0, master, 0)
		prevName = copedNode.name()
		copedNode.setName(assetType+"_"+prevName)
		copedNode.setGenericFlag(hou.nodeFlag.Selectable, 0)
	node.layoutChildren(items=(), horizontal_spacing=-1.0, vertical_spacing=-1.0)
	node.setSelected(1, clear_all_selected=True)
	
	color = str(colors[selType[0]])
	nodeshape = nodeshapes[selType[0]]	
	definition = node.createDigitalAsset(name=assetName, hda_file_name=filePath, description=assetName, min_num_inputs=0, max_num_inputs=1, compress_contents=False, comment=comment, version=None, save_as_embedded=False, ignore_external_references=False, change_node_type=True, create_backup=True)
	
	node = hou.selectedNodes()[0]
	

	definition = node.type().definition()
	print definition
	section_file = open(pipeLinePath+'/houdini_app/lokyScripts/'+assetType+'.xml', 'r')
	content = section_file.read()
	definition.addSection("Tools.shelf", contents=content, compression_type=hou.compressionType.NoCompression)
	section_file.close()
	
	parms = ['t','r', 's', 'p', 'pr', 'scale']
	for p in parms:
		for parm in node.parmTuple(p):
			if len(parm.keyframes()) > 0 and parm.expression() != '':
				continue
			else:
				parm.lock(1)
				#parm.hide(True)
	
	
	
	group = definition.parmTemplateGroup()
	group.hideFolder('Transform', True)
	definition.setParmTemplateGroup(group)
	group2 = definition.parmTemplateGroup()
	group2.hideFolder('Subnet', True)
	definition.setParmTemplateGroup(group2)
	
	
	
	
	
	
	#lockparms = "\nparms = ['t','r', 's', 'p', 'pr', 'scale']\nfor p in parms:\n    for parm in nodeName.parmTuple(p):\n        if len(parm.keyframes()) > 0 and parm.expression() != '':\n            continue\n        else:\n            parm.lock(1)\n            parm.hide(True)\n"
	#hideparms =  "\ngroup = nodeName.parmTemplateGroup()\ngroup.hideFolder('Transform', True)\nnodeName.setParmTemplateGroup(group)\ngroup2 = nodeName.parmTemplateGroup()\ngroup2.hideFolder('Subnet', True)\nnodeName.setParmTemplateGroup(group2)"

	
	
	
	
	modOnCreated ="nodeName = kwargs['node']\ntype_color = hou.Color("+color+")\nnodeName.setColor(type_color)\nnodeName.setUserData('nodeshape', '"+nodeshape+"')\nnodeName.setName('"+assetType+"_"+assetName+"', unique_name=True)"##+lockparms+hideparms
	
	
	
	definition.addSection("OnCreated", contents=modOnCreated, compression_type=hou.compressionType.NoCompression)
	definition.updateFromNode(node)
	
def hdaTex():	
	##### COPY TEXTURES ######
	node = hou.selectedNodes()[0]
	node.allowEditingOfContents()
	definition = node.type().definition()
	hdaPath = definition.libraryFilePath()
	#os.path.split(hdaPath)
	os.path.splitext(hdaPath)
	#texPath = assetLibrary+assetType+'/'+assetName
	texPath = os.path.splitext(hdaPath)[0]
	##############
	
	parm_group = definition.parmTemplateGroup()

	parm_folder = hou.FolderParmTemplate("hda_folder", "HDA Folder")
	texturePath = hou.StringParmTemplate(name='texture_folder', label='Texture Folder', num_components=1, default_value=["'import os /n node = hou.pwd() /n return os.path.splitext(node.type().definition().libraryFilePath())[0]'"], naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, file_type=hou.fileType.Directory)

	expr = ("import os\nnode = hou.pwd()\nreturn os.path.splitext(node.type().definition().libraryFilePath())[0]",)
	texturePath.setDefaultExpression(expr)
	texturePath.setDefaultExpressionLanguage((hou.scriptLanguage.Python, hou.scriptLanguage.Hscript)) 
	parm_folder.addParmTemplate(texturePath)
	parm_group.append(parm_folder)
	definition.setParmTemplateGroup(parm_group)
	definition.updateFromNode(node) ####!!!!!



	################
	proxyFolder = texPath+'/proxy'
	######

	#imageFolderParmPath = 
	try:
		os.mkdir(texPath)
	except OSError:
		print ("Creation of the directory %s failed" % texPath)
	else:
		print ("Successfully created the directory %s " % texPath)
	
	try:
		os.stat(proxyFolder)
	except:
		os.makedirs(proxyFolder)
	sourceImages= []
	targetImages = []


	allnodes = []
	selectedNodes = hou.selectedNodes()
	childrens = node.allSubChildren()
	for child in childrens:
		allnodes.append(child)
	folderList = []
	index = 0
	for imgMode in allnodes:
		if imgMode.type().name()=='arnold::image':
			imagePath = hou.parm(imgMode.path()+"/filename").evalAsString()
			coef = int(len(imgMode.path().split("/"))-len(node.path().split("/")))		
			trr = ""
			for i in range(0, coef):
				trr=trr+"../"
			parmExpres = "`chs('"+trr+"texture_folder')`/"
			newImagePath = parmExpres+imagePath.split("/")[-1]
			hou.parm(imgMode.path()+"/filename").set(newImagePath)
			imagePath = imagePath.replace('<udim>', '1001').replace('%(UDIM)d', '1001')
			textureFolder = os.path.split(imagePath)[0]
			if textureFolder not in folderList:
				folderList.append(textureFolder)
	for folder in folderList:
		if os.path.exists(folder):
			filess = os.listdir(folder)
			for f in filess:
				#print "file: "+f
				if os.path.isfile(folder+"/"+f):
					sourceImages.append(f)
		
		for sourceImage in sourceImages:
			print "sourceImage: "+sourceImage
			sourceImageExt = sourceImage.split(".")[-1]
			print "sourceImageExt: "+sourceImageExt
			if (sourceImageExt == "exr") or (sourceImageExt == "png") or (sourceImageExt == "jpg") or (sourceImageExt == "tif") or (sourceImageExt == "jpeg"):
				copyfile(folder+"/"+sourceImage, texPath+"/"+sourceImage)
				targetImages.append(texPath+"/"+sourceImage)
	print "targetImages: "+str(targetImages)
	

	

	#### Proxy #####
	for targetImage in targetImages:
		ext = os.path.splitext(targetImage)
		filename = os.path.split(targetImage)
		if (ext[1] == ".exr") or (ext[1] == ".png") or (ext[1] == ".jpg") or (ext[1] == ".tif") or (ext[1] == ".jpeg"):
			inp = targetImage
			outp = proxyFolder+'/'+filename[-1]+'.jpg'
			print "in: "+inp+" out: "+outp
			cmd = 'X:/app/win/ffmpeg/bin/ffmpeg -i '+inp+' -n -s 512x512 '+outp
			sp.call(cmd, shell=True)
			index=index+1
	hou.ui.displayMessage(str(index)+" Proxy finished", buttons=('OK',), severity=hou.severityType.ImportantMessage)
	
	
	
def embFiles():
	node = hou.selectedNodes()[0]
	node.allowEditingOfContents()
	definition = node.type().definition()
	childrens = node.allSubChildren(top_down=True, recurse_in_locked_nodes=False)
	for child in childrens:
		childType = child.type().name()
		print childType
		if childType != "filecache" and childType != "file" and childType != "alembic":
			continue
			print childType
		else:
			if childType == "filecache" or childType == "file":
				parmName = "file"
			if childType == "alembic":
				parmName = "fileName"
			filepath = hou.parm(child.path()+"/"+parmName).eval()
			section_file = open(filepath, "r")
			fileName = os.path.split(filepath)[-1]
			definition.addSection(fileName, hou.readFile(filepath), compression_type=hou.compressionType.NoCompression)
			section_file.close()
			coef = int(len(child.path().split("/"))-len(node.path().split("/")))		
			trr = ""
			for i in range(0, coef):
				trr=trr+"../"
			newParmPath  =  "opdef:"+ trr+"?"+fileName
			hou.parm(child.path()+"/"+parmName).set(newParmPath)
	definition.updateFromNode(node)


def imgPreviev():
	print "HELLO"

	clipboard = QApplication.clipboard()
	mimeData = clipboard.mimeData()
	
	node = hou.selectedNodes()[0]
	definition = node.type().definition()
	hdaPath = definition.libraryFilePath()
	toolset_path = os.path.splitext(hdaPath)[0]
	print toolset_path
	
	if mimeData.hasImage():
		print 'saved with screenshot'
		i = clipboard.image()
		p = QPixmap(i)
		p.save(toolset_path + '.png', "png")
		print "File: "+toolset_path + '.png Saved from Buffer!'
	else:
		selectedFIle = hou.ui.selectFile(start_directory=None, title=None, collapse_sequences=False, file_type=hou.fileType.Image, pattern=None, default_value=None, multiple_select=False, image_chooser=False, chooser_mode=hou.fileChooserMode.ReadAndWrite, width=0, height=0)
		if len(selectedFIle)>0:
			copyfile(selectedFIle, toolset_path +os.path.splitext(selectedFIle)[-1])
			print "File: "+toolset_path +os.path.splitext(selectedFIle)[-1]+' Saved from '+selectedFIle
		else:
			print "SomethingWrong!!!"



def addParameters():
	node = hou.selectedNodes()[0]
	node.allowEditingOfContents()
	definition = node.type().definition()

	parm_group = definition.parmTemplateGroup()
	parm_folder = hou.FolderParmTemplate("Shading", "Shading")
	master_folder = hou.FolderParmTemplate("Master", "Master")

	categories_template = hou.StringParmTemplate("categories", "Categories", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
	categories_template.setHelp("A list of tags which can be used to select the object")
	categories_template.setTags({"spare_category": "Shading"})
	parm_folder.addParmTemplate(categories_template)

	reflectmask_template = hou.StringParmTemplate("reflectmask", "Reflection Mask", 1, default_value=(["*"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.NodeReferenceList, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
	reflectmask_template.setHelp("Objects that will be reflected on this object.")
	reflectmask_template.setTags({"opexpand": "1", "opfilter": "!!OBJ/GEOMETRY!!", "oprelative": "/obj", "spare_category": "Shading"})
	parm_folder.addParmTemplate(reflectmask_template)

	refractmask_template = hou.StringParmTemplate("refractmask", "Refraction Mask", 1, default_value=(["*"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.NodeReferenceList, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
	refractmask_template.setHelp("Objects that will be refracted on this object.")
	refractmask_template.setTags({"opexpand": "1", "opfilter": "!!OBJ/GEOMETRY!!", "oprelative": "/obj", "spare_category": "Shading"})
	parm_folder.addParmTemplate(refractmask_template)

	lightmask_template = hou.StringParmTemplate("lightmask", "Light Mask", 1, default_value=(["*"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.NodeReferenceList, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
	lightmask_template.setHelp("Lights that illuminate this object.")
	lightmask_template.setTags({"opexpand": "1", "opfilter": "!!OBJ/LIGHT!!", "oprelative": "/obj", "spare_category": "Shading"})
	parm_folder.addParmTemplate(lightmask_template)

	lightcategories_template = hou.StringParmTemplate("lightcategories", "Light Selection", 1, default_value=(["*"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
	lightcategories_template.setTags({"spare_category": "Shading"})
	parm_folder.addParmTemplate(lightcategories_template)
	
	aovs_template = hou.StringParmTemplate("aovs", "AOVS:", 1, default_value=([node.type().name()]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
	parm_folder.addParmTemplate(aovs_template)

	lightParms = ["categories", "reflectmask", "refractmask", "lightmask", "lightcategories"]
	for child in node.allSubChildren(top_down=True, recurse_in_locked_nodes=True):
		#print child.type().name()
		if child.type().name()=="geo":
			childPath = child.path()
			print childPath
			coef = int(len(childPath.split("/"))-len(node.path().split("/")))		
			trr = ""
			for i in range(0, coef):
				trr=trr+"../"		
			for ligthParm in lightParms:
				hou.parm(childPath+"/"+ligthParm).setExpression('chsop("'+trr+ligthParm+'")', language=None, replace_expression=True)

	##### MASTER ##########
	m_t_template = hou.FloatParmTemplate("m_t", "M_Translete", 3, default_value=([0, 0, 0]), min=-1, max=1, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.XYZW)
	m_t_template.setTags({"autoscope": "1110000000000000", "script_action": "import objecttoolutils\nobjecttoolutils.matchTransform(kwargs, 0)", "script_action_help": "Select an object to match the translation with.", "script_action_icon": "BUTTONS_match_transform"})
	master_folder.addParmTemplate(m_t_template)

	m_r_template = hou.FloatParmTemplate("m_r", "M_Rotate", 3, default_value=([0, 0, 0]), min=0, max=360, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.XYZW)
	m_r_template.setTags({"autoscope": "1110000000000000", "script_action": "import objecttoolutils\nobjecttoolutils.matchTransform(kwargs, 1)", "script_action_help": "Select an object to match the rotation with.", "script_action_icon": "BUTTONS_match_rotation"})
	master_folder.addParmTemplate(m_r_template)

	m_s_template = hou.FloatParmTemplate("m_s", "M_Scale", 3, default_value=([1, 1, 1]), min=-1, max=1, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.XYZW)
	m_s_template.setTags({"autoscope": "1110000000000000", "script_action": "import objecttoolutils\nobjecttoolutils.matchTransform(kwargs, 2)", "script_action_help": "Select an object to match the scale with.", "script_action_icon": "BUTTONS_match_scale"})
	master_folder.addParmTemplate(m_s_template)

	m_scale_template = hou.FloatParmTemplate("m_scale", "M Uniform Scale", 1, default_value=([1]), min=0, max=10, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
	m_scale_template.setTags({"autoscope": "0000000000000000"})
	master_folder.addParmTemplate(m_scale_template)
	
	m_keeppos_template = hou.ToggleParmTemplate("m_keeppos", "Keep Position When Parenting", 0)
	m_keeppos_template.setTags({"autoscope": "0000000000000000"})
	master_folder.addParmTemplate(m_keeppos_template)

	hou.parm(node.path()+"/Master/tx").setExpression('ch("../m_tx")', language=None, replace_expression=True)
	hou.parm(node.path()+"/Master/ty").setExpression('ch("../m_ty")', language=None, replace_expression=True)
	hou.parm(node.path()+"/Master/tz").setExpression('ch("../m_tz")', language=None, replace_expression=True)
	hou.parm(node.path()+"/Master/rx").setExpression('ch("../m_rx")', language=None, replace_expression=True)
	hou.parm(node.path()+"/Master/ry").setExpression('ch("../m_ry")', language=None, replace_expression=True)
	hou.parm(node.path()+"/Master/rz").setExpression('ch("../m_rz")', language=None, replace_expression=True)
	hou.parm(node.path()+"/Master/sx").setExpression('ch("../m_sx")', language=None, replace_expression=True)
	hou.parm(node.path()+"/Master/sy").setExpression('ch("../m_sy")', language=None, replace_expression=True)
	hou.parm(node.path()+"/Master/sz").setExpression('ch("../m_sz")', language=None, replace_expression=True)
	hou.parm(node.path()+"/Master/scale").setExpression('ch("../m_scale")', language=None, replace_expression=True)
	hou.parm(node.path()+"/Master/keeppos").setExpression('ch("../m_keeppos")', language=None, replace_expression=True)
	
	parm_group.append(master_folder)
	parm_group.append(parm_folder)
	definition.setParmTemplateGroup(parm_group)
	definition.updateFromNode(node)
	node.matchCurrentDefinition()
	
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
	
def hdaAddVersion():
	enterComment = hou.ui.readInput("Comment: ", buttons=('OK',), severity=hou.severityType.Message)
	usr = os.environ["COMPUTERNAME"].lower()
	comment = usr + ":: " + enterComment[1]

	node = hou.selectedNodes()[0] #grab the first selected node
	try:
		hou.parm(n.path()+"/comment").set(comment)
	except:
		pass
	definition = node.type().definition()
	definition.setComment(comment)
	hdaFile = definition.libraryFilePath() #find the hda file path
	versions = []
	for d in hou.hda.definitionsInFile(hdaFile):
		versions.append(d.nodeTypeName().split('::')) #I name the definition myAsset::1.4
	latestVersion = 0

	if len(versions[-1])>1:
		latestVersion = int(versions[-1][-1]) # from myAsset::1.4 -> 1
		
	hdaNewVersion = str((latestVersion+1)).zfill(3)
	hdaNewName = versions[-1][0]+"::"+hdaNewVersion
	#hdaNewName = versions[-1][0]
	newHdaFile = hdaFile.rsplit("/", 1)[0]+"/"+versions[-1][0]+".v"+hdaNewVersion+".hda"
	#print "newFile: "+newHdaFile
	#print "oldFile: "+hdaFile
	#newDefinition = definition.copyToHDAFile(newHdaFile, new_name=hdaNewName ) #return None no matter what but set for readability
	newDefinition = definition.copyToHDAFile(hdaFile, new_name=hdaNewName ) #return None no matter what but set for readability
	#latestDefinition = hou.hda.definitionsInFile(newHdaFile)
	latestDefinition = hou.hda.definitionsInFile(hdaFile)
	#node = node.changeNodeType(hdaNewName , keep_network_contents=False)
	node = node.changeNodeType(hdaNewName , keep_network_contents=False)
	last = latestDefinition[-1]
	last.setVersion(str(hdaNewVersion))
	print "Latest version:"+hdaNewVersion

def textToFolder():
	print "a"
	node = hou.selectedNodes()[0]
	childrens = node.allSubChildren()
	for imgMode in childrens:
		if imgMode.type().name()=='arnold::image':
			imagePath = hou.parm(imgMode.path()+"/filename").evalAsString()
			newImagePath = "`chs('../../../../texture_folder')`/"+imagePath.split("/")[-1]
			hou.parm(imgMode.path()+"/filename").set(newImagePath)
			imagePath = imagePath.replace('<udim>', '1001').replace('%(UDIM)d', '1001')
			fileName = os.path.split(imagePath)[-1]
			newFolder = "O:/props/realGrass"
			#try:
			copyfile(imagePath, newFolder+"/"+fileName)