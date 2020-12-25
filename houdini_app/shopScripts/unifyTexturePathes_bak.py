# coding: utf-8
import hou
import os
import json

print '\n\n\n==================== in unifyTexturePaths ===================='


def createEmptyTp(parent_shop):
    print 'CREATING TP NODE'

    tp = parent_shop.createNode('arnold_vopnet')
    tp.setName('tp')
    tp.setColor(hou.Color(0.98, 0.275, 0.275))

    # PARAMETERS
    grp = tp.parmTemplateGroup()

    # MASTERPATH AND VERSION
    masterpathP = hou.StringParmTemplate('master_path', 'Master Path', 1, string_type=hou.stringParmType.FileReference)
    verP = hou.IntParmTemplate('version', 'Version', num_components=1)
    grp.addParmTemplate(masterpathP)
    grp.addParmTemplate(verP)

    # BUTTONS SECTION
    PATH_TO_SHOPSCRIPTS = 'X:/app/win/Pipeline/houdini_app/shopScripts'
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
    imagesToAcescgP = hou.ButtonParmTemplate("images_to_acescg", "Images to acescg", join_with_next=True,
                                                 help=u'Интерпретировать все текстуры как ACES CG',
                                                 script_callback='execfile("%s/imagesToAcescg.py")' % PATH_TO_SHOPSCRIPTS,
                                                 script_callback_language=hou.scriptLanguage.Python)  # , tags={'sourceExt':True})
    grp.append(imagesToAcescgP)
    bakePathsP = hou.ButtonParmTemplate("bake_paths", "Bake Paths", join_with_next=False,
                                        help=u'Запекает все ссылки текстур и шейдеров в Image нодах. Удобно если нужно удалить эту tp ноду.',
                                        script_callback='execfile("%s/bakePaths.py")' % PATH_TO_SHOPSCRIPTS,
                                        script_callback_language=hou.scriptLanguage.Python)
    grp.append(bakePathsP)

    # TEXTURES
    folderP = hou.FolderParmTemplate('textures_folder', 'Textures', folder_type=hou.folderType.Simple)
    createParmP = hou.ButtonParmTemplate("create_parm", "+", join_with_next=True, script_callback='execfile("%s/createParm.py")' % PATH_TO_SHOPSCRIPTS, script_callback_language=hou.scriptLanguage.Python)
    folderP.addParmTemplate(createParmP)
    removeParmsP = hou.ButtonParmTemplate("remove_parms", "Remove Texture paths", join_with_next=False, script_callback='execfile("%s/removeTextureParms.py")' % PATH_TO_SHOPSCRIPTS, script_callback_language=hou.scriptLanguage.Python)
    folderP.addParmTemplate(removeParmsP )
    folderP.addParmTemplate(hou.SeparatorParmTemplate(name='textures_end', is_hidden=True))
    grp.addParmTemplate(folderP)
    tp.setParmTemplateGroup(grp)

    return tp


