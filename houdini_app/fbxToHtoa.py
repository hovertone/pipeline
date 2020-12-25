import hou
import os
from houdini_app.lokyScripts import lokyLayoutS

def getFilename(node):
    return os.path.split(node.evalParm('filename'))[-1]

def findAnotherTextures():
    netw = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    pwd = netw.pwd()
    ii = [i for i in pwd.allSubChildren() if i.type().name() == 'arnold::image']
    #ii = ii.sort(key=getFilename)
    texs = list()
    for i in sorted(ii, key=getFilename):
        print i.evalParm('filename'), i.parent().name()
        p = i.parent()
        p.setColor(hou.Color((0.616, 0.871, 0.769)))
        texs.append(i.evalParm('filename'))

    print texs

def renameShaders():
    nodes = hou.selectedNodes()
    for sn in nodes:
        ss = [i for i in sn.allSubChildren() if i.type().name() == 'arnold_vopnet']
        for s in ss:
            if 'scene_' in s.name():
                s.setName(s.name().replace('scene_', ''))

def replaceImagePaths():
    sn = hou.node('/obj/city')
    ii = [i for i in sn.allSubChildren() if i.type().name() == 'arnold::image']
    for i in ii:
        oldVal = i.evalParm('filename')
        newVal = oldVal.replace('P:/Fata/assetBuilds', '$ASSETBUILDS')
        i.parm('filename').set(newVal)

def createGroupRenames():
    node = hou.selectedNodes()[0]
    groups = [g.name() for g in node.geometry().primGroups()]
    pwd = node.parent()
    gr = pwd.createNode('grouprename')
    gr.setInput(0, node)
    gr.setPosition((node.position()[0], node.position()[1] - 1))
    gr.parm('renames').set(len(groups))
    for i, e in enumerate(groups):
        gr.parm('group%s' % str(i+1)).set(e)
        stripped_e = e.replace('scene_', '').replace('_group', '') + '_SG'
        gr.parm('newname%s' % str(i+1)).set(stripped_e)

def materialGroupRename():
    netw = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    pwd = netw.pwd()
    grs = [n for n in pwd.children() if n.type().name() == 'grouprename']
    mats = [n for n in pwd.children() if n.type().name() == 'material']
    d = dict()
    for g in grs:
        for i in range(1, g.evalParm('renames')+1):
            d[g.evalParm('group%s' % i)] = g.evalParm('newname%s' % i)

    for m in mats:
        for i in range(1, m.evalParm('num_materials')+1):
            group = m.evalParm('group%s' % i)
            if group in d.keys():
                m.parm('group%s' % i).set(d[group])
                print '%s :: %s replaced with %s' % (m.name(), group, d[group])

def fixDuplicateMaterials(node):
    if node.type().name() != 'material':
        hou.ui.displayMessage('Selet material node')
        return
    else:
        con = node.parent()
        print con.path()

def fixShopDuplicates(node):
    if node.type().name() != 'arnold_vopnet':
        hou.ui.displayMessage('Selet material node')
        return
    else:
        parent = node.parent()
        geo = parent.parent()
        parent_i = [i for i in node.children() if i.type().name() == 'arnold::image'][0]
        for n in parent.children():
            print n.name()
            try:
                i = [i for i in n.children() if i.type().name() == 'arnold::image'][0]
            except IndexError:
                continue
            if parent_i.evalParm('filename') == i.evalParm('filename'):
                print '%s and %s are similar' % (node.name(), n.name())
                for mat in [m for m in geo.children() if m.type().name() == 'material']:
                    for a in range(1, mat.evalParm('num_materials')+1):
                        if n.name() in mat.evalParm('shop_materialpath%s' % str(a)):
                            oldVal = mat.evalParm('shop_materialpath%s' % str(a))
                            newVal = oldVal.replace(n.name(), node.name())
                            mat.parm('shop_materialpath%s' % str(a)).set(newVal)



