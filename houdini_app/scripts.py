import glob
import hou
import os
import re

def getnum(filename):
    digits = re.findall('(\d+)', filename)
    count = len(digits)
    if count>0:
        num = int(digits[count-1])
    else:
        num = 0
    return num

def setLastVersion():
    nodeName = hou.pwd()
    nodepath = nodeName.path()
    charName = hou.parm(nodepath+"/charName").eval()
    maxversion = 0
    project = hou.getenv("PROJECT")
    sequence = hou.getenv("SQ")
    shotnum = hou.parm(nodepath+"/shotNum").eval()
    if not shotnum:
        shotnum = "sh000"
    path = project+"/sequences/"+sequence+"/"+shotnum+"/cache/anim/"+charName+"/main/"
    if os.path.exists(path):
        numlist = []
        file_list_pre = os.listdir(path)
        for file in file_list_pre:
            filenum = int(getnum(file))
            numlist.append(filenum)
        maxversion = str(max(numlist)).zfill(3)
        if max(numlist)>0:
            hou.parm(nodepath+"/version").set(int(maxversion))
            print '%s version set' % int(maxversion)
    
def linkParameters():
    selectedNodes = hou.selectedNodes()
    #print selectedNodes
    for node in selectedNodes:
        print 'inside %s' % node.name()
        for child in node.children():
            childGeos = []
            if child.type().name() == 'geo':
                childGeos.append(child)
            #print '\tchildGeos are %s' % childGeos
            allParms = node.parms()
            switch = False
            for p in allParms:
                if p.name() == 'categories':
                    switch = True
                if switch:
                    #print '%s type is %s' % (p.name(), p.parmTemplate().type())
                    #print '.String' in str(p.parmTemplate().type())
                    for c in childGeos:
                        if '.String' in str(p.parmTemplate().type()):
                            c.parm(p.name()).setExpression('chs("../%s")' % p.name())
                        else:
                            c.parm(p.name()).setExpression('ch("../%s")' % p.name())


def findAOVsInAsset():
    #sn = hou.selectedNodes()
    node = hou.pwd()
    pwd = hou.pwd()
    print 'NODE NAME %s' % node.name()
    #sn = [hou.node('/obj/char_orderknight1')]
    if 'aovs' in [i.name() for i in node.parms()]:
        mats = []
        for c in node.allSubChildren():
            if c.type().name() == 'material':
                mats.append(c)

        shaders = []
        for m in mats:
            #print int(m.parm('num_materials').eval())
            for i in range(int(m.parm('num_materials').eval())):
                relPath = m.parm('shop_materialpath%s' % str(i+1)).eval()
                #relPath = node.evalParm('path')
                relNode = m.node(relPath)
                fullpath = relNode.path()
                shaders.append(fullpath)

        #print shaders
        passes = []
        for s in shaders:
            node = hou.node(s)
            print '-- in %s' % node.name()
            #nn = [i for i in node.children() if i.type().name() == 'arnold::standard_surface' or i.type.name() == 'arnold::aov_write_float']
            nn = []
            for c in node.children():
                #print '%s :: %s' % (c.name(), c.type().name())
                if str(c.type().name()) == 'arnold::standard_surface' or str(c.type().name()) == 'arnold::standard_hair' or str(c.type().name()) == 'arnold::aov_write_float' or str(c.type().name()) == 'arnold::aov_write_int'  or str(c.type().name()) == 'arnold::aov_write_rgb'  or str(c.type().name()) == 'arnold::aov_write_rgba':
                    nn.append(c)


            for n in nn:
                print '\tin %s' % n.name()
                if 'arnold::aov_write' in n.type().name():
                    value = n.parm('aov_name').eval()
                    if value != '' and value not in passes:
                        print '\t\t' + value
                        passes.append(value)
                elif 'arnold::standard_surface' in n.type().name() or 'arnold::standard_hair' in n.type().name():
                    for i in range(1, 9):
                        value = n.parm('aov_id%s' % i).eval()
                        if value != '' and value not in passes:
                            print '\t\t' + value
                            passes.append(value)

        print 'MATTES: %s' % ' '.join(sorted(passes))
        #print 'NODE NAME 2 %s' % node.name()
        pwd.parm('aovs').set(' '.join(sorted(passes)))
        #nn = []
        #for c in node.allSubChildren():
        #    if c.type().name() == 'arnold::standard_surface':
        #        nn.append(c)

        #for n in nn:
        #    print n.name()

