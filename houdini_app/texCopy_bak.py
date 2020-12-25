import hou
import os
import shutil

def main():
    #print 'inside222'
    shop = hou.node('/obj/Ork_Warior_Shading1/Ork_Warior_Shader/shopnet1')
    pp = []
    for s in shop.children():
        if 'Texture' in s.name():
            # print s.name()
            parms = [i for i in s.parms() if 'tex' in i.name()]
            for p in parms:
                oldVal = p.eval()
                # print '\t%s' % oldVal
                if oldVal != '':
                    if '<UDIM>' in oldVal:
                        pp.append(oldVal[:oldVal.find('<UDIM>')])
                    else:
                        pp.append(oldVal)

    # for i, p in enumerate(sorted(pp)):
    #     print '%s :: %s' % (i, p)

    path1 = '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/texture/v008'
    path2 = '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/'
    toCopy = []
    for path in [path1, path2]:
        for rootDir, subdirs, filenames in os.walk(path):
            if filenames:
                for f in filenames:
                    fullPath = '%s/%s' % (rootDir, f)
                    fullPath = fullPath.replace('\\', '/')
                    for p in pp:
                        if p in fullPath:
                            # print "MATCH"
                            # print '\t' + p + '\n\t' + fullPath
                            if '.tx' in fullPath:
                                toCopy.append(fullPath)
                                break

    #toCopy = ['//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/8k_noise.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1001.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1002.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1003.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1004.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1005.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1006.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1007.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1008.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1009.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1011.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1012.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1013.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1014.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1001.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1002.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1003.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1004.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1005.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1006.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1007.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1008.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1009.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1011.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1012.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1013.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1014.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1001.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1002.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1003.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1004.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1005.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1006.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1007.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1008.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1009.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1011.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1012.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1013.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1014.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1001.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1002.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1003.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1004.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1005.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1006.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1007.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1008.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1009.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1011.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1012.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1013.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1014.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1001.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1002.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1003.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1004.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1005.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1006.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1007.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1008.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1009.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1011.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1012.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1013.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1014.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1001.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1002.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1003.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1004.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1005.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1006.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1007.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1008.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1009.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1011.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1012.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1013.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1014.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1001.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1002.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1003.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1004.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1005.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1006.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1007.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1008.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1009.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1011.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1012.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1013.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1014.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1001.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1002.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1003.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1004.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1005.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1006.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1007.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1008.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1009.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1011.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1012.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1013.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1014.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1014.tx']

    #hou.parm('/obj/Ork_Warior_Shading1/Ork_Warior_Shader/shopnet1/test/a').set(str(toCopy))

    for tc in toCopy:
        print tc

    # Create an interruptable operation.
    operation = hou.InterruptableOperation('Doing Work', long_operation_name ='Starting Tasks', open_interrupt_dialog = True)
    operation.__enter__()

    counter = 0
    num_tasks = len(toCopy)
    print '%s in total' % num_tasks
    for i, tc in enumerate(toCopy):
        percent = float(i) / float(num_tasks)
        destPath = tc.replace('//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/', 'P:/Raid/in/191008/tex/v003/')
        if '.tx' in destPath:
            folder = os.path.dirname(destPath)
            if not os.path.exists(folder):
                os.makedirs(folder)

            if os.path.exists(destPath):
                print 'LOCATED :: %s' % destPath
            else:
                print 'MISSING :: %s' % destPath

                try:
                    shutil.copy2(tc, destPath)
                    pass
                except Exception as e:
                    # print 'FOUND :: %s' % tc
                    # print 'DEST :: %s' % destPath
                    print(e)

        operation.updateLongProgress(percent, '%s' % destPath)

    # Stop the operation. This closes the progress bar dialog.
    operation.__exit__(None, None, None)