def collectShadingData(mats=None):
    if not mats:
        mat_net = hou.node('/obj/city_main_v001_fbx2/materials')
        mats = mat_net.children()
    m_list = list()
    c_max = 1000
    c = 0
    for m in mats:
        if c < c_max:
            # print m.name()
            # print '\tbasecolor: %s, %s, %s' % (m.parm('basecolorr').eval(), m.parm('basecolorg').eval(), m.parm('basecolorb').eval())
            # print '\tbasecolor map: %s' % m.parm('basecolor_texture').eval()
            # print '\troughness: %s' % m.parm('rough').eval()
            # print '\tIOR: %s' % m.parm('ior').eval()
            # print '\tmetallic: %s' % m.parm('metallic').eval()
            # print '\treflectivity: %s' % m.parm('reflect').eval()
            # print '\ttransparency: %s' % m.parm('transparency').eval()

            d = dict()
            d['name'] = m.name()
            d['node'] = m.path()
            d['base_color'] = [m.parm('basecolorr').eval(), m.parm('basecolorg').eval(), m.parm('basecolorb').eval()]
            if m.parm('basecolor_useTexture').eval() == 1:
                d['base_color_tex'] = m.parm('basecolor_texture').eval()
            else:
                d['base_color_tex'] = ''

            d['roughness'] = m.parm('rough').eval()

            m_list.append(d)

            c += 1
        else:
            break

    return m_list

def copyShading():
    mat_net = hou.node('/obj/city_main_v001_fbx2/materials')
    mats = mat_net.children()
    mat_names = [''.join([j for j in i.name() if not j.isdigit()]) for i in mats]
    for m in sorted(set(mat_names)):
        print m

def findShaderMatch(sh, sh_list):
    #for s in sh_list:
    pass

def collectGeoData():
    fbx_sub = hou.node('/obj/city_main_v001_fbx2')
    #geos = [i for i in fbx_sub.children() if (i.type().name() == 'geo') and (len(i.children()) != 0)]
    geos = hou.selectedNodes()
    if len(geos) == 0:
        hou.ui.displayMessage('No nodes selected')
        return
    l = list()
    #geos = (hou.node('/obj/city_main_v001_fbx2/scene_sidewalk02'), hou.node('/obj/city_main_v001_fbx2/scene_road_B01'))
    for g in geos:
        print g.name()
        obj = dict()
        shading = list()
        name = g.name()
        obj['name'] = name
        upper_lvl_assign = g.parm('shop_materialpath').eval() != ''
        #print '%s : upper LVL assign %s' % (g.name(), g.parm('shop_materialpath').eval() != '')
        if upper_lvl_assign:
            if len(g.children()) == 1:
                geo_output = g.children()[0].path()
            else:
                print 'THERE IS MORE THAN 1 NODES INSIDE %s' % name
            shading.append({'whole':g.parm('shop_materialpath').eval()})
        else:
            geo_output = [i for i in g.children() if i.type().name() == 'partition'][0].path()
            mat = [i for i in g.children() if i.type().name() == 'material'][0]
            num_mat = mat.parm('num_materials').eval()
            for j in range(1, num_mat+1):
                shading.append({mat.parm('group%s' % int(j)).eval():mat.parm('shop_materialpath%s' % int(j)).eval()})

        obj['shading'] = shading
        obj['geo'] = geo_output

        l.append(obj)

    return l

