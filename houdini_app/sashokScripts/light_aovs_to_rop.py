import hou

def main():
    print 'in main latr'

    nn = hou.selectedNodes()
    print 'sel nodes %s' % str(nn)
    contrib = ['RGBA_' + i.parm('ar_aov').eval() for i in nn]
    contrib = list(set(contrib))
    print 'cccc ' + str(contrib)
    return

    out = hou.node('/out')
    obj = hou.node('/obj')
    rr = [rop for rop in out.allNodes() if rop.type().name() == 'arnold']
    #rr += obj.allNodes()
    #print type(rr)
    ropToAdjust = hou.ui.selectFromList([i.name() for i in rr if i.type().name() == 'arnold'])
    for i in ropToAdjust:
        r = rr[i]
        print r.name()
        #contrib_local = contrib
        aovs_amount = int(r.parm('ar_aovs').eval())
        aovs = [r.parm('ar_aov_label%s'%str(i+1)).eval() for i in range(aovs_amount)]

        for j, c in enumerate(contrib):
            if c not in aovs:
                r.parm('ar_aovs').set(int(r.parm('ar_aovs').eval()) + 1)
                r.parm('ar_aov_label%s' % str(int(r.parm('ar_aovs').eval()))).set(c)
                print 'ADDED %s to %s TOP' % (c, r.name())