def replacePaths():
    shop = hou.node('/obj/Ork_Warior_Shading1/Ork_Warior_Shader/shopnet1')
    pp = []
    for s in shop.children():
        if 'Texture' in s.name():
            # print s.name()
            parms = [i for i in s.parms() if 'tex' in i.name()]
            for p in parms:
                oldVal = p.eval()
                if oldVal != '':
                    newVal = oldVal.replace('P:/Raid/in/191008/tex/v001/', '')
                    p.set(newVal)

def replacePathsYellowImages():
    shop = hou.node('/obj/Ork_Warior_Shading1/Ork_Warior_Shader/shopnet1')
    pp = []
    for s in shop.children():
        for t in [i for i in s.children() if 'arnold::image' in i.type().name() and '//vpstorage/vpd/pipeline_and_r_n_d/' in i.parm('filename').eval()]:
            oldVal = t.parm('filename').eval()
            newVal = oldVal.replace('//vpstorage/vpd/pipeline_and_r_n_d/arnold_shaders/shader_presets_textures/v002/tex/', 'P:/Raid/in/191008/tex/v001/rnd/')
            t.parm('filename').set(newVal)

def test():
    shop = hou.node('/obj/Ork_Warior_Shading1/Ork_Warior_Shader/shopnet1')
    pp = []
    for s in shop.children():
        if s.name() == 'Ork_warior_Skin':
            for t in [i for i in s.children() if 'arnold::image' in i.type().name() and '//vpstorage/vpd/pipeline_and_r_n_d/' in i.parm('filename').eval()]:
                # print s.name()
                #print '%s :: %s' % (t.name(), t.parm('filename').eval())
                val = t.parm('filename').eval().replace('//vpstorage', '//vpstorage.plarium.local')
                pp.append(val)

    #operation = hou.InterruptableOperation('Doing Work', long_operation_name='Starting Tasks',                                            open_interrupt_dialog=True)
    #operation.__enter__()

    counter = 0
    num_tasks = len(pp)
    for i, tc in enumerate(pp):
        #percent = float(i) / float(num_tasks)
        if '.tx' in tc:
            destPath = tc.replace('//vpstorage.plarium.local/vpd/pipeline_and_r_n_d/arnold_shaders/shader_presets_textures/v002/tex/',
                                  'P:/Raid/in/191008/tex/v002/')

            folder = os.path.dirname(destPath)
            if not os.path.exists(folder):
                os.makedirs(folder)

            if os.path.exists(destPath):
                print 'LOCATED :: %s' % destPath
            else:
                print 'MISSING :: %s' % destPath

                try:
                    shutil.copy2(tc, destPath)
                except Exception as e:
                    print '\tFOUND :: %s' % tc
                    print '\tDEST :: %s' % destPath
                    print(e)

                # counter += 1
                #
                # if counter > 2:
                #     return

        #operation.updateLongProgress(percent, '%s' % destPath)

    # Stop the operation. This closes the progress bar dialog.
    #operation.__exit__(None, None, None)

    #for p in pp:
    #    print p


