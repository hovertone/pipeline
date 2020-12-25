#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: TEXTURE LABEL
#
#----------------------------------------------------------------------------------------------------------

import os
for n in nuke.selectedNodes('Read'):
    f = n['file'].value()
    tail = os.path.split(f)[-1]
    filename = tail.split('.')[0]
    print filename
    ff = n['first'].value()
    lf = n['last'].value()
    n['label'].setValue('%s\n%s - %s' % (filename, ff, lf))