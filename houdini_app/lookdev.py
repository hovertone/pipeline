
import os
import hou
from houdini_app.lokyScripts import lokyLayoutS
reload(lokyLayoutS)



def main(assetname=None):

    # Create nodes
    obj = hou.node('/obj')
    out = hou.node('/out')
    geo = obj.createNode('geo')
    arn = out.createNode('arnold')
    null_light = obj.createNode('null')
    null_geo = obj.createNode('null')
    cam1 = obj.createNode('cam')
    cam2 = obj.createNode('cam')
    light = obj.createNode('arnold_light')
    geo_file = geo.createNode('geo')

    if assetname:
        geo.setName(assetname)
        arn.setName("lookdev")

    lokyLayoutS.createShader(operator=geo, node_out=(geo_file,))
    light.parm("ar_light_type").set(6)
    light.parm("ar_format").set(2)
    light.parm("ar_light_color_type").set(2)
    ligh_shader = hou.node(light.path() + "/shopnet/arnold_vopnet")
    out_light = ligh_shader.children()[0]
    light_image = ligh_shader.createNode("image")
    light_image.parm("filename").set("L:/_RESOURCES/HDRI/luxo-jr_hdr/Luxo-Jr_4000x2000.exr")
    out_light.setInput(0, light_image, 0)


    # Setup parameters
    hou.playbar.setPlaybackRange(1, 300)
    hou.hscript("setenv FSTART = " + "1")
    hou.hscript("setenv FEND = " + "300")
    setGobalFrangeExpr = "tset `({0}-1)/$FPS` `{1}/$FPS`".format(1, 300)
    hou.hscript(setGobalFrangeExpr)

    light.setInput(0, null_light, 0)
    geo.setInput(0, null_geo, 0)

    cam1.parm("ty").set(1)
    cam1.parm("tz").set(5)

    cam2.parm("ty").set(1.7)
    cam2.parm("tz").set(1.2)

    # Animate Light
    parm = null_geo.parm('ry')
    parm.setKeyframe(hou.Keyframe(0))
    hou.setFrame(150)
    parm.setKeyframe(hou.Keyframe(360))

    # Animate Geo
    parm = null_light.parm('ry')
    parm.setKeyframe(hou.Keyframe(0))
    hou.setFrame(300)
    parm.setKeyframe(hou.Keyframe(360))

    # Rename nodes
    obj.layoutChildren()
    geo.layoutChildren()




