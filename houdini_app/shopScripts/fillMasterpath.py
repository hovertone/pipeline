#print '=========== in fillMasterpath ============='

def getcommonletters(strlist):
    return ''.join([x[0] for x in zip(*strlist) \
                     if reduce(lambda a,b:(a == b) and a or None,x)])

def findcommonstart(strlist):
    strlist = strlist[:]
    prev = None
    while True:
        common = getcommonletters(strlist)
        if common == prev:
            break
        strlist.append(common)
        prev = common

    return getcommonletters(strlist)

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

tp = hou.pwd()
button_name = 'find_master_substring'

grp = tp.parmTemplateGroup()
button = grp.find(button_name)

f = grp.find('textures_folder')
parms_to_avoid = tp.parm('parms_to_keep').eval().split(' ')
parm_names = [p.name() for p in f.parmTemplates() if p.name() and p.name() not in parms_to_avoid]
parm_d = dict()
for p in parm_names:
    parm_d[tp.parm(p)] = tp.parm(p).rawValue()

paths = parm_d.values()

if button.label() == 'Fill Masterpath':
    common_start =  findcommonstart(paths)
    ss_ind = len(common_start)
    first = paths[0]
    slash_indexes = find(first, '/')
    for i, si in enumerate(slash_indexes):
        if si > ss_ind:
            break

    substring = first[:slash_indexes[i]] #-1

    button.setLabel('Remove link')
    grp.replace(button_name, button)

    tp.parm('master_path').set(substring)
    for pn in parm_names:
        oldVal = tp.parm(pn).rawValue()
        tp.parm(pn).set(oldVal.replace(substring, '`chs("master_path")`'))

    grp.replace(button_name, button)
    tp.setParmTemplateGroup(grp)
else:
    master_path = tp.parm('master_path').eval()
    tp.parm('master_path').set('')
    for pn in parm_names:
        oldVal = tp.parm(pn).rawValue()
        tp.parm(pn).set(oldVal.replace('`chs("master_path")`', master_path))

    button.setLabel('Fill Masterpath')
    grp.replace(button_name, button)
    tp.setParmTemplateGroup(grp)


