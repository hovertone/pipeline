import os
# '=========== CREATE PARM ============='

node = hou.pwd()
mp = node.parm('master_path').eval()
if os.path.exists(mp):
    selectFile_res = hou.ui.selectFile(start_directory = mp, title = "Ukazhi put'", pattern = '*.exr', collapse_sequences = True, multiple_select = True)
else:
    selectFile_res = hou.ui.selectFile(title="Ukazhi put'", pattern = '*.exr', collapse_sequences = True, multiple_select = True)

seqs = [i.strip(' ').replace('$F', '<UDIM>') for i in selectFile_res.split(';')]

grp = node.parmTemplateGroup()
f = grp.find('textures_folder')
parms_to_avoid = node.parm('parms_to_keep').eval().split(' ')
existing_texture_names = [i.name() for i in f.parmTemplates() if i.name() not in parms_to_avoid]
exist_values = [node.parm(j).rawValue() for j in existing_texture_names]

if seqs[0] != '':
    for sq in seqs:
        print '%s' % sq
        if sq in exist_values:
            print '\talready exists'
        else:
            bn = os.path.basename(sq)
            name = bn[:bn.find('.')]

            print '\t creating %s' % name

            # DIGITS TO END OF PARM NAME
            parm_digit = 1
            while grp.find('%s_%s' % (name, str(parm_digit).zfill(2))):
                parm_digit += 1

            parm_name = '%s_%s' % (name, str(parm_digit).zfill(2))
            parm_name = parm_name.replace('-', '_')

            ext = os.path.splitext(sq)[-1]
            def_value = sq

            if mp != '' and mp in sq:
                def_value = def_value.replace(mp, "`chs('master_path')`")

            p = hou.StringParmTemplate(name=parm_name, label=parm_name, num_components=1, default_value=(def_value, ), join_with_next=True, string_type=hou.stringParmType.FileReference, tags={'ext': ext})
            grp.insertBefore(grp.find('textures_end'), p)

            # CREATING COLOR FAMILY PARM
            cfP = hou.StringParmTemplate(name='%s_cf' % parm_name, label='Family', num_components=1,
                                         menu_items=('ACES', 'Utility'),
                                         menu_labels=('ACES', 'Utility'),
                                         string_type=hou.stringParmType.Regular, join_with_next=True)

            # CREATING COLOR SPACE PARM
            csP = hou.StringParmTemplate(name='%s_cs' % parm_name, label='Space', num_components=1,
                                         menu_items=('Utility - Raw', 'Utility - sRGB - Texture', 'Utility - Linear - sRGB'),
                                         menu_labels=('Raw', 'sRGB - Texture', 'Linear - sRGB'),
                                         string_type=hou.stringParmType.Regular, join_with_next=False)

            # cfP.setItemGeneratorScript(
            #     "__import__('htoa.ocio').ocio.imageFamilyMenu(kwargs['node'])")
            csP.setItemGeneratorScript(
                "__import__('htoa.ocio').ocio.imageColorSpaceMenu(kwargs['node'].parm('%s_cf').eval())" % parm_name )


            #pt = csP.parmTemplate()
            #csP.setMenuItems(('Utility - Raw', 'Utility - sRGB - Texture', 'Utility - Linear - sRGB'))
            grp.insertBefore(grp.find('textures_end'), cfP)
            grp.insertBefore(grp.find('textures_end'), csP)
            node.setParmTemplateGroup(grp)
