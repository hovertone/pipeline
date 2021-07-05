#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Linear sRGB
# COLOR: #6a55ff
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

for n in nuke.selectedNodes('Read'):
        n['colorspace'].setValue('Utility - Linear - sRGB')