def createNodes(geo_list, mats_list, in_one_group=False):
    subnet = hou.node('/obj/converted')
    matnet = hou.node('/obj/converted/shopnet')
    ptg_preset = hou.node('/obj/converted/def_parmTemplate/shopnet1/preset')
    ptg = ptg_preset.parmTemplateGroup()

    if in_one_group:
        # SINGLE GROUP CREATION
        name_input_read = hou.ui.readInput('Type name for a group:', buttons=("OK", "CANCEL"))
        if name_input_read[0] == 1: # ON USER CANCEL
            print 'got to exit'
            pass
            #raise Exception('Canceled')
        else:
            geo = subnet.createNode('geo')
            print 'aaa ' + name_input_read[1]
            geo.setName(name_input_read[1])

            # MATS CREATION
            matnet = geo.createNode('shopnet')
            for m in mats_list:

                ar = matnet.createNode('arnold_vopnet')
                print 'NAME %s. Type %s' % (m['name'], type(m['name']))
                ar.setName(m['name'], unique_name = True)
                ar.moveToGoodPosition()

                out = [i for i in ar.children() if i.name() == 'OUT_material'][0]
                ss = ar.createNode('arnold::standard_surface')
                out.setInput(0, ss)

                ss.parm('base_colorr').set(m['base_color'][0])
                ss.parm('base_colorg').set(m['base_color'][1])
                ss.parm('base_colorb').set(m['base_color'][2])
                ss.parm('specular').set(0)
                ss.parm('specular_roughness').set(m['roughness'])

                if m['base_color_tex'] != '':
                    i = ar.createNode('arnold::image')
                    i.parm('filename').set(m['base_color_tex'])
                    i.setName("DIFFUSE")
                    ss.setInput(1, i)

                ar.layoutChildren()

                # PARM TEMPLATE GROUP SHIT
                ar.setParmTemplateGroup(ptg)
                ar.parm('ogl_numtex').set(1)
                ar.parm('ogl_tex1').set('`chs("%s/filename")`' % i.name())

            # GEO STUFF
            mats_to_merge = list()
            for g in geo_list:
                om = geo.createNode('object_merge')
                om.parm('objpath1').set(g['geo'])
                om.parm('xformtype').set(1)

                m = geo.createNode('material')
                mats_to_merge.append(m)
                m.setInput(0, om)
                m.moveToGoodPosition()
                m.parm('num_materials').set(len(g['shading']))

                for i, s in enumerate(g['shading']):
                    for k, v in s.iteritems():
                        group = k
                        if group == 'whole':
                            group = '*'
                        shader = v.split('/')[-1]
                        absolute_path = '%s/%s' % (matnet.path(), shader)
                        #print 'checkt geo %s : %s' % (geo.path(), absolute_path)
                        if geo.path() in absolute_path:
                            relative_path = absolute_path.replace(geo.path(), '..')
                            #print 'making rel path %s' % relative_path
                        else:
                            print 'no relative path match'
                            relative_path = absolute_path

                        m.parm('group%s' % (i + 1)).set(group)
                        m.parm('shop_materialpath%s' % (i + 1)).set(relative_path)

            #MERGE
            merge = geo.createNode('merge')
            for i, m in enumerate(mats_to_merge):
                merge.setInput(i, m)


            #NULL
            null = geo.createNode('null')
            null.setName('OUT')
            type_color = hou.Color((0.475, 0.812, 0.204))
            null.setColor(type_color)
            null.setInput(0, merge)
            null.setDisplayFlag(True)
            null.setRenderFlag(True)

            geo.layoutChildren()



    else:
        # ALL IN SEPARATED GROUPS CREATION
        # SHADERS GENERATION
        print mats_list
        for m in mats_list:
            ar = matnet.createNode('arnold_vopnet')
            print 'NAME %s' % m['name']
            ar.setName(m['name'])
            ar.moveToGoodPosition()

            out = [i for i in ar.children() if i.name() == 'OUT_material'][0]
            ss = ar.createNode('arnold::standard_surface')
            out.setInput(0, ss)

            ss.parm('base_colorr').set(m['base_color'][0])
            ss.parm('base_colorg').set(m['base_color'][1])
            ss.parm('base_colorb').set(m['base_color'][2])
            ss.parm('specular').set(0)
            ss.parm('specular_roughness').set(m['roughness'])

            if m['base_color_tex'] != '':
                i = ar.createNode('arnold::image')
                i.parm('filename').set(m['base_color_tex'])
                ss.setInput(1, i)

            ar.layoutChildren()

        # GEO GENERATION
        for g in geo_list:
            geo = subnet.createNode('geo')
            geo.setName(g['name'])
            geo.moveToGoodPosition()
            om = geo.createNode('object_merge')
            om.parm('objpath1').set(g['geo'])
            om.parm('xformtype').set(1)
            m = geo.createNode('material')
            m.setInput(0, om)
            m.moveToGoodPosition()
            m.parm('num_materials').set(len(g['shading']))
            for i, s in enumerate(g['shading']):
                for k, v in s.iteritems():
                    group = k
                    if group == 'whole':
                        group = '*'
                    shader = v.split('/')[-1]
                    m.parm('group%s' % (i+1)).set(group)
                    m.parm('shop_materialpath%s' % (i+1)).set('%s/%s' % (matnet.path(), shader))

            m.setDisplayFlag(True)
            m.setRenderFlag(True)






def main():
    #data = collectGeoData()
    #copyShading()
    #try:
    geo_data = collectGeoData()
    shade_nodes = list()
    for g in geo_data:
        for s in g['shading']:
            for k in s.keys():
                shade_nodes.append(hou.node(s[k]))

    shading_data = collectShadingData(shade_nodes)

    print shading_data
    createNodes(geo_data, shading_data, in_one_group=True)
    #except Exception as e: print(e)




