import os
try:
    node = hou.pwd()
    mp = node.parm('master_path').eval()
    if os.path.exists(mp):
        selectFile_res = hou.ui.selectFile(start_directory = mp, title = "Ukazhi put'")
    else:
        selectFile_res = hou.ui.selectFile(title="Ukazhi put'")

    if selectFile_res != '':
        bn = os.path.basename(selectFile_res)
        name = bn[:bn.find('.')]
        res = hou.ui.readInput("Kak nazovem mal'ca?", buttons=("Verno", "Ya uhozhu"), initial_contents = name)
        while res[0] == 0 and res[1] in [i.name() for i in node.parms()]:
            res = hou.ui.readInput("Eto imya uzhe sushestvuet. Pridumay chto-to unikalnot", buttons=("Pridumal!", "V pizdu"), initial_contents=name)
        if res[0] == 0:
            grp = node.parmTemplateGroup()
            f = grp.find('textures_folder')
            #if res[1]
            parm_name = res[1]
            ext = os.path.splitext(selectFile_res)[-1]

            if mp in selectFile_res:
                selectFile_res = selectFile_res.replace(mp, "`chs('master_path')`").replace('$F', '<UDIM>')
            p = hou.StringParmTemplate(name=parm_name, label=parm_name, num_components=1, default_value=(selectFile_res, ), string_type=hou.stringParmType.FileReference, tags={'ext': ext})
            grp.insertBefore(grp.find('textures_end'), p)
            node.setParmTemplateGroup(grp)

            # if mp in selectFile_res:
            #     #print 'replacing'
            #     selectFile_res = selectFile_res.replace(mp, "`chs('master_path')`").replace('$F', '<UDIM>')
            #     #print selectFile_res
            # node.parm(parm_name).set(selectFile_res)
except Exception as e: print(e)




# import os
# try:
#     node = hou.pwd()
#     mp = node.parm('master_path').eval()
#     if os.path.exists(mp):
#         selectFile_res = hou.ui.selectFile(start_directory = mp, title = "Ukazhi put'")
#     else:
#         selectFile_res = hou.ui.selectFile(title="Ukazhi put'")
#
#     if selectFile_res != '':
#         bn = os.path.basename(selectFile_res)
#         name = bn[:bn.find('.')]
#         res = hou.ui.readInput("Kak nazovem mal'ca?", buttons=("Verno", "Ya uhozhu"), initial_contents = name)
#         if res[0] == 0:
#             grp = node.parmTemplateGroup()
#             f = grp.find('textures_folder')
#             #if res[1]
#             parm_name = res[1]
#             ext = os.path.splitext(selectFile_res)[-1]
#
#
#             if mp in selectFile_res:
#                 selectFile_res = selectFile_res.replace(mp, "`chs('master_path')`").replace('$F', '<UDIM>')
#             p = hou.StringParmTemplate(name=parm_name, label=parm_name, num_components=1, default_value=(selectFile_res, ), string_type=hou.stringParmType.FileReference, tags={'ext': ext})
#             grp.insertBefore(grp.find('textures_end'), p)
#             node.setParmTemplateGroup(grp)
#
#             # if mp in selectFile_res:
#             #     #print 'replacing'
#             #     selectFile_res = selectFile_res.replace(mp, "`chs('master_path')`").replace('$F', '<UDIM>')
#             #     #print selectFile_res
#             # node.parm(parm_name).set(selectFile_res)
# except Exception as e: print(e)