import hou
print '                          START'

def main():
    nn = list(hou.selectedNodes())
    for n in nn:
        c = n.children()[0]
        name = c.name()
        bgp = c.parm('vm_background')
        oldVal = bgp.eval()
        photo1 = name.split('/')[-1]
        photo2 = photo1.split('_')[0]
        newVal = '$PROJECT/in/210809/project/p4/p4_market//%s-ARW_DxO_DeepPRIME.jpg' % photo2
        bgp.set(newVal)
