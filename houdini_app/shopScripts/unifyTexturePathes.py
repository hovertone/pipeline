# coding: utf-8
import hou
import os
import json

#print '\n\n\n==================== in unifyTexturePaths ===================='

def createEmptyTp(parent_shop):
    print 'CREATING TP NODE'

    PATH_TO_SHOPSCRIPTS = 'X:/app/win/Pipeline/houdini_app/shopScripts'
    print 'AUTO PATH', os.path.abspath(os.getcwd())

    if parent_shop.type().name() == 'shopnet':
        tp = parent_shop.createNode('arnold_vopnet')
    elif parent_shop.type().name() == 'matnet':
        tp = parent_shop.createNode('arnold_materialbuilder')

    tp.setName('tp')
    tp.setColor(hou.Color(0.98, 0.275, 0.275))

    # PARAMETERS
    grp = tp.parmTemplateGroup()

    # MASTERPATH
    masterpathP = hou.StringParmTemplate('master_path', 'Master Path', 1, join_with_next=True, string_type=hou.stringParmType.FileReference, file_type=hou.fileType.Directory)
    grp.addParmTemplate(masterpathP)

    # FIND MASTER PATH BUTTON
    # findMasterSubstringP = hou.ButtonParmTemplate("find_master_substring", "Fill Masterpath", join_with_next=False,
    #                                      help=u'В Python Shell выкидывает список текстур, использованных в каждом шейдере этого шопа',
    #                                      script_callback='execfile("%s/fillMasterpath.py")' % PATH_TO_SHOPSCRIPTS,
    #                                      script_callback_language=hou.scriptLanguage.Python)
    # grp.addParmTemplate(findMasterSubstringP)

    # LINK TEXTURES FOR MASTER PATH STRING
    linkMasterpathP = hou.ButtonParmTemplate("link_master_substring", "Link", join_with_next=False,
                                         help=u'Находит мастерпасс строку в путях к текстурам и заменяет путь папки на ссылку к мастерпасу',
                                         script_callback='execfile("%s/linkMasterpath.py")' % PATH_TO_SHOPSCRIPTS,
                                         script_callback_language=hou.scriptLanguage.Python)
    grp.addParmTemplate(linkMasterpathP)

    # VERSION
    verP = hou.IntParmTemplate('version', 'Version', num_components=1)
    grp.addParmTemplate(verP)

    # BUTTONS SECTION
    createEmptyShaderP = hou.ButtonParmTemplate("create_images", "Create Empty Shader", join_with_next=True,
                                                help=u'Создает Image ноды с путями к каждый текстуре внутри tp ноды',
                                                script_callback='execfile("%s/createEmptyShader.py")' % PATH_TO_SHOPSCRIPTS,
                                                script_callback_language=hou.scriptLanguage.Python)
    grp.append(createEmptyShaderP)
    listImagesP = hou.ButtonParmTemplate("list_images", "List all texture paths", join_with_next=True,
                                         help=u'В Python Shell выкидывает список текстур, использованных в каждом шейдере этого шопа',
                                         script_callback='execfile("%s/listImages.py")' % PATH_TO_SHOPSCRIPTS,
                                         script_callback_language=hou.scriptLanguage.Python)
    grp.append(listImagesP)
    switchExtensionsEXRP = hou.ButtonParmTemplate("switch_extensions_exr", "EXR", join_with_next=True,
                                               help=u'Заменяет расширение файлов на .exr и обратно',
                                               script_callback='execfile("%s/switchExtensionEXR.py")' % PATH_TO_SHOPSCRIPTS,
                                               script_callback_language=hou.scriptLanguage.Python)  # , tags={'sourceExt':True})
    grp.append(switchExtensionsEXRP)
    switchExtensionsTXP = hou.ButtonParmTemplate("switch_extensions_tx", "TX", join_with_next=True,
                                               help=u'Заменяет расширение файлов на .tx и обратно',
                                               script_callback='execfile("%s/switchExtensionTX.py")' % PATH_TO_SHOPSCRIPTS,
                                               script_callback_language=hou.scriptLanguage.Python)  # , tags={'sourceExt':True})
    grp.append(switchExtensionsTXP)
    imagesToAcescgP = hou.ButtonParmTemplate("images_to_acescg", "Images to acescg", join_with_next=False,
                                                 help=u'Интерпретировать все текстуры как ACES CG',
                                                 script_callback='execfile("%s/imagesToAcescg.py")' % PATH_TO_SHOPSCRIPTS,
                                                 script_callback_language=hou.scriptLanguage.Python)  # , tags={'sourceExt':True})
    grp.append(imagesToAcescgP)
    bakePathsP = hou.ButtonParmTemplate("bake_paths", "Bake Paths", join_with_next=True,
                                        help=u'Запекает все ссылки текстур и шейдеров в Image нодах. Удобно если нужно удалить эту tp ноду.',
                                        script_callback='execfile("%s/bakePaths.py")' % PATH_TO_SHOPSCRIPTS,
                                        script_callback_language=hou.scriptLanguage.Python)
    grp.append(bakePathsP)
    findReplaceP = hou.ButtonParmTemplate("find_replace", "Find & Replace", join_with_next=True,
                                        help=u'Подмена значений в путях на текстуры',
                                        script_callback='execfile("%s/findAndReplace.py")' % PATH_TO_SHOPSCRIPTS,
                                        script_callback_language=hou.scriptLanguage.Python)
    grp.append(findReplaceP)
    toacescgP = hou.ButtonParmTemplate("convert_to_acescg", "To ACEScg", join_with_next=True,
                                          help=u'Подмена значений в путях на текстуры',
                                          script_callback='execfile("%s/convertToAcescg.py")' % PATH_TO_SHOPSCRIPTS,
                                          script_callback_language=hou.scriptLanguage.Python)
    grp.append(toacescgP)
    toacescgP = hou.ButtonParmTemplate("copyTex", "Copy Textures", join_with_next=False,
                                       help=u'Копирование файлов',
                                       script_callback='execfile("%s/pathsSelect.py")' % PATH_TO_SHOPSCRIPTS,
                                       script_callback_language=hou.scriptLanguage.Python)
    grp.append(toacescgP)

    # TEXTURES
    folderP = hou.FolderParmTemplate('textures_folder', 'Textures', folder_type=hou.folderType.Simple)
    createParmP = hou.ButtonParmTemplate("create_parm", "+", join_with_next=True, script_callback='execfile("%s/createParm.py")' % PATH_TO_SHOPSCRIPTS, script_callback_language=hou.scriptLanguage.Python)
    folderP.addParmTemplate(createParmP)
    removeParmP = hou.ButtonParmTemplate("remove_parm", "-", join_with_next=True, script_callback='execfile("%s/removeParm.py")' % PATH_TO_SHOPSCRIPTS, script_callback_language=hou.scriptLanguage.Python)
    folderP.addParmTemplate(removeParmP)
    removeParmsP = hou.ButtonParmTemplate("remove_parms", "Remove all texture paths", join_with_next=False, script_callback='execfile("%s/removeTextureParms.py")' % PATH_TO_SHOPSCRIPTS, script_callback_language=hou.scriptLanguage.Python)
    folderP.addParmTemplate(removeParmsP)
    folderP.addParmTemplate(hou.SeparatorParmTemplate(name='textures_end', is_hidden=True))
    grp.addParmTemplate(folderP)

    paramsToKeepListP = hou.StringParmTemplate(name='parms_to_keep', label='Parms to Keep', num_components=1, default_value=("create_parm remove_parm remove_parms textures_end", ), is_hidden=True)
    grp.append(paramsToKeepListP)

    tp.setParmTemplateGroup(grp)

    print "Empty %s node created" % tp.name()
    return tp


