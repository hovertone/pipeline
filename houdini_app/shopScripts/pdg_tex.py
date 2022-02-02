import hou

# nodes = hou.selectedNodes()
# DEV
def main():
    nodes = (hou.node('/obj/tube1/topnet1/shopnet1/Ork_Warior_Leather'), )

    allImages = dict()
    for n in nodes:
        # print n.name()
        if n.type().name() != 'arnold_vopnet':
            print('ERROR :: wrong type nodes selected')
            return

        images = [i for i in n.allSubChildren() if i.type().name() == 'arnold::image']
        for i in images:
            p = i.parm('filename')
            # print '\t%s link %s' % (i.name(), i.parm('filename').eval() == i.parm('filename').rawValue())
            if p.eval() != p.rawValue():  # whick means filename parameter has a link
                # LINKED PARMS BAKING
                val = p.eval()
                p.revertToDefaults()
                p.set(val)
                print("\t%s's filename parameter has been baked" % i.name())

            allImages[p] = p.rawValue()

    ii = allImages
    # for k, v in ii.iteritems():
    #     print '%s %s' % (k, v)

    values = list(ii.values())
    val_set = sorted(list(set(values)))
    tex_amount = len(val_set)

    for k in val_set:
       print(k)

    to_pdg = dict()
    for v in val_set:
        f = os.path.split
        to_pdg