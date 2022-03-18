#print '\n\n\n ================ in switch extension ================'
import os
import hou

node = hou.pwd()

grp = node.parmTemplateGroup()
folder = grp.find('textures_folder')
replace_ext = '.tx'
parm_names = []
for t in folder.parmTemplates():
    if t.type() == hou.parmTemplateType.String and t.name() != 'master_path' and '_cs' not in t.name() and '_cf' not in t.name():
        parm_names.append(t.name())
allPaths = len(parm_names)

non_c = 0
for pn in parm_names:
    p = node.parm(pn)
    if replace_ext not in p.rawValue():
        non_c += 1

if non_c != 0:
    for pn in parm_names:
        p = node.parm(pn)
        oldVal = p.rawValue()
        cur_ext = os.path.splitext(oldVal)[-1]
        newVal = oldVal.replace(cur_ext, replace_ext)
        p.set(newVal)
# else:
#     for pn in parm_names:
#         p = node.parm(pn)
#         grp = node.parmTemplateGroup()
#         def_ext = grp.find(pn).tags()['ext']
#         oldVal = p.rawValue()
#         cur_ext = os.path.splitext(oldVal)[-1]
#         newVal = oldVal.replace(replace_ext, def_ext)
#         p.set(newVal)

