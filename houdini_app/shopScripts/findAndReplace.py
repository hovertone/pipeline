#print '=========== IN FIND REPLACE ============'

import hou

node = hou.pwd()
grp = node.parmTemplateGroup()
f = grp.find('textures_folder')
parms_to_avoid = node.parm('parms_to_keep').eval().split(' ')
existing_texture_names = [i.name() for i in f.parmTemplates() if i.name() not in parms_to_avoid]

if existing_texture_names == []:
    hou.ui.displayMessage('There are no textures to work with')
else:
    res = hou.ui.readMultiInput(message = 'What are we looking for?', input_labels =  ["Find", "Replace with"], buttons=('OK','Cancel'))
    if res[0] == 0: #USER CLICKED OK
        vals = res[1]
        find, replace = vals
        found = False
        for pn in existing_texture_names:
            oldVal = node.parm(pn).rawValue()
            if find in oldVal:
                found = True
                newVal = oldVal.replace(find, replace)
                node.parm(pn).set(newVal)
                print('%s replaced' % pn)

        if not found:
            hou.ui.displayMessage('No path matches the pattern "%s"' % find)