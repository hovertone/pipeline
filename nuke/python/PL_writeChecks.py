import os
import nuke

def checkBeforeRender():
    n = nuke.thisNode()
    if not os.path.exists(os.path.dirname(n['file'].value())):
        os.makedirs(os.path.dirname(n['file'].value()))
        print 'Had to create folder\n%s' % os.path.dirname(n['file'].value())

    if 'forDaily' in n['file'].value():
        format = n.format()
        f_w = int(format.width())
        f_h = int(format.height())

        bbox = n.bbox()
        bb_w = int(bbox.w())
        bb_h = int(bbox.h())

        if bb_w != f_w and bb_h != f_h:
            raise Exception('Bbox is outside format range')
