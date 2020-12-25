
import maya.cmds as cmds


def GeosetAttrUI():
    assets = cmds.ls(sl=True)
    for asset in assets:
        cmds.select(asset)
        atrs = ['assetname', 'componentname']

        for a in atrs:
            try:
                cmds.addAttr(ln=a, dt="string")
            except:
                pass

    cmds.select(assets)


    # UI CREATE
    if cmds.window('addAttr', exists=True):
        cmds.deleteUI('addAttr')
    cmds.window('addAttr', title="addAttrValue")
    cmds.columnLayout(adj=True, w=100, h=100)

    cmds.optionMenu('assetType', label='Asset type:')
    cmds.menuItem(label='env')
    cmds.menuItem(label='props')
    cmds.menuItem(label='char')

    cmds.text("Asset Name")
    tf = cmds.textField("attrValue")
    cmds.text("Component Name")
    tf2 = cmds.textField("attrValue2")
    cmds.button(l="Add Attributes", c=GeoaddAttrFromUi)
    cmds.separator()
    cmds.button(l="Export", c=testing)
    cmds.setParent('..')
    cmds.showWindow('addAttr')


def GeoaddAttrFromUi(tf):
    s3 = cmds.ls(sl=True)

    assetname = cmds.textField('attrValue', q=True, text=True)
    componentname = cmds.textField('attrValue2', q=True, text=True)
    for i in s3:
        cmds.setAttr(i + ".assetname", assetname, type="string")
        cmds.setAttr(i + ".componentname", componentname, type="string")


def testing(s):
    a = cmds.optionMenu('assetType', q=True, text=True)
    print "SSSSSS"
    print s