def collectParms(nodes):
    shaders_images = dict()
    for n in nodes:
        if n.type().name() != 'arnold_vopnet' and n.type().name() != 'arnold_materialbuilder':
            print 'ERROR :: wrong type nodes selected %s' % (n.path())
            return

        shaders_images[n] = dict()
        for i in [j for j in n.children() if j.type().name() == 'arnold::image']:
            p = i.parm('filename')
            # print '\t%s link %s' % (i.name(), i.parm('filename').eval() == i.parm('filename').rawValue())
            if p.eval() != p.rawValue():  # whick means filename parameter has a link
                # LINKED PARMS BAKING
                val = p.eval()
                p.revertToDefaults()
                p.set(val)
                print "\t%s's filename parameter has been baked" % i.name()

            shaders_images[n][p] = p.rawValue()

    return shaders_images

def fillExistingTp(tp, nodes):
    '''
    Creates per shader parameters. Not uniqes. Repeated paths would be duplicated. Only for debug usage

    :param tp:
    :param nodes:
    :return:
    '''
    print '\t\t\t\tFILL EXISTING TP'
    shaders_images = collectParms(nodes)

    values = []
    toNuke = dict()
    for s, vv in shaders_images.iteritems():
        #print s.name()
        tex_paths = []
        for p, v in vv.iteritems():
            #print '\t%s :: %s' % (p.node().name(), v)
            values.append(v)
            tex_paths.append(v)

        toNuke[s.name()] = tex_paths

    #values = ii.values()
    val_set = sorted(list(set(values)))
    tex_amount = len(val_set)

    # LOOK FOR SUBSTRING
    numberOfDigitsToMatch = 30
    sub_found = False
    for i, e in enumerate(val_set[0]):
        for tex_path in val_set:
            #print tex_path
            if tex_path[i] != e:
                sub_found = True
                print 'Strings are not matching from %s digit' % i
                break
        # print 'done %s' % e
        if sub_found: break

    if sub_found and i > numberOfDigitsToMatch:
        substring = val_set[0][:i]
        tp.parm('master_path').set(substring)
    else:
        sub_found = False
        print 'texture paths dont match'

    # JSON DUMP
    with open('%s/toNuke.txt' % substring, 'w') as outfile:
        json.dump(toNuke, outfile)

    # PRINT VAL SET
    # print 'VALSET'
    # for k in val_set:
    #     print k
    # print 'VALSET END'

    # return # EXIT

    #parms_vals = dict()
    for s, vv in shaders_images.iteritems():
        for p, v in vv.iteritems():
        #for i in range(tex_amount):
            grp = tp.parmTemplateGroup()
            folderP = grp.find('textures_folder')

            if not grp.find(s.name()): grp.insertBefore(grp.find('textures_end'),
                                                          hou.LabelParmTemplate(s.name(), s.name()))

            t = v
            ext = os.path.splitext(t)[-1]
            file = os.path.split(t)[-1]
            # parm_name = 'tex%s' % str(i+1).zfill(3)
            parm_name = file[:file.find('.')].lower().replace('_<udim>', '').replace('.<udim>', '')

            # DIGITS TO END OF PARM NAME
            parm_digit = 1
            print 'find is %s' % str(grp.find('%s_%s' % (parm_name, str(parm_digit).zfill(2))))
            while grp.find('%s_%s_%s' % (s.name(), parm_name, str(parm_digit).zfill(2))):
                parm_digit += 1

            #print t
            parm_name = '%s_%s_%s' % (s.name(), parm_name, str(parm_digit).zfill(2))
            parm_name = parm_name.replace('-', '_')
            #print parm_name

            # HARDCODE EXCEPTIONS
            if parm_name[0] == '8': parm_name = 'EightK_Noise'
            if parm_name[0] == '1': parm_name = 'colormask_01'
            # if parm_name == 'orc_dispork_sculpt1-dm_01': parm_name = 'orc_dm_01'
            # if parm_name == 'eyes3_1 - tm_01': parm_name = 'eyes3_tm_01'
            # if parm_name == 'teeth1 - tm_01' or parm_name == 'teeth1-tm_01': parm_name = 'teeth1_tm_01'
            # if parm_name == 'teethmask-tm_01': parm_name = 'teethmask_01'
            # if parm_name == 'colormask_01': parm_name = 'colosrmask_02'



            # REPLACING PATH WITH SUBSTRING
            if sub_found:
                actual_t = t.replace(substring, '`chs("master_path")`')
            else:
                actual_t = t

            # CREATING PARM
            texP = hou.StringParmTemplate(name=parm_name, label=parm_name, num_components=1, default_value=(actual_t,),
                                          string_type=hou.stringParmType.FileReference, tags={'ext': ext, 'node':str(p.path())})
            print 'adding %s' % parm_name
            # folderP.addParmTemplate(texP)
            grp.insertBefore(grp.find('textures_end'), texP)

            # listOfKeys = [key for key, value in ii.iteritems() if value == t] #
            # for k in listOfKeys:
            #     k.set('`chs("../../%s/%s")`' % (tp.name(), parm_name))

            # grp.append(folderP)
            tp.setParmTemplateGroup(grp)

    # if not simpleTP:
    #     if sub_found: tp.parm('master_path').set(substring)