def axeNodes():
    shop = hou.node('/obj/orc_warrior1/char_orc_warrior/Ork_Warior_Shader/shopnet1')
    pp = []
    for s in shop.children():
        if 'Axe' in s.name():
            # print s.name()
            for t in [i for i in s.children() if 'arnold::image' in i.type().name() and '//vpstorage.plarium.local/vpd/raid' in i.parm('filename').eval()]:

                oldVal = t.parm('filename').eval()

                newVal = oldVal.replace('//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior', '`chs("../../../../../texturefolder")`')
                t.parm('filename').set(newVal)
                # if oldVal != '':
                #     if '<UDIM>' in oldVal:
                #         pp.append(oldVal[:oldVal.find('<UDIM>')])
                #     else:
                #         pp.append(oldVal)

    # path1 = '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/_axe_/texture/v003/'
    # path2 = '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/_axe_/texture/v001'
    # toCopy = []
    # for path in [path1, path2]:
    #     for rootDir, subdirs, filenames in os.walk(path):
    #         if filenames:
    #             for f in filenames:
    #                 fullPath = '%s/%s' % (rootDir, f)
    #                 fullPath = fullPath.replace('\\', '/')
    #                 for p in pp:
    #                     if p in fullPath:
    #                         # print "MATCH"
    #                         # print '\t' + p + '\n\t' + fullPath
    #                         if '.tx' in fullPath:
    #                             toCopy.append(fullPath)
    #                             break
    #
    # # for p in pp:
    # #    print p
    #
    # # Create an interruptable operation.
    # operation = hou.InterruptableOperation('Doing Work', long_operation_name ='Starting Tasks', open_interrupt_dialog = True)
    # operation.__enter__()
    #
    # counter = 0
    # num_tasks = len(toCopy)
    # print '%s in total' % num_tasks
    # for i, tc in enumerate(toCopy):
    #     percent = float(i) / float(num_tasks)
    #     destPath = tc.replace('//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/', 'P:/Raid/assetBuilds/char/orc_warrior/main/tex/v001/')
    #     # if '.tx' in destPath:
    #     folder = os.path.dirname(destPath)
    #     if not os.path.exists(folder):
    #         os.makedirs(folder)
    #
    #     if os.path.exists(destPath):
    #         print 'LOCATED :: %s' % destPath
    #     else:
    #         print 'MISSING :: %s' % destPath
    #
    #         try:
    #             shutil.copy2(tc, destPath)
    #             pass
    #         except Exception as e:
    #             # print 'FOUND :: %s' % tc
    #             # print 'DEST :: %s' % destPath
    #             print(e)
    #
    #     operation.updateLongProgress(percent, '%s' % destPath)
    #
    # # Stop the operation. This closes the progress bar dialog.
    # operation.__exit__(None, None, None)

def findTXfile():
    shop = hou.node('/obj/orc_warrior1/char_orc_warrior/Ork_Warior_Shader/shopnet1')
    pp = []
    for s in shop.children():
        # print s.name()
        for t in [i for i in s.children() if 'arnold::image' in i.type().name() and 'GroundClay006_DISP_6K_linear.tx' in i.parm('filename').eval()]:
            print s.name(), ' :: ', t.name()

def selectImages():
    print 'done!1'
    #shader = hou.selectedNodes()[0]
    #shader.setSelected(False)
    shop = hou.node('/obj/orc_warrior1/char_orc_warrior/Ork_Warior_Shader/shopnet1')
    pp = []
    for s in shop.children():

        for t in s.children():
            if 'arnold::image' in t.type().name() and 'orcarmor_basecolor' in t.parm('filename').eval():
                print s.name()
                print '\t%s' % t.name()
                #t.parm('color_family').set('ACES')
                #t.parm('color_family').set('Utility')



