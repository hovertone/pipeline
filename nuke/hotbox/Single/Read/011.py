#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: 1001 start
#
#----------------------------------------------------------------------------------------------------------

for n in nuke.selectedNodes('Read'):
    n['frame_mode'].setValue('start at')
    n['frame'].setValue('1001')