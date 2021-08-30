# coding=utf-8



import hou
labels = ["OLD", "NEW"]
inputvalue = hou.ui.readMultiInput(message = 'Raplace Path Text', input_labels =  ["OLD", "NEW"], buttons=('OK','Cancel'))
true = inputvalue[0]
old = inputvalue[1][0]
new = inputvalue[1][1]
nodeParms = []
if true == 0:
    selectedNodes = hou.selectedNodes()
    for seleted in selectedNodes:
        nodeParms = seleted.parms()
        for nodeParm in nodeParms:
            imagePath = nodeParm.evalAsString()
            if type(nodeParm.eval())==str:
                if old in imagePath:
                    try:
                        nodeParm.set(imagePath.replace(old, new))
                    except:
                        pass
        childrens = seleted.allSubChildren(top_down=True, recurse_in_locked_nodes=False)
        for node in childrens:
            nodeParms = node.parms()
            for nodeParm in nodeParms:
                imagePath = nodeParm.evalAsString()
                if type(nodeParm.eval()) is str:
                    if old in imagePath:
                        try:
                            nodeParm.set(imagePath.replace(old, new))
                        except:
                            pass


