import hou
import os

mater_names = {
    'VRayNodeMtlRenderStats': 'null',
    'VRayNodeMtlSingleBRDF': 'null',
    'VRayNodeTexNormalMapFlip': 'null',
    'VRayNodeTexBitmap': 'null',
    'vray_material_output': 'arnold_material',
    'VRayNodeBRDFBump': 'arnold::bump2d',
    'VRayNodeBitmapBuffer': 'arnold::image',
    'VRayNodeMtlMulti': 'arnold::switch_shader',
    'VRayNodeBRDFVRayMtl': 'arnold::standard_surface',
}

vray_material = {
    'VRayNodeBRDFBump': {'inputs': [], 'outputs': []},
    'VRayNodeBitmapBuffer': {'inputs': [], 'outputs': []},
    'VRayNodeMtlMulti': {'inputs': [], 'outputs': []},
    'VRayNodeBRDFVRayMtl': {'inputs': [], 'outputs': []},
}

arnold_materials = {
    'arnold::bump2d': {'inputs': [], 'outputs': ''},
    'arnold::image': {'inputs': [], 'outputs': ''},
    'arnold::switch_shader': {'inputs': [], 'outputs': ''},
    'arnold::standard_surface': {'inputs': [], 'outputs': ''},
}

arnold_material = {

}


def process_shading_tree(data, node):
    if not node or node in data:
        return
    # print "Processing", node
    data.append(node)
    for node_input in node.inputs():
        process_shading_tree(data, node_input)


def create_arnold_shading(amb, node):
    #print "CREATE", node.type().name()
    if node.type().name() in mater_names:
        if mater_names[node.type().name()]:
            #print "INPUTS", node.inputs()
            n = amb.createNode(mater_names[node.type().name()])
            #n.moveToGoodPosition()
            #print 'TYPE', type(n)
            return n


def main():
    #vray_mats = []
    nodes = hou.selectedNodes()
    pwd = hou.node(nodes[0].parent().path())
    print 'PWD', pwd.path()
    d = dict()

    for node in nodes:
        l = list()
        for s in node.allSubChildren():
            if s.type().name() == "vray_material_output":
                process_shading_tree(l, s)
                d[node] = l

    # PRINT
    # for k in d.keys():
    #     print k.name()
    #     for i in d[k]:
    #         print '\t', i.name()

    associated = dict()
    for k in d.keys():
        #TEMP THING TO REMOVE EXISTING AMB
        amb_path = '%s/%s' % (pwd.path(), k.name() + '_ARN')
        if hou.node(amb_path):
            hou.node(amb_path).destroy()


        amb = pwd.createNode('arnold_materialbuilder')
        amb.children()[0].destroy() #remove default out_material inside new ARNOLD MATERIAL BUILDER
        amb.setName(k.name() + '_ARN')
        print 'CREATED amb node', amb.path()

        nodesToMove = list()
        for n in d[k]:
            new_node = create_arnold_shading(amb, n)
            if new_node:
                associated[new_node] = n

        amb.moveToGoodPosition()

        # PRINT ASSOCIATED
        # print associated
        # for k in associated.keys():
        #     print '%s :: %s' % (k.name(), associated[k])

        for k in associated.keys():
            print 'K ' + str(k), type(k)
            if k.type().name() == 'arnold::image':
                #print 'working with', k.path()
                vray_node = associated[k]
                path = vray_node.parm('file').eval().replace('\\', '/')
                k.parm('filename').set(path)
                file_name = os.path.splitext(os.path.basename(path))[0]
                #print 'filename before', file_name

                #fix naming
                file_name = file_name.replace(" ", '_')
                #print 'filename after fix', file_name
                if not file_name:
                    file_name = "Image"
                    k.setName(file_name, unique_name=True)
                k.setColor(hou.Color((0.475, 0.812, 0.204)))

        # for n in amb.children():
        #     print 'working on %s' % n.path()
        #     print '\tassociated with %s' % str(associated[n].path())
    # for n in d:
    #     amb = pwd.createNode('arnold_materialbuilder')
    #     try:
    #         amb.setName(n.name() + "_ARN")
    #         create_arnold_shading(amb, n)
    #     except:
    #         create_arnold_shading(amb, n)












