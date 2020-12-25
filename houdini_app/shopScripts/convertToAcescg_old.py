import linecache
import sys
import os

print '======= in convert to acescg =========='

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


tp = hou.pwd()
grp = tp.parmTemplateGroup()
f = grp.find('textures_folder')
parms_to_avoid = tp.parm('parms_to_keep').eval().split(' ')
parm_names = [p.name() for p in f.parmTemplates() if p.name() and p.name() not in parms_to_avoid]

for pn in parm_names:
    print pn

print '\n==============\n'

i_n = hou.node('/img/tex_to_acescg') #HARDCODE
oldTexturePath = tp.parm('master_path').eval()
newTexturePath = 'P:/Raid/assetBuilds/char/barbarian_jotun/main/tex/v006'

shopnet = hou.pwd().parent()
try:
    for pn in parm_names:
        name = tp.parm(pn).name()
        path = grp.find(pn).tags()['node'].split(' ')[0]
        newPath = '/'.join(path.split('/')[:-1])
        print '---%s:' % pn
        cf = hou.node(newPath).parm('color_family').eval()
        cs = hou.node(newPath).parm('color_space').eval()
        #print '\t', hou.node(newPath).parm('color_family').eval(), '::', hou.node(newPath).parm('color_space').eval()
        print '%s : %s' % (pn, cs)
        f = i_n.createNode('file')
        oldPath = tp.parm(pn).eval().replace('<UDIM>', '$F')
        f.parm('filename1').set(oldPath)

        #rename
        rn = i_n.createNode('rename')
        rn.parm('from').set(f.planes()[0])
        rn.parm('to').set('C')
        rn.setInput(0, f)

        #vopcop filter part
        vc = i_n.createNode('vopcop2filter')
        vc.setInput(0, rn)
        grpVC = vc.parmTemplateGroup()
        fromSpaceP = hou.StringParmTemplate(name='fromSpace', label='From Space', num_components=1, menu_items=('Utility - Raw', 'Utility - sRGB - Texture', 'Utility - Linear - sRGB'))
        grpVC.append(fromSpaceP)
        vc.setParmTemplateGroup(grpVC)
        vc.parm('fromSpace').set(cs)

        gl = hou.node(vc.path() + '/global1')
        ou = hou.node(vc.path() + '/output1')

        fltv = vc.createNode('floattovec')
        fltv.setInput(0, gl, 3)
        fltv.setInput(1, gl, 4)
        fltv.setInput(2, gl, 5)

        ocio = vc.createNode('ocio_transform')
        ocio.setInput(0, fltv)
        ocio.parm('fromspace').set('`chs("../fromSpace")`')
        ocio.parm('tospace').set('ACES - ACEScg')

        vecfl = vc.createNode('vectofloat')
        vecfl.setInput(0, ocio)

        ou.setInput(0, vecfl, 0)
        ou.setInput(1, vecfl, 1)
        ou.setInput(2, vecfl, 2)
        ou.setInput(3, gl, 6)

        vc.layoutChildren()

        #rop comp
        rc = i_n.createNode('rop_comp')
        rc.setInput(0, vc)
        replacedPath = oldPath.replace(oldTexturePath, newTexturePath)
        folder, filepath = os.path.split(replacedPath)
        acesfilepath = filepath[:filepath.find('.')] + '_acescg' + filepath[filepath.find('.'):]
        rc.parm('copoutput').set('/'.join([folder, acesfilepath]))

            #print '%s : %s : not scripted' % (pn, cs)


    i_n.layoutChildren()
except:
    PrintException()


