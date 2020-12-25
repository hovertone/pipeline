###############################################################################
# Name:
#   zshotmask_ui.py
#
# Author:
#   Chris Zurbrigg (http://zurbrigg.com)
#
# Usage:
#   Visit http://zurbrigg.com for details
#
# Copyright (C) 2018 Chris Zurbrigg. All rights reserved.
###############################################################################

import maya.cmds as cmds
import maya.OpenMaya as om


class ZShotMask(object):

    PLUG_IN_NAME = "zshotmask.py"
    NODE_NAME = "zshotmask"

    TRANSFORM_NODE_NAME = "zshotmask"
    SHAPE_NODE_NAME = "zshotmask_shape"

    DEFAULT_BORDER_COLOR = [0.0, 0.0, 0.0, 1.0]
    DEFAULT_LABEL_COLOR = [1.0, 1.0, 1.0, 1.0]

    LABEL_COUNT = 6
    MIN_COUNTER_PADDING = 1
    MAX_COUNTER_PADDING = 6
    DEFAULT_COUNTER_PADDING = 4

    OPT_VAR_CAMERA_NAME = "zurShotMaskCameraNameOptVar"
    OPT_VAR_LABEL_TEXT = "zurShotMaskLabelTextOptVar"
    OPT_VAR_LABEL_FONT = "zurShotMaskLabelFontOptVar"
    OPT_VAR_LABEL_COLOR = "zurShotMaskLabelColorOptVar"
    OPT_VAR_LABEL_SCALE = "zurShotMaskLabelScaleOptVar"
    OPT_VAR_BORDER_VISIBLE = "zurShotMaskBorderVisibleOptVar"
    OPT_VAR_BORDER_COLOR = "zurShotMaskBorderColorOptVar"
    OPT_VAR_BORDER_SCALE = "zurShotMaskBorderScaleOptVar"
    OPT_VAR_COUNTER_POSITION = "zurShotMaskCounterPositionOptVar"
    OPT_VAR_COUNTER_PADDING = "zurShotMaskCounterPaddingOptVar"

    @classmethod
    def create_mask(cls):
        if not cmds.pluginInfo(cls.PLUG_IN_NAME, q=True, loaded=True):
            try:
                cmds.loadPlugin(cls.PLUG_IN_NAME)
            except:
                om.MGlobal.displayError("Failed to load ZShotMask plug-in: {0}".format(cls.PLUG_IN_NAME))
                return

        if not cls.get_mask():
            transform_node = cmds.createNode("transform", name=cls.TRANSFORM_NODE_NAME)
            cmds.createNode(cls.NODE_NAME, name=cls.SHAPE_NODE_NAME, parent=transform_node)

        cls.refresh_mask()

    @classmethod
    def delete_mask(cls):
        mask = cls.get_mask()
        if mask:
            transform = cmds.listRelatives(mask, fullPath=True, parent=True)
            if transform:
                cmds.delete(transform)
            else:
                cmds.delete(mask)

    @classmethod
    def get_mask(cls):
        if cmds.pluginInfo(cls.PLUG_IN_NAME, q=True, loaded=True):
            nodes = cmds.ls(type=cls.NODE_NAME)
            if len(nodes) > 0:
                return nodes[0]

        return None

    @classmethod
    def refresh_mask(cls):
        mask = cls.get_mask()
        if not mask:
            return

        cmds.setAttr("{0}.camera".format(mask), cls.get_camera_name(), type="string")

        try:
            label_text = cls.get_label_text()
            cmds.setAttr("{0}.topLeftText".format(mask), label_text[0], type="string")
            cmds.setAttr("{0}.topCenterText".format(mask), label_text[1], type="string")
            cmds.setAttr("{0}.topRightText".format(mask), label_text[2], type="string")
            cmds.setAttr("{0}.bottomLeftText".format(mask), label_text[3], type="string")
            cmds.setAttr("{0}.bottomCenterText".format(mask), label_text[4], type="string")
            cmds.setAttr("{0}.bottomRightText".format(mask), label_text[5], type="string")
        except:
            pass

        label_color = cls.get_label_color()
        cmds.setAttr("{0}.fontName".format(mask), cls.get_label_font(), type="string")
        cmds.setAttr("{0}.fontColor".format(mask), label_color[0], label_color[1], label_color[2], type="double3")
        cmds.setAttr("{0}.fontAlpha".format(mask), label_color[3])
        cmds.setAttr("{0}.fontScale".format(mask), cls.get_label_scale())

        border_visibility = cls.get_border_visible()
        border_color = cls.get_border_color()
        cmds.setAttr("{0}.topBorder".format(mask), border_visibility[0])
        cmds.setAttr("{0}.bottomBorder".format(mask), border_visibility[1])
        cmds.setAttr("{0}.borderColor".format(mask), border_color[0], border_color[1], border_color[2], type="double3")
        cmds.setAttr("{0}.borderAlpha".format(mask), border_color[3])
        cmds.setAttr("{0}.borderScale".format(mask), cls.get_border_scale())

        cmds.setAttr("{0}.counterPosition".format(mask), cls.get_counter_position())
        cmds.setAttr("{0}.counterPadding".format(mask), cls.get_counter_padding())

    @classmethod
    def set_camera_name(cls, name):
        cmds.optionVar(sv=[cls.OPT_VAR_CAMERA_NAME, name])

    @classmethod
    def get_camera_name(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_CAMERA_NAME):
            return cmds.optionVar(q=cls.OPT_VAR_CAMERA_NAME)
        else:
            return ""

    @classmethod
    def set_label_text(cls, text_array):
        array_len = len(text_array)
        if array_len != cls.LABEL_COUNT:
            om.MGlobal.displayError("Failed to set label text. Invalid number of text values in array: {0} (expected 6)".format(array_len))
            return

        cmds.optionVar(sv=[cls.OPT_VAR_LABEL_TEXT, text_array[0]])
        for i in range(1, array_len):
            cmds.optionVar(sva=[cls.OPT_VAR_LABEL_TEXT, text_array[i]])

    @classmethod
    def get_label_text(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_LABEL_TEXT):
            return cmds.optionVar(q=cls.OPT_VAR_LABEL_TEXT)

        return ["", "Shot Name", "", "Animator Name", "", ""]

    @classmethod
    def set_label_font(cls, font):
        cmds.optionVar(sv=[cls.OPT_VAR_LABEL_FONT, font])

    @classmethod
    def get_label_font(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_LABEL_FONT):
            label_font = cmds.optionVar(q=cls.OPT_VAR_LABEL_FONT)
            if label_font:
                return label_font

        if cmds.about(win=True):
            return "Times New Roman"
        elif cmds.about(mac=True):
            return "Times New Roman-Regular"
        elif cmds.about(linux=True):
            return "Courier"
        else:
            return "Times-Roman"

    @classmethod
    def set_label_color(cls, red, green, blue, alpha):
        cmds.optionVar(fv=[cls.OPT_VAR_LABEL_COLOR, red])
        cmds.optionVar(fva=[cls.OPT_VAR_LABEL_COLOR, green])
        cmds.optionVar(fva=[cls.OPT_VAR_LABEL_COLOR, blue])
        cmds.optionVar(fva=[cls.OPT_VAR_LABEL_COLOR, alpha])

    @classmethod
    def get_label_color(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_LABEL_COLOR):
            return cmds.optionVar(q=cls.OPT_VAR_LABEL_COLOR)
        else:
            return cls.DEFAULT_LABEL_COLOR

    @classmethod
    def set_label_scale(cls, scale):
        cmds.optionVar(fv=[cls.OPT_VAR_LABEL_SCALE, scale])

    @classmethod
    def get_label_scale(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_LABEL_SCALE):
            return cmds.optionVar(q=cls.OPT_VAR_LABEL_SCALE)
        else:
            return 1.0

    @classmethod
    def set_border_visible(cls, top, bottom):
        cmds.optionVar(iv=[cls.OPT_VAR_BORDER_VISIBLE, top])
        cmds.optionVar(iva=[cls.OPT_VAR_BORDER_VISIBLE, bottom])

    @classmethod
    def get_border_visible(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_BORDER_VISIBLE):
            border_visibility = cmds.optionVar(q=cls.OPT_VAR_BORDER_VISIBLE)
            try:
                if len(border_visibility) == 2:
                    return border_visibility
            except:
                pass

        return [1, 1]

    @classmethod
    def set_border_color(cls, red, green, blue, alpha):
        cmds.optionVar(fv=[cls.OPT_VAR_BORDER_COLOR, red])
        cmds.optionVar(fva=[cls.OPT_VAR_BORDER_COLOR, green])
        cmds.optionVar(fva=[cls.OPT_VAR_BORDER_COLOR, blue])
        cmds.optionVar(fva=[cls.OPT_VAR_BORDER_COLOR, alpha])

    @classmethod
    def get_border_color(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_BORDER_COLOR):
            return cmds.optionVar(q=cls.OPT_VAR_BORDER_COLOR)
        else:
            return cls.DEFAULT_BORDER_COLOR

    @classmethod
    def set_border_scale(cls, scale):
        cmds.optionVar(fv=[cls.OPT_VAR_BORDER_SCALE, scale])

    @classmethod
    def get_border_scale(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_BORDER_SCALE):
            return cmds.optionVar(q=cls.OPT_VAR_BORDER_SCALE)
        else:
            return 1.0

    @classmethod
    def set_counter_position(cls, pos):
        cmds.optionVar(iv=[cls.OPT_VAR_COUNTER_POSITION, pos])

    @classmethod
    def get_counter_position(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_COUNTER_POSITION):
            pos = cmds.optionVar(q=cls.OPT_VAR_COUNTER_POSITION)
            if pos >= 0 and pos <= 6:
                return pos

        return 6

    @classmethod
    def set_counter_padding(cls, padding):
        cmds.optionVar(iv=[cls.OPT_VAR_COUNTER_PADDING, padding])

    @classmethod
    def get_counter_padding(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_COUNTER_PADDING):
            pos = cmds.optionVar(q=cls.OPT_VAR_COUNTER_PADDING)
            if pos >= cls.MIN_COUNTER_PADDING and pos <= cls.MAX_COUNTER_PADDING:
                return pos

        return cls.DEFAULT_COUNTER_PADDING

    @classmethod
    def reset_settings(cls):
        cmds.optionVar(remove=cls.OPT_VAR_BORDER_COLOR)
        cmds.optionVar(remove=cls.OPT_VAR_BORDER_SCALE)
        cmds.optionVar(remove=cls.OPT_VAR_BORDER_VISIBLE)
        cmds.optionVar(remove=cls.OPT_VAR_CAMERA_NAME)
        cmds.optionVar(remove=cls.OPT_VAR_COUNTER_PADDING)
        cmds.optionVar(remove=cls.OPT_VAR_COUNTER_POSITION)
        cmds.optionVar(remove=cls.OPT_VAR_LABEL_COLOR)
        cmds.optionVar(remove=cls.OPT_VAR_LABEL_FONT)
        cmds.optionVar(remove=cls.OPT_VAR_LABEL_SCALE)
        cmds.optionVar(remove=cls.OPT_VAR_LABEL_TEXT)


