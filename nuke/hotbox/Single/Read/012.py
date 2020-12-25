#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Localize ON
#
#----------------------------------------------------------------------------------------------------------

nodes = nuke.selectedNodes('Read')
for n in nodes:
    n['localizationPolicy'].setValue("on")