def collectParms(nodes):
    # nodes = hou.selectedNodes()
    # DEV
    # nodes = (hou.node('/obj/orcWarriorShading/shopnet_ACES1/Ork_Warior_Metal'), hou.node('/obj/orcWarriorShading/shopnet_ACES1/Ork_Warior_Axe_Metal'), hou.node('/obj/orcWarriorShading/shopnet_ACES1/Ork_Warior_Cloth'), hou.node('/obj/orcWarriorShading/shopnet_ACES1/Ork_Gum'), hou.node('/obj/orcWarriorShading/shopnet_ACES1/Ork_Teeth'), hou.node('/obj/orcWarriorShading/shopnet_ACES1/Ork_warior_Skin'), hou.node('/obj/orcWarriorShading/shopnet_ACES1/Ork_Warior_Leather'), hou.node('/obj/orcWarriorShading/shopnet_ACES1/Ork_Warior_Bone'), hou.node('/obj/orcWarriorShading/shopnet_ACES1/Ork_Eye_glass'), hou.node('/obj/orcWarriorShading/shopnet_ACES1/Ork_Warior_Axe_Leather'), hou.node('/obj/orcWarriorShading/shopnet_ACES1/Ork_Eye'))

    shaders_images = dict()
    for n in nodes:
        # print n.name()
        if n.type().name() != 'arnold_vopnet':
            print 'ERROR :: wrong type nodes selected %s' % (n.path())
            return

        shaders_images[n] = dict()
        # images = [i for i in n.allSubChildren() if i.type().name() == 'arnold::image']
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
    print '\t\t\t\tFILL EXISTING TP'
    shaders_images = collectParms(nodes)
    # for k, v in ii.iteritems():
    #     print '%s %s' % (k, v)

    # GETTING ALL THE FILE PATHS AND ASSIGN TO VALUES VAR
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
    # for k, v in ii.iteritems():
    #     print '%s %s' % (k, v)

    # GETTING ALL THE FILE PATHS AND ASSIGN TO VALUES VAR
    ii = dict()
    for s, vv in shaders_images.iteritems():
        ii.update(vv)

    values = ii.values()
    val_set = sorted(list(set(values)))
    tex_amount = len(val_set)

    # LOOK FOR SUBSTRING
    numberOfDigitsToMatch = 30
    sub_found = False
    for i, e in enumerate(val_set[0]):
        for tex_path in val_set:
            # print tex_path
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

    # PRINT VAL SET
    print 'VALSET'
    for k in val_set:
        print k
    print 'VALSET END'

    # return # EXIT

    # parms_vals = dict()
    for t in val_set:
        # for i in range(tex_amount):
        grp = tp.parmTemplateGroup()
        folderP = grp.find('textures_folder')

        #if not grp.find(s.name()): grp.insertBefore(grp.find('textures_end'), hou.LabelParmTemplate(s.name(), s.name()))

        ext = os.path.splitext(t)[-1]
        file = os.path.split(t)[-1]
        # parm_name = 'tex%s' % str(i+1).zfill(3)
        parm_name = file[:file.find('.')].lower().replace('_<udim>', '').replace('.<udim>', '')

        # DIGITS TO END OF PARM NAME
        parm_digit = 1
        print 'find is %s' % str(grp.find('%s_%s' % (parm_name, str(parm_digit).zfill(2))))
        while grp.find('%s_%s' % (parm_name, str(parm_digit).zfill(2))):
            parm_digit += 1

        # print t
        parm_name = '%s_%s' % (parm_name, str(parm_digit).zfill(2))
        parm_name = parm_name.replace('-', '_')
        # print parm_name

        # HARDCODE EXCEPTIONS
        if parm_name[0] == '8': parm_name = 'EightK_Noise'
        if parm_name[0] == '1': parm_name = 'colormask_01'
        #if parm_name == 'teethMask - tm': parm_name = 'teethMask'
        #if parm_name == 'teeth1 - tm': parm_name = 'teeth1'
        #teeth1_tm_01

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
        parmsLinked = [key.path()  for (key, value) in ii.items() if value == t]
        texP = hou.StringParmTemplate(name=parm_name, label=parm_name, num_components=1, default_value=(actual_t,),
                                      string_type=hou.stringParmType.FileReference,
                                      tags={'ext': ext, 'node': str(parmsLinked)})
        print 'adding %s' % parm_name
        # folderP.addParmTemplate(texP)
        grp.insertBefore(grp.find('textures_end'), texP)

        listOfKeys = [key for key, value in ii.iteritems() if value == t] #
        for k in listOfKeys:
            k.set('`chs("../../%s/%s")`' % (tp.name(), parm_name))

        try:
            tp.setParmTemplateGroup(grp)
        except Exception as e:
            print e


    # if not simpleTP:
    #     if sub_found: tp.parm('master_path').set(substring)