def fillExistingTpSet(tp, nodes):
    print '\t\t\t\tFILL EXISTING TP'
    shaders_images = collectParms(nodes)
    print 'SHADERS IMAGE %s' % str(shaders_images)

    # for k, v in ii.iteritems():
    #     print '%s %s' % (k, v)

    # GETTING ALL THE FILE PATHS AND ASSIGN TO VALUES VAR
    ii = dict()
    for s, vv in shaders_images.iteritems():
        ii.update(vv)

    for key, value in ii.iteritems():
        print key
        print value
        print '\n'

    values = ii.values()
    val_set = sorted(list(set(values)))
    tex_amount = len(val_set)


    # PRINT VAL SET
    # print 'VALSET'
    # for k in val_set:
    #     print k
    # print 'VALSET END'

    for t in val_set:
        print t
        grp = tp.parmTemplateGroup()
        folderP = grp.find('textures_folder')

        parms_to_avoid = tp.parm('parms_to_keep').eval().split(' ')
        texture_parm_names = [p.name() for p in folderP.parmTemplates() if p.name() and p.name() not in parms_to_avoid]

        # CHECK IF WE NEED TO CREATE A NEW PARM OR LINK TO AN EXISTING ONE
        match = False
        for pn in texture_parm_names:
            if t == tp.parm(pn).eval():
                match = True
                break

        if not match:
            cs = [key.node().parm('color_space').eval() for (key, value) in ii.iteritems() if value == t][0]

            ext = os.path.splitext(t)[-1]
            file = os.path.split(t)[-1]
            parm_name = file[:file.find('.')].lower().replace('_<udim>', '').replace('.<udim>', '')

            # DIGITS TO END OF PARM NAME
            parm_digit = 1
            while grp.find('%s_%s' % (parm_name, str(parm_digit).zfill(2))):
                parm_digit += 1

            parm_name = '%s_%s' % (parm_name, str(parm_digit).zfill(2))
            parm_name = parm_name.replace('-', '_')
            parm_name = parm_name.replace(' ', '_')
            parm_name = parm_name.replace('xn__', '')

            # CREATING PARM
            parmsLinked = [key.path()  for (key, value) in ii.items() if value == t]
            texP = hou.StringParmTemplate(name=parm_name, label=parm_name, num_components=1, default_value=(t,),
                                          string_type=hou.stringParmType.FileReference, join_with_next=True,
                                          tags={'ext': ext, 'node': ' '.join(parmsLinked)})
            # ADDING PARM
            print 'adding %s' % parm_name
            grp.insertBefore(grp.find('textures_end'), texP)

            listOfKeys = [key for key, value in ii.iteritems() if value == t] #
            for k in listOfKeys:
                k.set('`chs("../../%s/%s")`' % (tp.name(), parm_name))

            # CREATING CS PARM
            #print 'T ' + t
            #print [key.eval() for (key, value) in ii.iteritems() if value == t]
            #cs = [key.eval() for (key, value) in ii.items() if value == t][0]
            csP = hou.StringParmTemplate(name='%s_cs' % parm_name, label='space', num_components=1,
                                         menu_items=('Utility - Raw', 'Utility - sRGB - Texture', 'Utility - Linear - sRGB'),
                                         menu_labels=('Raw', 'sRGB - Texture', 'Linear - sRGB'),
                                         default_value=(cs, ),
                                         string_type=hou.stringParmType.Regular, join_with_next=False)
            #pt = csP.parmTemplate()
            #csP.setMenuItems(('Utility - Raw', 'Utility - sRGB - Texture', 'Utility - Linear - sRGB'))
            grp.insertBefore(grp.find('textures_end'), csP)

        else:
            print 'exists %s' % pn
            listOfKeys = [key for key, value in ii.iteritems() if value == t]  #
            for k in listOfKeys:
                k.set('`chs("../../%s/%s")`' % (tp.name(), pn))

            tags = grp.find(pn).tags()
            nodes_tag = tags['node'].split(' ')

            nodes_to_append = [key.path() for key, value in ii.iteritems() if value == t]
            nodes_tag += nodes_to_append
            tags['node'] = ' '.join(nodes_tag)
            pt = grp.find(pn)
            pt.setTags(tags)
            grp.replace(pn, pt)

        try:
            tp.setParmTemplateGroup(grp)
        except Exception as e:
            print e

