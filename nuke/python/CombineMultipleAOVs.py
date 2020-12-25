import os
import nuke
from glob import glob
import re

def main():
    read = nuke.selectedNode()
    filePath = read['file'].value()
    folder = os.path.dirname(filePath)
    aovs = [i for i in os.listdir(folder) if '.' not in i]
    for i, aov in enumerate(aovs):
        #nuke.Layer(aov, ['red', 'green', 'blue'])
        nuke.tcl("add_layer", "%s %s.red %s.green %s.blue" % (aov, aov, aov, aov))
        exrs = sorted(os.listdir(os.path.join(folder, aov)))

        ff = re.search(r'\.(\d{4})\.', exrs[0]).group(1)
        lf = re.search(r'\.(\d{4})\.', exrs[-1]).group(1)

        #print ff, lf
        aovPath = os.path.join(folder, aov, exrs[0].replace(ff, '####')).replace('\\', '/')
        r = nuke.createNode('Read', 'file %s first %s last %s origfirst %s origlast %s format %s' % (aovPath, ff, lf, ff, lf, 'HD_1080'))
        r['postage_stamp'].setValue(False)
        # r['file'].setValue(aovPath)
        # r['first'].setValue(int(ff))
        # r['origfirst'].setValue(int(ff))
        # r['last'].setValue(int(lf))
        # r['origlast'].setValue(int(lf))

        r.setXYpos(read.xpos() + 110, read.ypos() + (i+1)*110)

        # if aov not in nuke.layers():
        #     nuke.Layer(aov, ['red', 'green', 'blue'])
        #     print '%s layer created' % aov
        # else:
        #     print '%s layer exists' % aov

        # sc = nuke.nodes.ShuffleCopy()
        # sc['out2'].setValue(aov)
        #
        # sc['alpha'].setValue('alpha2')
        # sc['black'].setValue('red1')
        # sc['white'].setValue('green1')
        # sc['red2'].setValue('blue')
        #
        # sc.setXYpos(read.xpos(), read.ypos() + (i+1)*110)
        #
        # if i == 0:
        #     sc.setInput(0, read)
        #     sc.setInput(1, r)
        #     connect = sc
        # else:
        #     sc.setInput(0, connect)
        #     sc.setInput(1, r)
        #     connect = sc
# =========================================================
        c = nuke.nodes.Copy()
        print 'aov %s' % aov

        c['from0'].setValue('rgba.red')
        c['to0'].setValue('%s.red' % aov)

        c['from1'].setValue('rgba.green')
        c['to1'].setValue('%s.green' % aov)

        c['from2'].setValue('rgba.blue')
        c['to2'].setValue('%s.blue' % aov)

        c['bbox'].setValue('B side')

        c.setXYpos(read.xpos(), read.ypos() + (i+1)*110)

        if i == 0:
            c.setInput(0, read)
            c.setInput(1, r)
            connect = c
        else:
            c.setInput(0, connect)
            c.setInput(1, r)
            connect = c




