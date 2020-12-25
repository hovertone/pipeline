def addParms():
	import hou
	targetNode = hou.selectedNodes()[0]
	# Code for parameter template
	hou_parm_template = hou.FolderParmTemplate("ogl_numtex", "Diffuse Texture Layers", folder_type=hou.folderType.MultiparmBlock, default_value=1, ends_tab_group=False)
	hou_parm_template.setTags({"spare_category": "OpenGL"})
	# Code for parameter template
	hou_parm_template2 = hou.ToggleParmTemplate("ogl_use_tex#", "Use Diffuse Map #", default_value=True)
	hou_parm_template2.setHelp("None")
	hou_parm_template2.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
	hou_parm_template.addParmTemplate(hou_parm_template2)
	# Code for parameter template
	hou_parm_template2 = hou.StringParmTemplate("ogl_tex#", "Texture #", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
	hou_parm_template2.setHelp("None")
	hou_parm_template2.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
	hou_parm_template.addParmTemplate(hou_parm_template2)
	# Code for parameter template
	hou_parm_template2 = hou.StringParmTemplate("ogl_texuvset#", "UV Set", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["uv","uv2","uv3","uv4","uv5","uv6","uv7","uv8"]), menu_labels=(["uv","uv2","uv3","uv4","uv5","uv6","uv7","uv8"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
	hou_parm_template2.setHelp("None")
	hou_parm_template2.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
	hou_parm_template.addParmTemplate(hou_parm_template2)
	# Code for parameter template
	hou_parm_template2 = hou.StringParmTemplate("ogl_tex_min_filter#", "Minification Filter", 1, default_value=(["GL_LINEAR_MIPMAP_LINEAR"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["GL_NEAREST","GL_LINEAR","GL_NEAREST_MIPMAP_NEAREST","GL_LINEAR_MIPMAP_NEAREST","GL_NEAREST_MIPMAP_LINEAR","GL_LINEAR_MIPMAP_LINEAR"]), menu_labels=(["No filtering (very poor)","Bilinear (poor)","No filtering, Nearest Mipmap (poor)","Bilinear, Nearest Mipmap (okay)","No filtering, Blend Mipmaps (good)","Trilinear (best)"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
	hou_parm_template2.setHelp("None")
	hou_parm_template2.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
	hou_parm_template.addParmTemplate(hou_parm_template2)
	# Code for parameter template
	hou_parm_template2 = hou.StringParmTemplate("ogl_tex_mag_filter#", "Magnification Filter", 1, default_value=(["GL_LINEAR"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["GL_NEAREST","GL_LINEAR"]), menu_labels=(["No filtering","Bilinear"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
	hou_parm_template2.setHelp("None")
	hou_parm_template2.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
	hou_parm_template.addParmTemplate(hou_parm_template2)
	# Code for parameter template
	hou_parm_template2 = hou.StringParmTemplate("ogl_tex_wrap#", "Texture Wrap", 1, default_value=(["repeat"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["repeat","clamp","decal","mirror"]), menu_labels=(["Repeat","Streak","Decal","Mirror"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
	hou_parm_template2.setHelp("None")
	hou_parm_template2.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
	hou_parm_template.addParmTemplate(hou_parm_template2)
	# Code for parameter template
	hou_parm_template2 = hou.StringParmTemplate("ogl_tex_vwrap#", "Texture V Wrap", 1, default_value=(["repeat"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["repeat","clamp","decal","mirror"]), menu_labels=(["Repeat","Streak","Decal","Mirror"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
	hou_parm_template2.setHelp("None")
	hou_parm_template2.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
	hou_parm_template.addParmTemplate(hou_parm_template2)
	targetNode.addSpareParmTuple(hou_parm_template)
	
	
	# Code for parameter template
	hou_parm_template = hou.ToggleParmTemplate("ogl_use_specmap", "Use Specular Map", default_value=True)
	hou_parm_template.setHelp("When enabled, use the map specified in ogl_specmap for the\n    specular map. If this property is not present, it is assumed to be\n    enabled.")
	hou_parm_template.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
	targetNode.addSpareParmTuple(hou_parm_template)
	# Code for parameter template
	hou_parm_template = hou.StringParmTemplate("ogl_specmap", "Specular Map", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
	hou_parm_template.setHelp("The image file to use for modifying specular reflections. The RGB values of\n    the file are multiplied by the specular colors of lights when shading.")
	hou_parm_template.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
	targetNode.addSpareParmTuple(hou_parm_template)
	# Code for parameter template
	hou_parm_template = hou.IntParmTemplate("ogl_speclayer", "Specular Layer", 1, default_value=([0]), min=0, max=15, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
	hou_parm_template.setConditional(hou.parmCondType.DisableWhen, "{ ogl_specmap == \\\"\\\" }")
	hou_parm_template.setHelp("The texture layer that the UV coordinates for the specular map are sourced \n    from.")
	hou_parm_template.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
	targetNode.addSpareParmTuple(hou_parm_template)
	# Code for parameter template
	hou_parm_template = hou.ToggleParmTemplate("ogl_use_roughmap", "Use Roughness Map", default_value=True)
	hou_parm_template.setHelp("When enabled, use the map specified in ogl_roughmap for the\n    roughness map. If this property is not present, it is assumed to be\n    enabled.")
	hou_parm_template.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
	targetNode.addSpareParmTuple(hou_parm_template)
	# Code for parameter template
	hou_parm_template = hou.StringParmTemplate("ogl_roughmap", "Roughness Map", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
	hou_parm_template.setHelp("Texture map for Roughness. Rougher surfaces have larger but dimmer specular highlights. This overrides the constant ogl_rough.")
	hou_parm_template.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
	targetNode.addSpareParmTuple(hou_parm_template)
	# Code for parameter template
	hou_parm_template = hou.ToggleParmTemplate("ogl_invertroughmap", "Invert Roughness Map (Glossiness)", default_value=False)
	hou_parm_template.setConditional(hou.parmCondType.DisableWhen, "{ ogl_roughmap == \\\"\\\" }")
	hou_parm_template.setHelp("Invert the roughness map so that it is interpreted as a gloss map - \n    zero is no gloss (dull), one is very glossy (shiny).")
	hou_parm_template.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
	targetNode.addSpareParmTuple(hou_parm_template)
	# Code for parameter template
	hou_parm_template = hou.IntParmTemplate("ogl_roughmap_comp", "Roughness Channel", 1, default_value=([0]), min=0, max=4, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=(["0","1","2","3","4"]), menu_labels=(["Luminance","Red","Green","Blue","Alpha"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
	hou_parm_template.setConditional(hou.parmCondType.DisableWhen, "{ ogl_roughmap == \\\"\\\" }")
	hou_parm_template.setHelp("Texture component used for Roughness within the Roughness texture map, \n    which can be the luminance of RGB, red, green, blue or alpha. This allows\n    roughness to be sourced from packed texture maps which contain parameters \n    in the other texture channels.")
	hou_parm_template.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
	targetNode.addSpareParmTuple(hou_parm_template)
	# Code for parameter template
	hou_parm_template = hou.ToggleParmTemplate("ogl_use_metallicmap", "Use Metallic Map", default_value=True)
	hou_parm_template.setHelp("When enabled, use the map specified in ogl_metallicmap for the\n    metallic map. If this property is not present, it is assumed to be\n    enabled.")
	hou_parm_template.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
	targetNode.addSpareParmTuple(hou_parm_template)
	# Code for parameter template
	hou_parm_template = hou.StringParmTemplate("ogl_metallicmap", "Metallic Map", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
	hou_parm_template.setHelp("Texture map for Metallic. The GL Metallic parameter is multiplied by the\n    texture map value.")
	hou_parm_template.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
	targetNode.addSpareParmTuple(hou_parm_template)
	# Code for parameter template
	hou_parm_template = hou.IntParmTemplate("ogl_metallicmap_comp", "Metallic Channel", 1, default_value=([0]), min=0, max=4, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=(["0","1","2","3","4"]), menu_labels=(["Luminance","Red","Green","Blue","Alpha"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
	hou_parm_template.setConditional(hou.parmCondType.DisableWhen, "{ ogl_metallicmap == \\\"\\\" }")
	hou_parm_template.setHelp("Channel of the metallic texture map to sample (luminance, red, green, blue,\n    alpha).")
	hou_parm_template.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
	targetNode.addSpareParmTuple(hou_parm_template)