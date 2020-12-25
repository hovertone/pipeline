import hou

def main(replaceThis, replaceWith):
    nodes = (hou.node('/obj/arena'), hou.node('/obj/Ruins_snow'), hou.node('/obj/gate'), hou.node('/obj/castle'), hou.node('/obj/Ruins'), hou.node('/obj/castle_ice'), hou.node('/obj/arena_snow'), hou.node('/obj/Cliffs_snow'), hou.node('/obj/spikes'), hou.node('/obj/columns'), hou.node('/obj/Cliffs'), hou.node('/obj/Tower_snow'), hou.node('/obj/Tower'), hou.node('/obj/gate_ice'), hou.node('/obj/columns_snow'))
    geo_readers = list()
    for n in nodes:
        for s in n.children():
            if s.type().name() == 'filecache' or s.type().name() == 'file':
                geo_readers.append(s)

    #print 'READERS'
    for r in geo_readers:
        oldVal = r.parm('file').rawValue()
        if replaceThis in oldVal:
            newVal = oldVal.replace(replaceThis, replaceWith)
            r.parm('file').set(newVal)

    shaders = list()
    image_readers = list()
    for n in nodes:
        for s in n.allSubChildren():
            if s.type().name() == 'arnold_vopnet':
                shaders.append(s)
            elif s.type().name() == 'arnold::image':
                image_readers.append(s)

    print 'SHADERS'
    for s in shaders:
        for p in s.parms():
            oldVal = p.rawValue()
            if replaceThis in oldVal:
                newVal = oldVal.replace(replaceThis, replaceWith)
                p.set(newVal)

    print 'IMAGES'
    for ir in image_readers:
        oldVal = ir.parm('filename').rawValue()
        if replaceThis in oldVal:
            newVal = oldVal.replace(replaceThis, replaceWith)
            ir.parm('filename').set(newVal)


