import hou

node = hou.pwd()
parent = node.parent()
parms = []
for p in node.parms():
    if p.parmTemplate().type() == hou.parmTemplateType.String and p.name() != 'master_path' and '_cs' not in p.name() and 'parms_to_keep' not in p.name():
        parms.append(p)



if parent.type().name() == 'shopnet':
    newSh = parent.createNode('arnold_vopnet', node_name='New_Shader')
elif parent.type().name() == 'matnet':
    newSh = parent.createNode('arnold_materialbuilder', node_name='New_Shader')

print('%s created' % newSh.name())

for p in parms:
    i = newSh.createNode('arnold::image')
    i.parm('filename').set('`chs("../../%s/%s")`' % (node.name(), p.name()))
    i.setName(p.name())
    i.setColor(hou.Color((0.302, 0.525, 0.114)))

newSh.layoutChildren()
pos = (node.position().x(), node.position().y() - 1)
newSh.setPosition(pos)