def AOVsToROP():
    node = hou.pwd()
    contrib = node.parm('aovs').eval().split(' ')

    out = hou.node('/out')
    rr = list(out.allNodes())
    # print type(rr)
    ropToAdjust = hou.ui.selectFromList([i.name() for i in rr])
    for i in ropToAdjust:
        r = rr[i]
        # contrib_local = contrib
        aovs_amount = int(r.parm('ar_aovs').eval())
        aovs = [r.parm('ar_aov_label%s' % str(i + 1)).eval() for i in range(aovs_amount)]
        for j, c in enumerate(contrib):
            if c not in aovs:
                r.parm('ar_aovs').set(int(r.parm('ar_aovs').eval()) + 1)
                r.parm('ar_aov_label%s' % str(int(r.parm('ar_aovs').eval()))).set(c)

def getShader(hdaName, hdaLabel = None):
    nodeName = hou.pwd()
    parent=nodeName.parent()
    if not hdaLabel: hdaLabel = hdaName
    try:
        shaderNode = parent.createNode(hdaName, node_name=hdaLabel)
        nodeName.setInput(2, shaderNode, 0)
        #shaiderNode.moveToGoodPosition(relative_to_inputs=True, move_inputs=True, move_outputs=True, move_unconnected=True)
        #parent.layoutChildren((shaiderNode,), horizontal_spacing=-1.0, vertical_spacing=-1.0)
        shaderNode.setPosition((nodeName.position().x(), nodeName.position().y()+1))
    except:
        print "NODE: "+hdaName+" Not Found!!!"

def getFX(hdaName, hdaLabel = None):
    nodeName = hou.pwd()
    parent=nodeName.parent()
    if not hdaLabel: hdaLabel = hdaName
    try:
        shaiderNode = parent.createNode(hdaName, node_name=hdaLabel)
        nodeName.setInput(1, shaiderNode, 0)
        #shaiderNode.moveToGoodPosition(relative_to_inputs=True, move_inputs=True, move_outputs=True, move_unconnected=True)
        #parent.layoutChildren((shaiderNode,), horizontal_spacing=-1.0, vertical_spacing=-1.0)
        shaiderNode.setPosition((nodeName.position().x(), nodeName.position().y() + 1))
    except:
        print "NODE: "+hdaName+" Not Found!!!"


def separateAOVsForROP():
    arnolds = [node for node in hou.selectedNodes() if node.type().name() == "arnold"]
    for node in arnolds:
        path = node.parm('ar_picture').rawValue()
        folder = os.path.dirname(path)
        filename = os.path.basename(path)
        name, ext = os.path.splitext(filename)
        aovs = node.parm('ar_aovs')
        for i in range(1, aovs.eval() + 1):
            index = str(i)
            aovname = node.parm("ar_aov_label" + index).eval()
            # aovpath = folder + "/" + aovname + "_" + name + ext
            # aovpath = folder + "/" + aovname + "_" + name + ext
            # aovpath = """pythonexprs("(hou.node('.').parm('ar_picture').unexpandedString()).replace((hou.node('.').parm('ar_picture').unexpandedString().split('/')[len(hou.node('.').parm('ar_picture').unexpandedString().split('/'))-1]), hou.node('.').parm('ar_aov_label'+ (hou.expandString('$CH')).replace('ar_aov_separate_file', '')).eval() + '_' + (hou.node('.').parm('ar_picture').unexpandedString().split('/')[len(hou.node('.').parm('ar_picture').unexpandedString().split('/'))-1]))")"""
            aovpath = '$SHOT/render/$OS/v`padzero(3, chsop("version"))`/`chs("ar_aov_label%s")`/`$SN`_`$OS`_`chs("ar_aov_label%s")`_v`padzero(3, chsop("version"))`.$F4.exr' % (index, index)
            node.parm("ar_aov_separate" + index).set(1)
            node.parm("ar_aov_separate_file" + index).set(aovpath)

