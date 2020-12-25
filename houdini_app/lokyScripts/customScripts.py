import hou

def shopToMat():
	toDels = []
	toRenames = []
	newNames = []
	selecteds = hou.selectedNodes()
	for selected in selecteds:
		if selected.type().name() == "shopnet":
			allnodes = (selected,)
		else:
			allnodes =list(selected.allSubChildren())
		for shopnet in allnodes:
			if shopnet.type().name() == "shopnet":	
				parentName = shopnet.name()
				baseParent = shopnet.parent()
				newname = parentName+"_MAT"
				newMatnet = baseParent.createNode("matnet", newname)
				
				childrens = shopnet.allSubChildren()
				oldvops = []
				newVops = []
				for node in childrens:
					if node.type().name() == "arnold_vopnet":
						code = node.asCode().replace(parentName, parentName+"_MAT").replace("arnold_vopnet", "arnold_materialbuilder").replace('if locals().get("hou_parent") is None:\n    ', '').replace('if locals().get("hou_node") is None:\n    ', '')
						exec(code)
						oldvops.append(node)
						newVops.append(hou_node)
				for idx, vop in enumerate(oldvops):
					secondChildrens = vop.children()
					newVops[idx].copyItems(secondChildrens, channel_reference_originals = False, relative_references = False, connect_outputs_to_multi_inputs = True)
				toDels.append(shopnet)
				toRenames.append(newMatnet)
				newNames.append(parentName)
				#shopnet.destroy()
				print newMatnet
				#newMatnet.setName(parentName, unique_name=False)
	for idx, newName in enumerate(newNames):
		toDels[idx].destroy()
		toRenames[idx].setName(newName, unique_name=False)
		