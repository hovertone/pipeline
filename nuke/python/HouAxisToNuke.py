def importHouAxis():	
	import pyperclip
	import nuke
	getclip = pyperclip.paste()
	objlist = getclip.split("_@")
	for node in objlist[1:]:
		keylist = node.split("_")
		axis = nuke.nodes.Axis()
		axis.setName(keylist[0])
		for keys in keylist[1:]:
			mass = keys.split(",")
			kt = axis['translate']
			kr = axis['rotate']
			kt.setAnimated()
			kr.setAnimated()
			kt.setValue(float(mass[1]), 0, time = float(mass[0]))
			kt.setValue(float(mass[2]), 1, time = float(mass[0]))
			kt.setValue(float(mass[3]), 2, time = float(mass[0]))
			kr.setValue(float(mass[4]), 0, time = float(mass[0]))
			kr.setValue(float(mass[5]), 1, time = float(mass[0]))
			kr.setValue(float(mass[6]), 2, time = float(mass[0]))

			