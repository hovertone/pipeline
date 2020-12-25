import hou

mater_names = {
    'VRayNodeMtlRenderStats': None,
    'VRayNodeMtlSingleBRDF': None,
    'VRayNodeTexNormalMapFlip': None,
    'VRayNodeTexBitmap': None,
    'vray_material_output': None,
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
    data[node] = {'name': node}
    for node_input in node.inputs():
        process_shading_tree(data, node_input)


def create_arnol_shading(main, node):
    print "CREATE", node.type().name()
    if node.type().name() in mater_names:
        if mater_names[node.type().name()]:
            print "INPUTS", node.inputs()
            main.createNode(mater_names[node.type().name()])


def main():
    vray_mats = []
    nodes = hou.selectedNodes()
    current = hou.node(nodes[0].parent().path())

    for node in nodes:
        for s in node.allSubChildren():
            if s.type().name() == "vray_material_output":
                d = {}
                process_shading_tree(d, s)
                m = dict(mat=node.name(), data=d)
                vray_mats.append(m)

    for mat in vray_mats:
        a = current.createNode('arnold_materialbuilder')
        for i in mat["data"]:
            try:
                a.setName(mat["mat"] + "_ARN")
                create_arnol_shading(a, i)
            except:
                create_arnol_shading(a, i)


main()