# ZHEKA VORVALSYA
def main2():
    #print 'inside333'
    #return
    shop = hou.node('/obj/Skeleton_Geo1/Skeleton/Skeleton_Shader1/shopnet')
    pp = []
    for s in shop.children():
        if 'Pathes' in s.name():
            # print s.name()
            parms = [i for i in s.parms() if 'tex' in i.name()]
            for p in parms:
                oldVal = p.eval()
                # print '\t%s' % oldVal
                if oldVal != '':
                    if '<UDIM>' in oldVal:

                        pp.append(oldVal[:oldVal.find('<UDIM>')])
                    else:
                        pp.append(oldVal)

    for i, p in enumerate(sorted(pp)):
        print '%s :: %s' % (i, p)

    #path1 = '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/texture/v008'
    #path2 = '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/'
    toCopy = []
    path = '//vpstorage.plarium.local/vpd/raid/assets/characters/ice_golem/texturing/texture/v008/converted'
    for rootDir, subdirs, filenames in os.walk(path):
        if filenames:
            for f in filenames:
                fullPath = '%s/%s' % (rootDir, f)
                fullPath = fullPath.replace('\\', '/')
                for p in pp:
                    if p in fullPath:
                        # print "MATCH"
                        # print '\t' + p + '\n\t' + fullPath
                        if '.exr' in fullPath:
                            toCopy.append(fullPath)
                            break

    #toCopy = ['//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/8k_noise.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1001.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1002.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1003.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1004.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1005.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1006.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1007.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1008.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1009.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1011.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1012.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1013.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1014.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_basecolor.1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1001.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1002.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1003.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1004.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1005.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1006.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1007.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1008.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1009.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1011.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1012.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1013.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1014.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_metalness.1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1001.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1002.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1003.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1004.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1005.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1006.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1007.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1008.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1009.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1011.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1012.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1013.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1014.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_normal.1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1001.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1002.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1003.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1004.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1005.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1006.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1007.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1008.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1009.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1011.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1012.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1013.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1014.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/orcarmor_roughness.1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1001.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1002.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1003.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1004.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1005.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1006.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1007.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1008.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1009.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1011.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1012.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1013.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1014.exr', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/Bake/converted/displace_Bake_OrkArmor_1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1001.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1002.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1003.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1004.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1005.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1006.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1007.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1008.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1009.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1011.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1012.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1013.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1014.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/UV_1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1001.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1002.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1003.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1004.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1005.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1006.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1007.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1008.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1009.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1011.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1012.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1013.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1014.tif', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAY/RAY_1014.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1001.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1001.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1002.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1002.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1003.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1003.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1004.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1004.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1005.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1005.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1006.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1006.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1007.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1007.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1008.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1008.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1009.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1009.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1011.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1011.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1012.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1012.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1013.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1013.tx', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1014.png', '//vpstorage.plarium.local/vpd/raid/assets/characters/orc_warrior/armor_texture/v005/displace/RAYCAST_MASK/test_ColorMask.1014.tx']

    #hou.parm('/obj/Ork_Warior_Shading1/Ork_Warior_Shader/shopnet1/test/a').set(str(toCopy))

    # for tc in toCopy:
    #     print tc

    # Create an interruptable operation.
    operation = hou.InterruptableOperation('Doing Work', long_operation_name ='Starting Tasks', open_interrupt_dialog = True)
    operation.__enter__()

    counter = 0
    num_tasks = len(toCopy)
    print '%s in total' % num_tasks
    for i, tc in enumerate(toCopy):
        percent = float(i) / float(num_tasks)
        destPath = tc.replace('//vpstorage.plarium.local/vpd/raid/assets/characters/ice_golem/texturing/texture/v008/converted/', 'P:/Raid/assetBuilds/char/ice_golem/main/tex/v010/')
        if '.exr' in destPath:
            folder = os.path.dirname(destPath)
            if not os.path.exists(folder):
                os.makedirs(folder)

            if os.path.exists(destPath):
                print 'LOCATED :: %s' % destPath
            else:
                print 'MISSING :: %s' % destPath

                try:
                    shutil.copy2(tc, destPath)
                    pass
                except Exception as e:
                    # print 'FOUND :: %s' % tc
                    # print 'DEST :: %s' % destPath
                    print(e)

        operation.updateLongProgress(percent, '%s' % destPath)

    # Stop the operation. This closes the progress bar dialog.
    operation.__exit__(None, None, None)

