#print '\n\n\n================== in bake paths ======================'
shopnet = hou.pwd().parent()
for s in shopnet.children():
    print s.name()
    for i in s.children():
        if i.type().name() == 'arnold::image':
            p = i.parm('filename')
            # LINKED PARMS BAKING
            val = p.eval()
            p.revertToDefaults()
            p.set(val)
            print "\t%s's filename parameter has been baked" % i.name()