class ZShotMaskUi(object):

    VERSION = "1.0.2"

    WINDOW_NAME = "ZShotMaskUi"

    APP_NAME = "Shot Mask VP2.0"

    LABELS = ["Top-Left  ", "Top-Center  ", "Top-Right  ", "Bottom-Left  ", "Bottom-Center  ", "Bottom-Right  "]

    ALL_CAMERAS = "<All Cameras>"

    @classmethod
    def display(cls):
        cls.delete()

        main_window = cmds.window(cls.WINDOW_NAME,
                                  title="{0} (http://zurbrigg.com)".format(cls.APP_NAME),
                                  sizeable=True,
                                  menuBar=True)
        edit_menu = cmds.menu(label="Edit", parent=main_window)
        cmds.menuItem(label="Reset Settings", command="ZShotMaskUi.reset_settings()", parent=edit_menu)

        help_menu = cmds.menu(label="Help", parent=main_window)
        cmds.menuItem(label="About", command="ZShotMaskUi.about()", parent=help_menu)

        main_layout = cmds.columnLayout(adjustableColumn=True, parent=main_window)

        # Camera Section
        camera_layout = cmds.frameLayout(label="Camera", parent=main_layout)
        camera_form_layout = cmds.formLayout(parent=camera_layout)

        cls.camera_name = cmds.textFieldButtonGrp(label="Name  ",
                                                  buttonLabel=" ... ",
                                                  columnWidth=(1, 90),
                                                  changeCommand="ZShotMaskUi.update_mask()",
                                                  buttonCommand="ZShotMaskUi.display_camera_dialog()",
                                                  parent=camera_form_layout)

        cmds.formLayout(camera_form_layout, e=True, af=(cls.camera_name, "top", 3))
        cmds.formLayout(camera_form_layout, e=True, af=(cls.camera_name, "left", 0))

        # Labels Section
        label_layout = cmds.frameLayout(label="Labels", parent=main_layout)
        label_form_layout = cmds.formLayout(parent=label_layout)

        cls.label_text_ctrls = []
        cls.label_settings_scale_ctrls = []
        cls.label_settings_offset_x_ctrls = []
        cls.label_settings_offset_y_ctrls = []

        label_text = ["", "", "", "", "", ""]

        for i in range(0, len(label_text)):
            cls.create_label_fields(i, label_form_layout)

        cls.label_font_tfg = cmds.textFieldButtonGrp(label="Font  ",
                                                     buttonLabel=" ... ",
                                                     columnWidth=(1, 90),
                                                     editable=False,
                                                     buttonCommand="ZShotMaskUi.display_font_dialog()",
                                                     parent=label_form_layout)

        cls.label_color_csg = cmds.colorSliderGrp(label="Color  ",
                                                  columnWidth=(1, 90),
                                                  changeCommand="ZShotMaskUi.update_mask()",
                                                  dragCommand="ZShotMaskUi.update_mask()",
                                                  parent=label_form_layout)
        cls.label_trans_csg = cmds.colorSliderGrp(label="Transparency  ",
                                                  columnWidth=(1, 90),
                                                  changeCommand="ZShotMaskUi.update_mask()",
                                                  dragCommand="ZShotMaskUi.update_mask()",
                                                  parent=label_form_layout)

        font_scale_label = cmds.text("Scale  ", align="right", width=93, parent=label_form_layout)
        cls.label_scale = cmds.floatField(width=50,
                                          value=1.0,
                                          minValue=0.1,
                                          maxValue=2.0,
                                          step=0.01,
                                          precision=2,
                                          changeCommand="ZShotMaskUi.update_mask()",
                                          dragCommand="ZShotMaskUi.update_mask()",
                                          parent=label_form_layout)

        cmds.formLayout(label_form_layout, e=True, af=(cls.label_text_ctrls[0], "top", 3))
        cmds.formLayout(label_form_layout, e=True, af=(cls.label_text_ctrls[0], "left", 0))

        label_text_count = len(cls.label_text_ctrls)
        for i in range(1, label_text_count):
            cmds.formLayout(label_form_layout, e=True, ac=(cls.label_text_ctrls[i], "top", 0, cls.label_text_ctrls[i - 1]))
            cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_text_ctrls[i], "left", 0, cls.label_text_ctrls[i - 1]))

        cmds.formLayout(label_form_layout, e=True, ac=(cls.label_font_tfg, "top", 0, cls.label_text_ctrls[label_text_count - 1]))
        cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_font_tfg, "left", 0, cls.label_text_ctrls[label_text_count - 1]))

        cmds.formLayout(label_form_layout, e=True, ac=(cls.label_color_csg, "top", 0, cls.label_font_tfg))
        cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_color_csg, "left", 0, cls.label_font_tfg))
        cmds.formLayout(label_form_layout, e=True, ac=(cls.label_trans_csg, "top", 0, cls.label_color_csg))
        cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_trans_csg, "left", 0, cls.label_color_csg))
        cmds.formLayout(label_form_layout, e=True, ac=(font_scale_label, "top", 4, cls.label_trans_csg))
        cmds.formLayout(label_form_layout, e=True, ac=(cls.label_scale, "top", 0, cls.label_trans_csg))
        cmds.formLayout(label_form_layout, e=True, ac=(cls.label_scale, "left", 0, font_scale_label))
        cmds.formLayout(label_form_layout, e=True, af=(cls.label_scale, "bottom", 5))

        # Border Section
        border_layout = cmds.frameLayout(label="Border", parent=main_layout)

        border_form_layout = cmds.formLayout(parent=border_layout)
        cls.border_vis_cbg = cmds.checkBoxGrp(numberOfCheckBoxes=2,
                                              label="",
                                              labelArray2=("Top", "Bottom"),
                                              columnWidth3=(90, 60, 60),
                                              changeCommand="ZShotMaskUi.update_mask()",
                                              parent=border_form_layout)
        cls.border_color_csg = cmds.colorSliderGrp(label="Color  ",
                                                   columnWidth=(1, 90),
                                                   changeCommand="ZShotMaskUi.update_mask()",
                                                   dragCommand="ZShotMaskUi.update_mask()",
                                                   parent=border_form_layout)
        cls.border_trans_csg = cmds.colorSliderGrp(label="Transparency  ",
                                                   columnWidth=(1, 90),
                                                   changeCommand="ZShotMaskUi.update_mask()",
                                                   dragCommand="ZShotMaskUi.update_mask()",
                                                   parent=border_form_layout)
        border_scale_label = cmds.text("Scale  ", align="right", width=93, parent=border_form_layout)
        cls.border_scale = cmds.floatField(width=50,
                                           value=1.0,
                                           minValue=0.5,
                                           maxValue=2.0,
                                           step=0.01,
                                           precision=2,
                                           changeCommand="ZShotMaskUi.update_mask()",
                                           dragCommand="ZShotMaskUi.update_mask()",
                                           parent=border_form_layout)

        cmds.formLayout(border_form_layout, e=True, af=(cls.border_vis_cbg, "top", 3))
        cmds.formLayout(border_form_layout, e=True, af=(cls.border_vis_cbg, "left", 0))

        cmds.formLayout(border_form_layout, e=True, ac=(cls.border_color_csg, "top", 0, cls.border_vis_cbg))
        cmds.formLayout(border_form_layout, e=True, ac=(cls.border_trans_csg, "top", 0, cls.border_color_csg))
        cmds.formLayout(border_form_layout, e=True, ac=(border_scale_label, "top", 4, cls.border_trans_csg))
        cmds.formLayout(border_form_layout, e=True, ac=(cls.border_scale, "top", 0, cls.border_trans_csg))
        cmds.formLayout(border_form_layout, e=True, ac=(cls.border_scale, "left", 0, border_scale_label))
        cmds.formLayout(border_form_layout, e=True, af=(cls.border_scale, "bottom", 5))

        # Counter Section
        counter_layout = cmds.frameLayout(label="Counter", parent=main_layout)
        counter_form_layout = cmds.formLayout(parent=counter_layout)

        cls.counter_vis_cbg = cmds.checkBoxGrp(numberOfCheckBoxes=1,
                                               label="",
                                               label1=("Enable"),
                                               columnWidth2=(90, 60),
                                               changeCommand="ZShotMaskUi.update_mask()",
                                               parent=counter_form_layout)
        cls.counter_position = cmds.radioButtonGrp(numberOfRadioButtons=4,
                                                   label="",
                                                   columnWidth5=(90, 86, 86, 86, 86),
                                                   labelArray4=("Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"),
                                                   changeCommand="ZShotMaskUi.update_mask()",
                                                   parent=counter_form_layout)
        counter_padding_label = cmds.text("Padding  ", align="right", width=93, parent=counter_form_layout)
        cls.counter_padding = cmds.intField(width=50,
                                            value=1,
                                            minValue=1,
                                            maxValue=6,
                                            step=1,
                                            changeCommand="ZShotMaskUi.update_mask()",
                                            parent=counter_form_layout)

        cmds.formLayout(counter_form_layout, e=True, af=(cls.counter_vis_cbg, "top", 3))
        cmds.formLayout(counter_form_layout, e=True, af=(cls.counter_vis_cbg, "left", 0))
        cmds.formLayout(counter_form_layout, e=True, ac=(cls.counter_position, "top", 0, cls.counter_vis_cbg))
        cmds.formLayout(counter_form_layout, e=True, ac=(counter_padding_label, "top", 4, cls.counter_position))
        cmds.formLayout(counter_form_layout, e=True, ac=(cls.counter_padding, "top", 0, cls.counter_position))
        cmds.formLayout(counter_form_layout, e=True, ac=(cls.counter_padding, "left", 0, counter_padding_label))

        # Buttons
        button_layout = cmds.formLayout(parent=main_layout)
        create_btn = cmds.button(label="Create",
                                 width=80,
                                 command="ZShotMask.create_mask()",
                                 parent=button_layout)
        delete_btn = cmds.button(label="Delete",
                                 width=80,
                                 command="ZShotMask.delete_mask()",
                                 parent=button_layout)
        cmds.formLayout(button_layout, e=True, af=(delete_btn, "right", 0))
        cmds.formLayout(button_layout, e=True, ac=(create_btn, "right", 2, delete_btn))

        cmds.window(main_window, e=True, w=100, h=100)
        cmds.window(main_window, e=True, sizeable=False)
        cmds.window(main_window, e=True, rtf=True)

        cls.update_ui_elements()

        cmds.showWindow(main_window)

    @classmethod
    def delete(cls):
        if cmds.window(cls.WINDOW_NAME, exists=True):
            cmds.deleteUI(cls.WINDOW_NAME, window=True)

    @classmethod
    def create_label_fields(cls, text_index, parent):

        text = cmds.textFieldGrp(label=cls.LABELS[text_index],
                                 columnWidth=(1, 90),
                                 changeCommand="ZShotMaskUi.update_mask()",
                                 parent=parent)

        cls.label_text_ctrls.append(text)

    @classmethod
    def display_camera_dialog(cls):
        result = cmds.layoutDialog(ui="ZShotMaskUi.camera_dialog_layout()",
                                   title="Select Camera",
                                   parent=cls.WINDOW_NAME)

        if result not in ["cancel", "dismiss"]:
            cmds.textFieldButtonGrp(cls.camera_name, e=True, text=result)
            cls.update_mask()

    @classmethod
    def camera_dialog_layout(cls):
        cameras = cmds.listCameras()
        cameras.insert(0, cls.ALL_CAMERAS)

        layout = cmds.setParent(q=True)
        cmds.formLayout(layout, e=True)

        cls.camera_tsl = cmds.textScrollList(numberOfRows=8,
                                             parent=layout)
        for camera in cameras:
            cmds.textScrollList(cls.camera_tsl,
                                e=True,
                                append=camera,
                                doubleClickCommand="ZShotMaskUi.camera_dialog_ok()")

        current_camera = cmds.textFieldButtonGrp(cls.camera_name, q=True, text=True)
        if current_camera in cameras:
            cmds.textScrollList(cls.camera_tsl, e=True, selectItem=current_camera)

        ok_button = cmds.button(label="OK", c="ZShotMaskUi.camera_dialog_ok()")
        cancel_button = cmds.button(label="Cancel", c="ZShotMaskUi.camera_dialog_cancel()")

        cmds.formLayout(layout, e=True, af=(cls.camera_tsl, "top", 0))
        cmds.formLayout(layout, e=True, af=(cls.camera_tsl, "left", 0))
        cmds.formLayout(layout, e=True, af=(cls.camera_tsl, "right", 0))

        cmds.formLayout(layout, e=True, ac=(cancel_button, "top", 4, cls.camera_tsl))
        cmds.formLayout(layout, e=True, af=(cancel_button, "right", 0))

        cmds.formLayout(layout, e=True, aoc=(ok_button, "top", 0, cancel_button))
        cmds.formLayout(layout, e=True, ac=(ok_button, "right", 2, cancel_button))

    @classmethod
    def camera_dialog_ok(cls):
        selection = cmds.textScrollList(cls.camera_tsl, q=True, selectItem=True)
        if not selection:
            camera = ""
        else:
            camera = selection[0]
        cmds.layoutDialog(dismiss=camera)

    @classmethod
    def camera_dialog_cancel(cls):
        cmds.layoutDialog(dismiss="cancel")

    @classmethod
    def display_font_dialog(cls):
        font = cmds.fontDialog()
        if font:
            font = font.split('|', 1)[0]
            cmds.textFieldButtonGrp(cls.label_font_tfg, e=True, text=font)

            cls.update_mask()

    @classmethod
    def update_ui_elements(cls):
        if not cmds.window(cls.WINDOW_NAME, exists=True):
            return

        camera_name = ZShotMask.get_camera_name()
        if not camera_name:
            camera_name = cls.ALL_CAMERAS
        cmds.textFieldButtonGrp(cls.camera_name, e=True, text=camera_name)

        label_text = ZShotMask.get_label_text()
        for i in range(len(cls.label_text_ctrls)):
            cmds.textFieldGrp(cls.label_text_ctrls[i], e=True, text=label_text[i])

        color = ZShotMask.get_label_color()
        label_color = [color[0], color[1], color[2]]
        label_alpha = [color[3], color[3], color[3]]

        color = ZShotMask.get_border_color()
        border_color = [color[0], color[1], color[2]]
        border_alpha = [color[3], color[3], color[3]]

        cmds.textFieldButtonGrp(cls.label_font_tfg, e=True, text=ZShotMask.get_label_font())
        cmds.colorSliderGrp(cls.label_color_csg, e=True, rgbValue=label_color)
        cmds.colorSliderGrp(cls.label_trans_csg, e=True, rgbValue=label_alpha)
        cmds.floatField(cls.label_scale, e=True, value=ZShotMask.get_label_scale())

        border_visibility = ZShotMask.get_border_visible()
        cmds.checkBoxGrp(cls.border_vis_cbg, e=True, value1=border_visibility[0])
        cmds.checkBoxGrp(cls.border_vis_cbg, e=True, value2=border_visibility[1])
        cmds.colorSliderGrp(cls.border_color_csg, e=True, rgbValue=border_color)
        cmds.colorSliderGrp(cls.border_trans_csg, e=True, rgbValue=border_alpha)
        cmds.floatField(cls.border_scale, e=True, value=ZShotMask.get_border_scale())

        counter_position = ZShotMask.get_counter_position()
        counter_enabled = counter_position == 1 or counter_position == 3 or counter_position == 4 or counter_position == 6
        radio_btn_index = 0
        if counter_position == 1:
            radio_btn_index = 1
        elif counter_position == 3:
            radio_btn_index = 2
        elif counter_position == 4:
            radio_btn_index = 3
        elif counter_position == 6:
            radio_btn_index = 4

        cmds.checkBoxGrp(cls.counter_vis_cbg, e=True, value1=counter_enabled)
        cmds.radioButtonGrp(cls.counter_position, e=True, select=radio_btn_index)
        cmds.intField(cls.counter_padding, e=True, value=ZShotMask.get_counter_padding())

    @classmethod
    def update_mask(cls):
        if not cmds.window(cls.WINDOW_NAME, exists=True):
            return

        ZShotMask.set_camera_name(cmds.textFieldButtonGrp(cls.camera_name, q=True, text=True))

        text_array = []
        for i in range(len(cls.LABELS)):
            text_array.append(cmds.textFieldGrp(cls.label_text_ctrls[i], q=True, text=True))

        ZShotMask.set_label_text(text_array)
        ZShotMask.set_label_font(cmds.textFieldButtonGrp(cls.label_font_tfg, q=True, text=True))

        label_color = cmds.colorSliderGrp(cls.label_color_csg, q=True, rgbValue=True)
        label_alpha = cmds.colorSliderGrp(cls.label_trans_csg, q=True, rgbValue=True)
        ZShotMask.set_label_color(label_color[0], label_color[1], label_color[2], label_alpha[0])
        ZShotMask.set_label_scale(cmds.floatField(cls.label_scale, q=True, value=True))

        borderTopEnabled = cmds.checkBoxGrp(cls.border_vis_cbg, q=True, value1=True)
        borderBottomEnabled = cmds.checkBoxGrp(cls.border_vis_cbg, q=True, value2=True)
        ZShotMask.set_border_visible(borderTopEnabled, borderBottomEnabled)

        border_color = cmds.colorSliderGrp(cls.border_color_csg, q=True, rgbValue=True)
        border_alpha = cmds.colorSliderGrp(cls.border_trans_csg, q=True, rgbValue=True)
        ZShotMask.set_border_color(border_color[0], border_color[1], border_color[2], border_alpha[0])
        ZShotMask.set_border_scale(cmds.floatField(cls.border_scale, q=True, value=True))

        if cmds.checkBoxGrp(cls.counter_vis_cbg, q=True, value1=True):
            radio_btn_index = cmds.radioButtonGrp(cls.counter_position, q=True, select=True)
            counter_position = 6
            if radio_btn_index == 1:
                counter_position = 1
            elif radio_btn_index == 2:
                counter_position = 3
            elif radio_btn_index == 3:
                counter_position = 4

            ZShotMask.set_counter_position(counter_position)
        else:
            ZShotMask.set_counter_position(0)

        ZShotMask.set_counter_padding(cmds.intField(cls.counter_padding, q=True, value=True))

        ZShotMask.refresh_mask()

    @classmethod
    def about(cls):
        message = '<h3>Zurbrigg {0}</h3>'.format(cls.APP_NAME)
        message += '<p>Version: {0}<br>'.format(cls.VERSION)
        message += 'Author:  Chris Zurbrigg</p>'
        message += '<a style="color:white;" href="http://zurbrigg.com">http://zurbrigg.com</a><br>'
        message += '<p>Copyright &copy; 2018 Chris Zurbrigg</p>'

        cmds.confirmDialog(title="About", button="OK", message=message, messageAlign="left", parent=cls.WINDOW_NAME)

    @classmethod
    def reset_settings(cls):
        ZShotMask.reset_settings()
        ZShotMask.refresh_mask()

        cls.update_ui_elements()


if __name__ == "__main__":
    ZShotMaskUi.display()