def main():
    print '\t\t\t\tMAIN'
    nodes = hou.selectedNodes()

    if len(nodes) == 0:
        # if no nodes were selected. The empty tp node should be created on a proper level if all conditions are met.
        if hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor, 0):
            pwd = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor, 0)
            netw_context = hou.node(pwd.pwd().path())
            print 'FOR TESTS: %s' % str(netw_context.type().name())
            if netw_context.type().name() == 'shopnet' or netw_context.type().name() == 'matnet':
                createEmptyTp(netw_context)
            else:
                hou.ui.displayMessage('Not shopnetw context. Select nodes or execute script in shopnetw context')
                return
        else:
            hou.ui.displayMessage('No Network View found')
            return
    elif nodes[0].type().name() == 'arnold_vopnet' or nodes[0].type().name() == 'arnold_materialbuilder':
        # if proper nodes selected. All subshildren image nodes filenames will be linked to tp
        parent = nodes[0].parent()
        tp_list = [c for c in parent.children() if c.name() == 'tp']
        if tp_list == []:
            tp = createEmptyTp(parent)
        else:
            tp = tp_list[0]
        fillExistingTpSet(tp, nodes)
        return

    elif nodes[0].type().name() != 'arnold_vopnet' or nodes[0].type().name() != 'arnold_materialbuilder':
        hou.ui.displayMessage('Only arnold vopnet nodes should be selected')
        return
    else:
        hou.ui.displayMessage('Something goes wrong! Sorry! Have a nice evening)')
        return

