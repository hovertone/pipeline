import hou
pwd = hou.pwd()
#print pwd.name()
tp_path = pwd.parm('tp_path').eval()
tp = hou.node(tp_path)
pwd.parm('destination_path').set(tp.parm('master_path').eval())