def removeAOVsSeparation():
    arnolds = [node for node in hou.selectedNodes() if node.type().name() == "arnold"]
    for node in arnolds:
        path = node.parm('ar_picture').rawValue()
        folder = os.path.dirname(path)
        filename = os.path.basename(path)
        name, ext = os.path.splitext(filename)
        aovs = node.parm('ar_aovs')
        for i in range(1, aovs.eval() + 1):
            index = str(i)
            #aovname = node.parm("ar_aov_label" + index).eval()
            node.parm("ar_aov_separate" + index).set(0)

def sustitutePaths():
    shop = hou.node('/obj/DarkElve_Shading/geometry/Darkelf_Shader2/shopnet')
    for s in shop.children():
        print s.name()
        parms = [i for i in s.parms() if 'elf' in i.name()]
        for p in parms:
            oldVal = p.eval()
            newVal = oldVal.replace('//vpstorage.plarium.local/vpd/raid/assets/characters/dark_elves_support/texturing/texture/v005', '$PROJECT/in/191004/tex_v005')
            print '\t%s' % newVal
            p.set(newVal)


def importAllFBXFromPath():
    root_path = 'P:/UnderTheSea/in/200311'
    ext_to_find = '.fbx'

    fbx_list = list()
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(ext_to_find):
                fbx_path = os.path.join(root, file).replace('\\', '/')
                #print 'FBX PATH IS %s' % fbx_path
                fbx_list.append(fbx_path)

    fbx_list.sort()
    # FOR INCREMENT TRIGGERING
    check_dir_splited = fbx_list[0].strip(root_path).split('/')[:-1]
    check_dir ='/'.join(check_dir_splited)
    #print 'CHECK DIR %s' % check_dir

    netw = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    pwd = netw.pwd()
    #print pwd.path()

    # ACTION
    dir_counter = 0
    x_offset, y_offset = 3.0, 4.0
    x, y = 0, 0
    orig = [0, 0]
    label_created = False
    for p in fbx_list:
        dir_name_splitted = p.strip(root_path).split('/')[:-1]
        dir_name = '/'.join(dir_name_splitted)
        #print 'DIR NAME %s' % dir_name
        file_name = p.strip(root_path).split('/')[-1].strip(ext_to_find)

        #LABEL STUFF
        if not label_created:
            st = pwd.createStickyNote()
            st.setText(dir_name)
            #st.resize()
            st.setPosition((orig[0] + x*x_offset,  orig[1] + y*y_offset - y_offset/3))
            label_created = True

        f = pwd.createNode('file')
        f.parm('file').set(p)
        f.setPosition((orig[0] + x*x_offset, orig[1] + y*y_offset))
        print 'FILENAME %s' % file_name
        x += 1



        if dir_name != check_dir:
            dir_counter += 1
            x = 0
            y += 1
            check_dir = dir_name
            label_created = False

def createDarkNull():
    print 'IN DARK NULL'
    netw = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    pwd = netw.pwd()
    #print pwd.path()

    sel = hou.selectedNodes()
    #print sel
    if len(sel) == 1 and sel[0].type().name() == 'null': # ONLY ONE NULL NODE HAD BEEN SELECTED
        n = sel[0]
    elif len(sel) == 0: # NO NODES HAD BEEN SELECTED
        n = pwd.createNode('null')
    elif len(sel) > 0:
        n = pwd.createNode('null')
        n.setInput(0, sel[-1])
        n.moveToGoodPosition()
        n.setRenderFlag(True)
        n.setDisplayFlag(True)

    type_color = hou.Color((0.475, 0.812, 0.204))
    n.setColor(type_color)
    #n.setUserData('nodeshape', 'circle')
    n.setName('OUT', unique_name=True)
    n.setSelected(True)

