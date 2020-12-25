import os
import nuke
import nukescripts
import json
from CUF import selectOnly

def main():

    json_path = 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/toNuke.txt'
    with open(json_path) as json_file:
        data = json.load(json_file)

    print type(data)

    pos = nuke.toNode('start')


    #l = ['P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/default_material_sssmask_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/default_material_paint_layer_3_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/Default_Material_roughness_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/default_material_paint_layer_2_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/default_material_dirt_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/default_material_paint_layer_5_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/default_material_paint_layer_4_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/default_material_paint_layer_2_copy_2_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/default_material_orc_dispork_sculpt1_cc_dm_copy_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/orc_dispork_sculpt1-dm_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/default_material_paint_layer_4_BLUR_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/default_material_paint_layer_6_BLUR_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/rnd/GroundClay006_DISP_6K_linear.exr', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/Bake/Ork_BaseColor.<UDIM>_obj_bake.exr', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/default_material_sssmask_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/Default_Material_clown_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/1_ColorMask.<UDIM>.png', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/dispLowbody_02-DM_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/dispLowbody_02-DM_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/dispLowbody_02-DM_<UDIM>.tif', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/1_ColorMask.<UDIM>.png', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/1_ColorMask.<UDIM>.png', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/Bake/converted/displace_Bake_OrkArmor_<UDIM>.exr', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/Bake/Ork_Cavity.<UDIM>_obj_bake.exr', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/Bake/Ork_Roughness.<UDIM>_obj_bake.exr', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/texture/v008/Bake/converted/Paint_Bake_OrkWarior_<UDIM>.exr']
    counter = 0
    tex_counter = 0
    row = 1
    for s, path_list in data.iteritems():
        print s
        # sn = nuke.createNode('StickyNote')
        # sn['label'].setValue(s)
        # sn.setXYpos(pos.xpos() + 110, pos.ypos() + row * 140)

        #selectOnly()
        for ind, i in enumerate(path_list):
            tex_counter += 1

            #
            # if counter > 3:
            #     return # EXIT

            print i
        #
        #     r = nuke.createNode("Read")
        #     if '<UDIM>' in i:
        #         path = i.replace('<UDIM>', "####")
        #     else:
        #         path = i
        #     r['file'].setValue(path)
        #
        #     folder, file = os.path.split(i)
        #     if '<UDIM>' in i:
        #         allfiles = os.listdir(folder)
        #         pattern = file[:file.find('<UDIM>')-1]
        #         f_i = file.index('<UDIM>')-1
        #
        #         try:
        #             files = []
        #             for f in allfiles:
        #                 if pattern in f:
        #                     files.append(f)
        #
        #             ff = files[0][f_i+1:f_i+5]
        #             lf = files[-1][f_i+1:f_i+5]
        #
        #             r['first'].setValue(int(ff))
        #             r['origfirst'].setValue(int(ff))
        #
        #             r['last'].setValue(int(lf))
        #             r['origlast'].setValue(int(lf))
        #         except:
        #             print '%s :: %s ERROR' % (s, file)
        #
        #     r.setXYpos(sn.xpos() + (ind+1)*110, pos.ypos() + row * 140)
        #
        #
        # row += 1
        # counter += 1

    print '%s IN TOTOAL TEXS' % tex_counter