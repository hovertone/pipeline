print '\n\n\n================== in bake paths ======================'
import hou
try:
    shopnet = hou.pwd().parent()
    parms_to_bake = ['filename', 'color_family', 'color_space']
    for s in shopnet.children():
        print s.name()
        for i in s.children():
            if i.type().name() == 'arnold::image':
                for ptb in parms_to_bake:
                    print '\t\t:::: baking %s type' % ptb
                    p = i.parm(ptb)
                    # LINKED PARMS BAKING
                    val = p.eval()
                    p.revertToDefaults()
                    p.set(val)
                    print "\t%s's filename parameter has been baked" % i.name()
except:
    pass
