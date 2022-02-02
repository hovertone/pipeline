import os

node = hou.pwd()
grp = node.parmTemplateGroup()
f = grp.find('textures_folder')
parm_to_del = [p for p in f.parmTemplates() if p.name()]
parms_to_keep = node.parm('parms_to_keep').eval().split(' ')
for p in parm_to_del:
    if p.name() not in parms_to_keep:
        print('removing %s parm' % p.name())
        grp.remove(p.name())


node.setParmTemplateGroup(grp)
