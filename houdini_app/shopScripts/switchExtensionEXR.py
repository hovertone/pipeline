#print '\n\n\n ================ in switch extension ================'
import os
import hou

#try:
node = hou.pwd()

grp = node.parmTemplateGroup()
folder = grp.find('textures_folder')
#replace_ext = '.exr'

parm_names = []
for t in folder.parmTemplates():
    if t.type() == hou.parmTemplateType.String and t.name() != 'master_path' and '_cs' not in t.name() and '_cf' not in t.name():
        parm_names.append(t.name())

allPaths = len(parm_names)

non_c = 0
for pn in parm_names:
    print('name %s' % pn)
    p = node.parm(pn)
    pp = grp.find(pn)
    tags = pp.tags()
    replace_ext = tags['ext']
    if replace_ext not in p.rawValue():
        oldVal = p.rawValue()
        cur_ext = os.path.splitext(oldVal)[-1]
        newVal = oldVal.replace(cur_ext, replace_ext)
        p.set(newVal)

