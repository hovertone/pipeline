def main():
    print 'in create new'
    node = hou.node('/obj/dummy1')
    definition = node.type().definition()
    #hdaFile = definition.libraryFilePath()
    newDefinition = definition.copyToHDAFile('O:/props/test111.hda', new_name='aa', new_menu_name='sss')
    print newDefinition

