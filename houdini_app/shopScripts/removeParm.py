#print '========= in remove parm =========='

node = hou.pwd()
grp = node.parmTemplateGroup()
f = grp.find('textures_folder')
parms_to_avoid = node.parm('parms_to_keep').eval().split(' ')
existing_texture_names = [i.name() for i in f.parmTemplates() if i.name() not in parms_to_avoid and '_cs' not in i.name()]
res = hou.ui.selectFromList(existing_texture_names, message = 'Select parms to delete', exclusive = False)
for i in res:
    grp.remove(existing_texture_names[i])
    grp.remove(existing_texture_names[i]+'_cs')

node.setParmTemplateGroup(grp)
