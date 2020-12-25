import hou

def main():
    n= hou.node(hou.pwd().path())
    n.parm('ogl_texuvset1').set('1')