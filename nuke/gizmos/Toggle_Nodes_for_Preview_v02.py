import nuke


def Toggle_Nodes_for_Preview():

    #Check if any node is selected

    if nuke.selectedNodes() != []:
        
        #Create string to hold selected nodes
    
        nodesToToggle = []
        
        for n in nuke.selectedNodes():
            nodesToToggle.append(n.name())
        
        
        #Create NoOp node
        
        myNode = nuke.nodes.NoOp()
        myNode.knob('label').setValue('Toggle Nodes')
        
        
        #Create button to toggle nodes 
        
        myTab = nuke.Tab_Knob('ToggleNodes_Tab', 'ToggleNodes')
        myButton = nuke.PyScript_Knob('ToggleNodes_Button', 'ToggleNodes')
        myNode.addKnob(myTab)
        myNode.addKnob(myButton)
        
        myNode.knob('ToggleNodes_Button').setCommand('nodesToDisable = ' + str(nodesToToggle) + ' \nfor n in nodesToDisable: \n    try:\n        currentNode = nuke.toNode(n) \n        currentValue = currentNode["disable"].getValue() \n        currentNode["disable"].setValue(not(currentValue))\n    except:\n        pass')

        
    else:

        nuke.message('No nodes selected.')