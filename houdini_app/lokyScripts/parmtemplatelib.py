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

#################################
node = hou.selectedNodes()[0]
parm_template = node.parm("tx").parmTemplate()
code = parm_template.asCode()
print code

hou_parm_template = hou.FloatParmTemplate("m_t", "M_Translete", 3, default_value=([0, 0, 0]), min=-1, max=1, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.XYZW)
hou_parm_template.setTags({"autoscope": "1110000000000000", "script_action": "import objecttoolutils\nobjecttoolutils.matchTransform(kwargs, 0)", "script_action_help": "Select an object to match the translation with.", "script_action_icon": "BUTTONS_match_transform"})

hou_parm_template = hou.FloatParmTemplate("m_r", "M_Rotate", 3, default_value=([0, 0, 0]), min=0, max=360, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.XYZW)
hou_parm_template.setTags({"autoscope": "1110000000000000", "script_action": "import objecttoolutils\nobjecttoolutils.matchTransform(kwargs, 1)", "script_action_help": "Select an object to match the rotation with.", "script_action_icon": "BUTTONS_match_rotation"})

hou_parm_template = hou.FloatParmTemplate("m_s", "M_Scale", 3, default_value=([1, 1, 1]), min=-1, max=1, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.XYZW)
hou_parm_template.setTags({"autoscope": "1110000000000000", "script_action": "import objecttoolutils\nobjecttoolutils.matchTransform(kwargs, 2)", "script_action_help": "Select an object to match the scale with.", "script_action_icon": "BUTTONS_match_scale"})

