#print '============== in Images To ACES ================'
shopnet = hou.pwd().parent()
for s in shopnet.children():
    for i in s.children():
        if i.type().name() == 'arnold::image':
            i.parm('color_family').set('ACES')
            i.parm('color_space').set('ACES - ACEScg')