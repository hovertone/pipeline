import hou
import subprocess
import PySide2.QtGui as qtg
def hiplccc():
    nodes = hou.selectedNodes()
    text = "import hou\n"
    text = text+"net_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)\n"+"targetParent = net_editor.pwd()\n"
    text2 = ""
    preSub = nodes
    for preNodes in nodes:
        preSub = preSub+preNodes.allSubChildren(top_down=True, recurse_in_locked_nodes=False)
    for node in preSub:
        preparent = node.parent()
        parentPath = preparent.path()
        if preparent.isLockedHDA()==False:
            parent = "hou.node('"+parentPath+"')"
            type = node.type().name()
            name = node.name()
            connectors = node.inputConnectors()
            text = text+"newNode = targetParent.createNode('"+type+"', '"+name+"', run_init_scripts=False)\n"
            for connector in connectors:
                tttt = len(connector)
                if tttt>0:
                    #print "a"
                    indexx = str(connector[0].inputIndex())
                    outdexx = str(connector[0].outputIndex())
                    inputName = connector[0].inputItem().name()
                    text2 = text2 + "hou.node(targetParent.path()+'/'+'"+name+"').setInput("+indexx+", hou.node(targetParent.path()+'/'+'"+inputName+"'), "+outdexx+")\n"
                    text2 = text2 + "hou.node(targetParent.path()+'/'+'"+name+"').moveToGoodPosition(relative_to_inputs=True, move_inputs=True, move_outputs=True, move_unconnected=True)\n"     
            parms = node.parms()
            for parm in parms:
                parmName = str(parm.name())
                parmValPre = str(parm.evalAsString())
                if parmValPre=="on":
                    parmValue = str(parm.evalAsString()).replace('off', '0').replace('on', '1').replace("\n", "")
                else:
                    parmValue = str(parm.evalAsString()).replace('off', '0').replace("\n", "")
                text = text + "hou.parm(newNode.path()+'/'+'"+parmName+"').set('"+str(parmValue)+"')\n"
    layout = "hou.node(targetParent.path()).layoutChildren(items=(), -1.0, -1.0)\n"
    text = text+text2
    app = qtg.QGuiApplication.instance()
    clipboard = app.clipboard()
    clipboard.setText(text)