def main3():
    #print 'inside333'
    #return
    ext = ['.exr', '.png', '.tif']
    destFolder = 'P:/Raid/assetBuilds/char/skeleton/main/tex/v005'
    shop = hou.node('/obj/Skeleton_Geo1/Skeleton/Skeleton_Shader1/shopnet')
    pp = []
    for s in shop.children():
        if len(s.parms()) > 0:
            # print s.name()
            parms = [i for i in s.parms()]
            for p in parms:
                oldVal = p.eval()
                # print '\t%s' % oldVal
                if oldVal != '':
                    oldVal = os.path.splitext(oldVal)[0]
                    if '//vpstorage/' in oldVal:
                        oldVal = oldVal.replace('//vpstorage/', '//vpstorage.plarium.local/')
                    if '<UDIM>' in oldVal:

                        pp.append(oldVal[:oldVal.find('<UDIM>')])
                    else:
                        pp.append(oldVal)

    for i, p in enumerate(sorted(pp)):
        print '%s :: %s' % (i, p)

    paths = []
    s = [os.path.split(i)[0] for i in pp]
    for i in set(s):
        paths.append(i)
    print paths



    toCopy = []
    #path = '//vpstorage.plarium.local/vpd/raid/assets/characters/ice_golem/texturing/texture/v008/converted'
    for path in paths:
        for rootDir, subdirs, filenames in os.walk(path):
            if filenames:
                for f in filenames:
                    fullPath = '%s/%s' % (rootDir, f)
                    fullPath = fullPath.replace('\\', '/')
                    #print fullPath
                    for p in pp:
                        if p in fullPath:
                            # print "MATCH"
                            # print '\t' + p + '\n\t' + fullPath
                            for e in ext:
                                if e in fullPath and '.tex' not in fullPath and fullPath not in toCopy:
                                    toCopy.append(fullPath)
                                    break

    #print 'pring to COPY'
    for tc in toCopy:
        print tc

    # Create an interruptable operation.
    operation = hou.InterruptableOperation('Doing Work', long_operation_name ='Starting Tasks', open_interrupt_dialog = True)
    operation.__enter__()

    counter = 0
    num_tasks = len(toCopy)
    print '%s in total' % num_tasks
    for i, tc in enumerate(toCopy):
        percent = float(i) / float(num_tasks)
        #destPath = tc.replace('//vpstorage.plarium.local/vpd/raid/assets/characters/ice_golem/texturing/texture/v008/converted/', 'P:/Raid/assetBuilds/char/ice_golem/main/tex/v010/')
        destPath = '%s/%s' % (destFolder, os.path.split(tc)[-1])
        folder = os.path.dirname(destPath)
        if not os.path.exists(folder):
            os.makedirs(folder)

        if os.path.exists(destPath):
            print 'LOCATED :: %s' % destPath
        else:
            print 'MISSING :: %s' % destPath

            try:
                shutil.copy2(tc, destPath)
                pass
            except Exception as e:
                # print 'FOUND :: %s' % tc
                # print 'DEST :: %s' % destPath
                print(e)

        operation.updateLongProgress(percent, '%s' % destPath)

    # Stop the operation. This closes the progress bar dialog.
    operation.__exit__(None, None, None)


def hairCache():
    nodes = hou.selectedNodes()
    #nodes = (hou.node('/obj/braid_hair_R_2'), hou.node('/obj/braid_hair_L_5'), hou.node('/obj/braid_hair_R_5'), hou.node('/obj/braid_hair_L_3'), hou.node('/obj/braid_hair_L_1'), hou.node('/obj/braid_hair_R_6'), hou.node('/obj/braid_hair_L_2'), hou.node('/obj/braid_hair_L_6'), hou.node('/obj/braid_hair_L_4'), hou.node('/obj/braid_hair_R_3'), hou.node('/obj/braid_hair_R_1'), hou.node('/obj/braid_hair_R_4'))
    for n in nodes:
        print n.name()
        #filecache = [i for i in n.children() if 'filecache' in n.type().name()]
        #print filecache
        for c in n.children():
            if c.type().name() == 'filecache':
                #print c.parm('file').eval()
                #print 'EXP : %s' %
                if c.color().rgb() == (0.28999999165534973, 0.5649999976158142, 0.8859999775886536):
                    print 'executing %s' % c.name()
                    print '\tswitching toggle '

                    c.parm('execute').pressButton()
                    c.parm('loadfromdisk').set(True)

