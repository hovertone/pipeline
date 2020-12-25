import maya.cmds as cmd
import re, os


def exportCharToABC(charName = ''):
	if charName not in ['marine', 'battlemage', 'assasin', 'raccoon', 'ctulhu', 'tentacle']:
		print 'charName is invalid'
		return

	start = str(cmds.playbackOptions(query=True, minTime=True))
	end = str(cmds.playbackOptions(query=True, maxTime=True))

	scriptPath = cmds.file(query=True,sn=True)
	fileName = os.path.split(scriptPath)[-1]
	try:
	    rs = re.search(u'\S\H(\d{3})\.(\d{4})', fileName)
	    shot, ver = rs.group(1), rs.group(2)
	except:
	    print 'error' #method return spot
	saveName = u'P:/alliance2/shots/SH%s/cache/anim/%s/%s_v%s.abc' % (shot, charName, charName, ver)
	saveFolder = os.path.dirname(saveName)
	if not os.path.exists(saveFolder):
	    os.makedirs(saveFolder)

	if charName == 'marine':
		objects = "marine:MetalArm_metalArm_41 marine:MetalArm_metalArm_37 marine:MetalArm_metalArm_38 marine:MetalArm_metalArm_39 marine:MetalArm_metalArm_40 marine:MetalArm_metalArm_11 marine:MetalArm_metalArm_63 marine:MetalArm_metalArm_09 marine:MetalArm_metalArm_10 marine:MetalArm_metalArm_27 marine:MetalArm_metalArm_28 marine:MetalArm_metalArm_24 marine:MetalArm_metalArm_20 marine:MetalArm_metalArm_21 marine:Legs_pants_01 marine:MetalArm_metalArm_64 marine:MetalArm_metalArm_12 marine:Head_REye_in marine:Body_body marine:Knees_knee_belts marine:MetalArm_metalArm_62 marine:MetalArm_metalArm_67 marine:MetalArm_metalArm_14 marine:MetalArm_metalArm_13 marine:MetalArm_metalArm_05 marine:MetalArm_metalArm_06 marine:MetalArm_metalArm_04 marine:MetalArm_metalArm_50 marine:MetalArm_metalArm_51 marine:Head_throat marine:Belt_Belt_03 marine:Belt_Belt_04 marine:Belt_Belt_02 marine:MetalArm_metalArm_42 marine:MetalArm_metalArm_43 marine:MetalArm_metalArm_44 marine:MetalArm_metalArm_45 marine:MetalArm_metalArm_71 marine:MetalArm_metalArm_72 marine:MetalArm_metalArm_68 marine:MetalArm_metalArm_69 marine:MetalArm_metalArm_52 marine:MetalArm_metalArm_53 marine:MetalArm_metalArm_48 marine:MetalArm_metalArm_49 marine:Head_hair marine:MetalArm_metalArm_65 marine:MetalArm_metalArm_66 marine:ShouldersArmor_shArmor_03 marine:Legs_boots_01 marine:Head_head_03 marine:MetalArm_metalArm_61 marine:Head_REye_out marine:Head_head_01 marine:MetalArm_metalArm_70 marine:MetalArm_metalArm_18 marine:MetalArm_metalArm_15 marine:MetalArm_metalArm_47 marine:MetalArm_metalArm_02 marine:MetalArm_metalArm_03 marine:MetalArm_metalArm_01 marine:MetalArm_metalArm_46 marine:MetalArm_metalArm_30 marine:MetalArm_metalArm_31 marine:MetalArm_metalArm_29 marine:MetalArm_metalArm_25 marine:MetalArm_metalArm_26 marine:MetalArm_metalArm_07 marine:MetalArm_metalArm_08 marine:MetalArm_metalArm_57 marine:MetalArm_metalArm_58 marine:MetalArm_metalArm_56 marine:MetalArm_metalArm_59 marine:MetalArm_metalArm_60 marine:MetalArm_metalArm_54 marine:MetalArm_metalArm_55 marine:Head_LEye_out marine:RArm_arm_07 marine:RArm_arm_02 marine:RArm_arm_03 marine:RArm_arm_04 marine:RArm_arm_01 marine:MetalArm_metalArm_36 marine:MetalArm_metalArm_33 marine:MetalArm_metalArm_34 marine:MetalArm_metalArm_32 marine:MetalArm_metalArm_35 marine:RArm_arm_06 marine:Belt_Belt_01 marine:Knees_knees marine:RArm_arm_05 marine:Head_LEye_in marine:Head_glasses marine:ShouldersArmor_shArmor_02 marine:ShouldersArmor_shArmor_01 marine:MetalArm_metalArm_22 marine:MetalArm_metalArm_23 marine:MetalArm_metalArm_19 marine:MetalArm_metalArm_16 marine:MetalArm_metalArm_17"
	elif charName == 'battlemage':
		objects = ''
	elif charName == 'assasin':
		objects = ''
	elif charName == 'raccoon':
		objects = ''
	elif charName == 'ctulhu':
		objects = ''
	command = "-frameRange %s %s -step 0.2 -uvWrite -writeFaceSets -wholeFrameGeo -worldSpace -dataFormat ogawa %s -file %s" % (start, end, objects, saveName)
	cmd.AbcExport ( j = command )

	msg = '%s %s has been exported to %s' % (charName, ver, saveName)
	cmd.confirmDialog(title='SUCCESS', message=msg, button=['OK'], defaultButton='OK')