def main():
    print '\t\t\t\tMAIN'
    nodes = hou.selectedNodes()

    if len(nodes) == 0:
        hou.ui.displayMessage('Select shader(s) or shop node')
        return
    elif nodes[0].type().name() == 'arnold_vopnet':
        parent = nodes[0].parent()
        tp_list = [c for c in parent.children() if c.name() == 'tp']
        if tp_list == []:
            print 'dont have a TP'
            tp = createEmptyTp(parent)
        else:
            tp = tp_list[0]

        #fillExistingTp(tp, nodes) #per shader
        fillExistingTpSet(tp, nodes)
        return
    elif nodes[0].type().name() == 'shopnet':
        createEmptyTp(nodes[0])
        return
    else:
        hou.ui.displayMessage('Something goes wrong! Sorry! Have a nice evening)')
        return

    #
    # ii, shaderName = collectParms(nodes)
    # # for k, v in ii.iteritems():
    # #     print '%s %s' % (k, v)
    #
    # values = ii.values()
    # val_set = sorted(list(set(values)))
    # tex_amount = len(val_set)
    #
    # #PRINT VAL SET
    # print 'VALSET'
    # for k in val_set:
    #     print k
    # # print val_set
    # print 'VALSET END'
    #
    # #return # EXIT
    #
    # #LOOK FOR SUBSTRING
    # numberOfDigitsToMatch = 30
    # sub_found = False
    # for i, e in enumerate(val_set[1]):
    #     for tex_path in val_set:
    #         print tex_path
    #         if tex_path[i] != e:
    #             sub_found = True
    #             print 'Strings are not matching from %s digit' % i
    #             break
    #     #print 'done %s' % e
    #     if sub_found: break
    #
    # if sub_found and i > numberOfDigitsToMatch:
    #     substring = val_set[3][:i]
    # else:
    #     sub_found = False
    #     print 'texture paths dont match'
    #
    #
    # # ============================================================
    # # ACQUIRING A TP NODE
    # if hou.node('%s/tp' % shoppath):
    #     #
    #     #hou.ui.displayMessage('tp node is already exists. Delete %s first.' % '%s/tp' % shoppath)
    #     print 'FOUND TP NODE'
    #     tp = hou.node('%s/tp' % shoppath)
    # else:
    #     print 'CREATING TP NODE'
    #     #node = hou.node('/obj/DarkElve_Shading/geometry/Darkelf_Shader1/shopnet1/dark_elf_leather')#HARDCODE
    #     #p = node.path()
    #     #split = p.split('/')
    #     #shopPath = '/'.join(split[:-1])
    #     shop = hou.node(shoppath)
    #     tp = shop.createNode('arnold_vopnet')
    #     tp.setName('tp')
    #     tp.setColor(hou.Color(0.98, 0.275, 0.275))
    #
    #     # PARAMETERS
    #     grp = tp.parmTemplateGroup()
    #
    #     # MASTERPATH AND VERSION
    #     masterpathP = hou.StringParmTemplate('master_path', 'Master Path', 1, string_type=hou.stringParmType.FileReference)
    #     verP = hou.IntParmTemplate('version', 'Version', num_components=1)
    #     grp.addParmTemplate(masterpathP)
    #     grp.addParmTemplate(verP)
    #
    #     # BUTTONS SECTION
    #     PATH_TO_SHOPSCRIPTS = 'X:/app/win/Pipeline/houdini_app/shopScripts'
    #     createEmptyShaderP = hou.ButtonParmTemplate("create_images", "Create Empty Shader", join_with_next=True, help=u'Создает Image ноды с путями к каждый текстуре внутри tp ноды', script_callback='execfile("%s/createEmptyShader.py")' % PATH_TO_SHOPSCRIPTS, script_callback_language=hou.scriptLanguage.Python)
    #     grp.append(createEmptyShaderP)
    #     listImagesP = hou.ButtonParmTemplate("list_images", "List all texture paths", join_with_next=True, help=u'В Python Shell выкидывает список текстур, использованных в каждом шейдере этого шопа', script_callback='execfile("%s/listImages.py")' % PATH_TO_SHOPSCRIPTS, script_callback_language=hou.scriptLanguage.Python)
    #     grp.append(listImagesP)
    #     switchExtensionsP = hou.ButtonParmTemplate("switch_extensions", "TX", join_with_next=True, help=u'Заменяет расширение файлов на .tx и обратно', script_callback='execfile("%s/switchExtensionEXR.py")' % PATH_TO_SHOPSCRIPTS, script_callback_language=hou.scriptLanguage.Python) #, tags={'sourceExt':True})
    #     grp.append(switchExtensionsP)
    #     bakePathsP = hou.ButtonParmTemplate("bake_paths", "Bake Paths", join_with_next=False, help=u'Запекает все ссылки текстур и шейдеров в Image нодах. Удобно если нужно удалить эту tp ноду.', script_callback='execfile("%s/bakePaths.py")' % PATH_TO_SHOPSCRIPTS, script_callback_language=hou.scriptLanguage.Python)
    #     grp.append(bakePathsP)
    #
    #     # TEXTURES
    #     folderP = hou.FolderParmTemplate('textures_folder', 'Textures', folder_type=hou.folderType.Simple)
    #     #createParmP = hou.ButtonParmTemplate("create_parm", "+", join_with_next=False, script_callback='execfile("%s/createParm.py")' % PATH_TO_SHOPSCRIPTS, script_callback_language=hou.scriptLanguage.Python)
    #     #folderP.addParmTemplate(createParmP)
    #     folderP.addParmTemplate(hou.SeparatorParmTemplate(name='textures_end', is_hidden=True))
    #     grp.addParmTemplate(folderP)
    #     tp.setParmTemplateGroup(grp)
    #
    #
    #
    # parms_vals = dict()
    # if not simpleTP:
    #     for i in range(tex_amount):
    #         grp = tp.parmTemplateGroup()
    #         folderP = grp.find('textures_folder')
    #
    #         if not grp.find(shaderName): grp.insertBefore(grp.find('textures_end'), hou.LabelParmTemplate(shaderName, shaderName))
    #
    #
    #         t = val_set[i]
    #         ext = os.path.splitext(t)[-1]
    #         file = os.path.split(t)[-1]
    #         #parm_name = 'tex%s' % str(i+1).zfill(3)
    #         parm_name = file[:file.find('.')].lower().replace('<udim>', '')
    #
    #         if parm_name[0] == '8': parm_name = 'EightK_Noise'
    #
    #         parm_digit = 1
    #         while grp.find('%s_%s' % (parm_name, str(parm_digit).zfill(2))):
    #             parm_digit += 1
    #
    #         parm_name = '%s_%s' % (parm_name, str(parm_digit).zfill(2))
    #         print t
    #         print file
    #         print parm_name
    #
    #         #parms_vals[parm_name] = t
    #
    # # for k, v in parms_vals.iteritems():
    # #     print k, v
    #
    #         if sub_found:
    #             actual_t = t.replace(substring, '`chs("master_path")`')
    #         else:
    #             actual_t = t
    #
    #         texP = hou.StringParmTemplate(name=parm_name, label=parm_name, num_components=1, default_value=(actual_t, ), string_type=hou.stringParmType.FileReference, tags={'ext':ext})
    #         #folderP.addParmTemplate(texP)
    #         grp.insertBefore(grp.find('textures_end'), texP)
    #
    #         # listOfKeys = [key for key, value in ii.iteritems() if value == t] #
    #         # for k in listOfKeys:
    #         #     k.set('`chs("../../%s/%s")`' % (tp.name(), parm_name))
    #
    #         #grp.append(folderP)
    #         tp.setParmTemplateGroup(grp)
    #
    #
    # # if not simpleTP:
    # #     if sub_found: tp.parm('master_path').set(substring)



