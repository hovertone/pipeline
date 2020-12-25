tp = hou.pwd()
button_name = 'link_master_substring'

grp = tp.parmTemplateGroup()
button = grp.find(button_name)

f = grp.find('textures_folder')
parms_to_avoid = tp.parm('parms_to_keep').eval().split(' ')
parm_names = [p.name() for p in f.parmTemplates() if p.name() and p.name() not in parms_to_avoid and '_cs' not in p.name()]

# for p in parm_names:
#     print p

mp = tp.parm('master_path')
if button.label() == 'Link':
    if mp.rawValue() != '':
        for p in parm_names:
            if mp.rawValue() in tp.parm(p).rawValue():
                oldVal = tp.parm(p).rawValue()
                newVal = oldVal.replace(mp.rawValue(), '`chs("master_path")`')
                tp.parm(p).set(newVal)
        button.setLabel('Unlink')
        grp.replace(button_name, button)
        tp.setParmTemplateGroup(grp)
    else:
        hou.ui.displayMessage('Masterpath folder should not be empty')
else:
    for p in parm_names:
        if'`chs("master_path")`' in tp.parm(p).rawValue():
            oldVal = tp.parm(p).rawValue()
            newVal = oldVal.replace('`chs("master_path")`', mp.rawValue())
            tp.parm(p).set(newVal)
    mp.set('')
    button.setLabel('Link')
    grp.replace(button_name, button)
    tp.setParmTemplateGroup(grp)