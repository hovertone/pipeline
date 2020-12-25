#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Rec. 709
# COLOR: #ff5f00
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

for n in nuke.selectedNodes('Read'):
        n['colorspace'].setValue('Output - Rec.709')