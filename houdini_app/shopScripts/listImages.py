import hou
import os

#print '\n\n\n================== in list images ======================'
shopnet = hou.pwd().parent()
for s in shopnet.children():
    print(s.name())
    for i in s.children():
        if i.type().name() == 'arnold::image':
            p = i.parm('filename')
            if p.rawValue() == p.eval():
                s = '  !not linked!  %s' % p.eval()
            else:
                s = '\t%s' % p.eval()
            print(s)
            #print '\t\tlinked: %s  |  ext: %s' % (p.rawValue() != p.eval(), os.path.splitext(p.eval())[-1])
