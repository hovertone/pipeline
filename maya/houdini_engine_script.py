asset = cmds.ls(type="houdiniAsset")[0]

start = int(cmds.playbackOptions(q=True, min=True))
end = int(cmds.playbackOptions(q=True, max=True))

for i in range(end - start + 1):
    cmds.setAttr(asset + ".houdiniAssetParm.houdiniAssetParm_execute__button", 1)
    cmds.currentTime(start)
    start += 1






# CREATE ASSET AND SET SELECT
import maya.mel as mel
cmds.delete(cmds.ls(type="houdiniAsset"))
asset = mel.eval('houdiniEngine_loadAsset "O:/fx/mayatobgeo.hda" "Sop/mayatobgeo::001";')
setSelectio = mel.eval('AEhoudiniAssetSetInputToSelection ' + asset + '.input[0].inputNodeId;')




# EXPORT BGEO SQ
asset = cmds.ls(type="houdiniAsset")[0]
start = int(cmds.playbackOptions( q=True,min=True ))
end  = int(cmds.playbackOptions( q=True,max=True ))

for i in range(end-start+1):
    cmds.setAttr(asset+".houdiniAssetParm.houdiniAssetParm_execute__button", 1)
    cmds.currentTime(start)
    start +=1