def replacePaths():
    #print 'inside333'
    #return
    ext = ['.exr', '.png', '.tif'] #HARDCODE
    destFolder = '`chs("../../../texture_folder")`' #HARDCODE
    shop = hou.node('/obj/char_skeleton/skeleton/shopnet') #HARDCODE
    pp = dict()
    #sticky = hou.item('/obj/Skeleton_Geo1/Skeleton/Skeleton_Shader1/shopnet/__stickynote1') #HARDCODE
    for s in shop.children():
        if len(s.parms()) > 0:
            # print s.name()
            parms = [i for i in s.parms()]
            for p in parms:
                pp[p.path()] = p.eval()

    #sticky.setText(str(pp))
    # for i, p in pp.iteritems():
    #     print '%s :: %s' % (i, p)

    #newFolder =
    for k, v in pp.iteritems():
        p = hou.parm(k)
        old =  p.eval()
        file = os.path.split(old)[-1]

        new = '%s/%s' % (destFolder, file)
        p.set(new)

def bakeValues():
    obj = hou.node('/obj')
    l = [i for i in obj.allSubChildren() if i.type().name() == 'arnold::image']
    parms = dict()
    for i in l:
        #print i.name()
        p = i.parm('filename')
        if '`' in p.rawValue():
            exprVal = p.rawValue()
            path = exprVal[exprVal.find('"'):exprVal.rfind('"')+1]
            print type(path)
            print i.parm(path)
            #print i.parm(path).name()
            #print pp.path()
        else:
            parms[i.parm('filename').path()] = i.parm('filename').eval()

def getExprParms():
    obj = hou.node('/obj')
    l = [i for i in obj.allSubChildren() if i.type().name() == 'arnold::image']
    parms = dict()
    for i in l:
        #print i.name()
        p = i.parm('filename')
        if '`' in p.rawValue():
            exprVal = p.rawValue()
            path = exprVal[exprVal.find('"'):exprVal.rfind('"')+1]
            print type(path)
            print i.parm(path)
            #print i.parm(path).name()
            #print pp.path()
        else:
            parms[i.parm('filename').path()] = i.parm('filename').eval()
            
def bakeParms():
    shop = hou.node('/obj/char_skeleton/skeleton/shopnet_ACES')
    l = [i for i in shop.allSubChildren() if i.type().name() == 'arnold::image']
    for n in l:
        p = n.parm('filename')
        value = p.eval()
        #print p.path()
        #print '\t%s' % value
        p.revertToDefaults()
        p.set(value.replace('P:/Raid/assetBuilds/char/skeleton/main/tex/v005', '`chs("../../../../texture_folder_aces")`'))

def imageNodesSetup():
    shop = hou.node('/obj/char_skeleton/skeleton/shopnet_ACES')
    l = [i for i in shop.allSubChildren() if i.type().name() == 'arnold::image']
    for n in l:
        fn = n.parm('filename').eval()
        print n.parm('filename').path()
        print fn
        if '.png' in fn:
            n.parm('color_family').set('Utility')
            n.parm('color_space').set('Utility - sRGB - Texture')
            print '\tUtility - sRGB - Texture'
        elif '.tif' in fn:
            n.parm('color_family').set('Utility')
            n.parm('color_space').set('Utility - Raw')
            print '\tUtility - Raw'
        elif '.exr' in fn:
            n.parm('color_family').set('Utility')
            n.parm('color_space').set('Utility - Linear - sRGB')
            print '\tUtility - Linear - sRGB'
        else:
            print '\tA vot eto ya her znaet!'

def listImages():
    # if len(hou.selectedNodes())> 0:
    #     for n in hou.selectedNodes():
    #         subs = n.

    #shop = hou.node('/obj/char_skeleton/skeleton/shopnet_ACES')
    nodes = hou.selectedNodes()
    for no in nodes:
        print no.name()
        l = [i for i in no.allSubChildren() if i.type().name() == 'arnold::image']
        list = []
        for n in l:
            fn = n.parm('filename').eval()
            #print n.parm('filename').path()
            list.append(fn)
            #print ''

        # for i in set(list):
        #     print i

        s = no.createStickyNote()
        s.setText(str(list))