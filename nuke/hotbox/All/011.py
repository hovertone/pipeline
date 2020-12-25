#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: path replace
#
#----------------------------------------------------------------------------------------------------------

for r in nuke.allNodes():
    if r.Class() == 'Read' or r.Class() == 'RedGeo':
        path = r['file'].value()
        newPath = path.replace('P:/', 'V:/')
        r['file'].setValue(newPath)