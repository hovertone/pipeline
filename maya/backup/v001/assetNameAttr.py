import maya.cmds as cmds


def addAttrMatGroup():
    s1 = cmds.select(cmds.ls(sl=True), hi=True)
    s2 = cmds.ls(sl=True, shapes=True)
    cmds.select(s2)
    s3 = cmds.ls(sl=True)

    for i in s3:
        cmds.addAttr(ln="matGroup", dt="string")


def setAttrUI():

    assets = cmds.ls(sl=True)
    for asset in assets:
        cmds.select(asset)
        try:
            cmds.addAttr(ln="assetname", dt="string")
        except:
            pass
    cmds.select(assets)


    if cmds.window('addAttr', exists=True):
        cmds.deleteUI('addAttr')
    cmds.window('addAttr', title="addAttrValue", w=180, h=150)
    cmds.columnLayout(adj=True)
    tf = cmds.textField("attrValue")
    cmds.button(l="ADD ATTR", c=addAttrFromUi)
    cmds.setParent('..')
    cmds.showWindow('addAttr')


def addAttrFromUi(tf):
    s3 = cmds.ls(sl=True)
    t = cmds.textField('attrValue', q=True, text=True)
    for i in s3:
        cmds.setAttr(i + ".assetname", t, type="string")
