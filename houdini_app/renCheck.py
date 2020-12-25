
import hou, os


def rCheck(node):

	message = ""

	for n in node.inputs():
		if not n:
			pass
		else:
			rop = hou.node(n.path())
			path = rop.parm("ar_picture").eval()
			render = "Render exists: No"
			if os.path.exists(path):
				render = "Render exists: Yes"

			cam  = rop.parm("camera").eval()
			res = str(rop.parm("res_overridex").eval()) + " " + str(rop.parm("res_overridey").eval())
			frames = "Frames: " + str(int(rop.parm("f1").eval())) + "-" + str(int(rop.parm("f2").eval()))
			mb = "MotionBlur: Off"
			if rop.parm("ar_mb_xform_enable").eval() == 1:
				mb = "MotionBlur: On"
			ignores = ["operators","textures", "shaders", "atmosphere", "lights", "shadows", "subdivision",
						"displacement", "bump", "smoothing", "dof", "sss", "motion"]
			ign_message = ""
			for i in ignores:
				if rop.parm("ar_ignore_" + i).eval() == 1:
					ign_message += "IGNORE: " + i + ", "
			message += '\n'.join(["Name: " + rop.name(), render, cam, res, frames, mb, ign_message, '\n'])


	u = hou.ui.displayMessage(text=message, buttons=("Render", "Cancel"))
	if u == 0:
		import afanasy
		reload(afanasy)
		afanasy.render(node)


