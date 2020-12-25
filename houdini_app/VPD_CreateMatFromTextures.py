#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys, getpass, re
import os.path
from os import path

import hou
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import glob
from functools import partial
import textwrap
import ConfigParser
import shutil
import threading
import time
import datetime
import PIL
from PIL import Image

fGray = "<font color=\"#878787\">"
fWhite = "<font color=\"#FFFFFF\">"
fGreen = "<font color=\"#00FF00\">"
fRed = "<font color=\"#FF0000\">"
fEnd = "</font>"
  
stylesheet = hou.qt.styleSheet()

ToolTipStyle = """QToolTip {
                           font-size: 16px; background-color: #303030; border: 2px solid grey}
                           """

#------------------------------------------------------------------------

def Fn_Connect_node (Node, BeforeNode, AfterNode):
    #конектим ноду между двумя заддаными нодами 
    #(с проверками на отсутствие и смещением существующих нод)
    if BeforeNode == None:
        pos = AfterNode.position()
        if AfterNode.outputs() !=():
            AfterNode.outputs()[0].setFirstInput(Node)
        Node.setFirstInput(AfterNode)
        Node.setGenericFlag(hou.nodeFlag.Render, True)
        Node.setGenericFlag(hou.nodeFlag.Display, True)
    else:
        pos = BeforeNode.position()
        if BeforeNode != None:
            Node.setFirstInput(BeforeNode)
        if AfterNode != None:
            AfterNode.setFirstInput(Node)
    if AfterNode == None:
        Node.setGenericFlag(hou.nodeFlag.Render, True)
        Node.setGenericFlag(hou.nodeFlag.Display, True)
    Node.setPosition(pos)
    Node.move(hou.Vector2((0.0, -1.0)))
    if Node.outputs() !=():
        for itm in Node.parent().children():
            if Node in itm.inputAncestors():
                itm.move(hou.Vector2((0.0, -1.0)))    
    
def Fn_Create_SOP_MaterialNode (SopNode, after, SG, MatName):
    #создаем ноду SOP_material. до или после заданной ноды   
    BeforeNode = None
    AfterNode = None
    shop = Fn_Create_SOP_Shopnet(SopNode.parent()).name()
    #print shop
    if SG == "":
        materialName = MatName
        groups = ""
    else:
        materialName = SG[0]
        groups = ' ' .join(SG[1])
    material = SopNode.parent().createNode('material', materialName)

    material.parm('shop_materialpath1').set("../" +shop +"/" + MatName)
    
    #print SG[1]
    #print groups
    material.parm('group1').set(groups)
    if after ==0:
        Node = material
        if SopNode.inputs() != ():
            BeforeNode = SopNode.inputs()[0]
        AfterNode = SopNode
        Fn_Connect_node(Node, BeforeNode, AfterNode)
    if after ==1:
        Node = material
        BeforeNode = SopNode
        if SopNode.outputs() != ():
            AfterNode = SopNode.outputs()[0]
        Fn_Connect_node(Node, BeforeNode, AfterNode)
    return material    
     
def Fn_Create_SOP_Shopnet (ObjNode):     
    # создаем SOP_shopnet, если его еще нет             
    IsShopnetExist = 0
    for itm in ObjNode.children():
        if itm.type().name() == "shopnet":
            IsShopnetExist = 1
            shop = itm
    if IsShopnetExist != 1:        
        shop = ObjNode.createNode('shopnet', 'shopnet')
        shop.moveToGoodPosition()
    return shop    
    
def Fn_CopyPaste_Nodes (CopiedNode, DestinationNode):
    #копирует ноду или список нод в заданное место.
    CopiedNode_list = []
    if type(CopiedNode) in [list,tuple]:
        CopiedNode_list = CopiedNode    
    else: 
        CopiedNode_list.append(CopiedNode)
    NewNode = hou.copyNodesTo(CopiedNode_list, DestinationNode)
    return NewNode 
    
def Fn_NodeChk (node):
    error = 0
    if node.type().name() == "geo" and node.children() == ():    
        error = 1 
    if node.type().name() == "shopnet":
        error = 2    
    if node.type().name() == "arnold_vopnet":
        error = 0    
    NodeChk = error
    return NodeChk    

def Fn_NewMsgBox (text="NewToolButton"):    
    msgBox = QtWidgets.QMessageBox()
    msgBox.setFixedWidth(500)
    msgBox.setFixedHeight(200)
    msgBox.setText(text)
    msgBox.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    msgBox.setStyleSheet(stylesheet)
    msgBox.exec_()

def Fn_FindSop(node):
    SopNode = node
    NodeChk = Fn_NodeChk(node)
    if node.type().name() == "geo" and NodeChk == 0:
        for itm in node.children():
            if itm.isGenericFlagSet(hou.nodeFlag.Render):
                return itm
    if node.parent().type().name() == "geo" and NodeChk == 0:
        return node
    if node.parent().type().name() == "arnold_vopnet":
        return node
    if NodeChk != 0:
        return None 

    #    "arnold_vopnet"

def Fn_Load_MatNode_To_SOP ():
    #загружает выбранный материал в shopnet созданный 
    #внутри выбранной geo ноды. создает ноду material, 
    #прописывает путь к созданному материалу    
    sel = hou.selectedItems()
    if sel ==():
        Fn_NewMsgBox(
                    """ERROR: Nothing is selected. Select 
                    Geo node(s), or any node in SOP context"""
                    )  
    else: 

        NewMat = Fn_LoadMatNodeToShop()
        Fin_Msg = ""
        #print "aaaaaa"
        for node in sel:
            NodeChk = Fn_NodeChk(node)
            #print NodeChk
            if node.type().name() == "geo" and NodeChk == 0:
                #print "geo -  0"
                for itm in node.children():
                    if itm.isGenericFlagSet(hou.nodeFlag.Render):
                        SopNode = itm
                material = Fn_Create_SOP_MaterialNode(SopNode, 0)
                Fin_Msg = (Fin_Msg + "[ " + node.path() 
                + " ] \n SUCCESS: Material created in  \n")
            elif node.parent().type().name() == "geo"  and NodeChk == 0:
                #print "parent geo -  0"
                SopNode = node

                material = Fn_Create_SOP_MaterialNode(SopNode, 1)
                #print "material - ", material   
                Fin_Msg = (Fin_Msg + "[ " + node.parent().path() 
                + " ] \n SUCCESS: Material created in  \n")
            else:
                if NodeChk == 0:
                    Fin_Msg = (Fin_Msg + "[ " + node.path() 
                    + """ ] \n ERROR: - It is not a GEO node 
                        or it's not in SOP context \n""")
                if NodeChk == 1:
                    Fin_Msg = (Fin_Msg + "[ " + node.path() 
                    + " ] \n ERROR: - Node is empty \n")
                if NodeChk == 2:
                    Fin_Msg = (Fin_Msg + "[ " + node.path() 
                    + " ] \n ERROR: - It is a Shopnet \n")
                continue
                            
            shop = Fn_Create_SOP_Shopnet(SopNode.parent())
            MovedMat = Fn_CopyPaste_Nodes(NewMat, shop)
            material.setName(str(MovedMat[0].name())) 
            for itm in SopNode.parent().children():
                if  (
                    itm.type().name() == "material" 
                    and itm.color() == hou.Color((0.332, 0.832, 0.332))
                    ):
                    itm.setColor(hou.Color((0.832, 0.832, 0.832)))
            material.setColor(hou.Color((0.332, 0.832, 0.332)))
            material.parm('shop_materialpath1').set("../" 
                + SopNode.parent().relativePathTo(MovedMat[0]))
            Fn_NewNode_Arrange(MovedMat[0])
        NewMat.destroy()    
        if Fin_Msg!="":        
            Fn_NewMsgBox(Fin_Msg)

def Fn_Find_List_Diff (list1, list2):
    #находит разницу между двумя списками
    return list(set(list1).symmetric_difference(set(list2)))  
   
def Fn_NewNode_Arrange (node):
    #перемешает заданную ноду на 1 "юнит" ниже чем все ноды в родительском контексте
    pos = node.position()
    for itm in node.parent().children():
        if itm.position()[0] < (pos[0] + 1) and itm.position()[0] > (pos[0] - 1):
            if itm.position()[1] < pos[1]:
               pos[1] = itm.position()[1]
    node.setPosition(pos) 
    node.move(hou.Vector2((0.0, -1.0)))   

def Fn_SortByMatList (val):
    return val.order


#------------------------------------------------------------------------

def Fn_CreateLayout (name="new",type = "H", HPolice = "Preferred",
                                             VPolice = "Preferred"):
    #_locals = locals()
    if type == "H":
        exec(name + "_Layout" " = QtWidgets.QHBoxLayout()", globals())
    if type == "V":
        exec(name + "_Layout" " = QtWidgets.QVBoxLayout()", globals())
       
    exec(name + "_Wgt" " = QtWidgets.QWidget()", globals())
    exec(name + "_Wgt.setLayout(" + name + "_Layout)", globals())
    exec(name + "_Wgt.setStyleSheet(stylesheet)")
    exec(name + "_Wgt.setSizePolicy(QtWidgets.QSizePolicy." + HPolice 
                    + ", QtWidgets.QSizePolicy." + VPolice + ")")


 
def Fn_Align_Wgts (Layout, Text=""):
    if Text.find("|")!=-1: 
        Algn = (Text.replace(" ","")).split("|")
        ##print  Algn
    SAlgn=["",""]
    for i in range(2):
        if Algn[i] == "Right":
            SAlgn[i]= QtCore.Qt.AlignRight
        if Algn[i] == "Left":
            SAlgn[i]= QtCore.Qt.AlignLeft
        if Algn[i] == "HCenter":
            SAlgn[i]= QtCore.Qt.AlignHCenter
        if Algn[i] == "Top":
            SAlgn[i]= QtCore.Qt.AlignTop
        if Algn[i] == "Bottom":
            SAlgn[i]= QtCore.Qt.AlignBottom
        if Algn[i] == "VCenter":
            SAlgn[i]= QtCore.Qt.AlignVCenter  
    for index in range(Layout.count()):
        wgt = Layout.itemAt(index).widget()
        Layout.setAlignment(wgt, SAlgn[0] | SAlgn[1]) 



def Fn_NewToolButton (Name="NewToolButton", Width=100, Height=30):
    btn = QtWidgets.QToolButton()
    btn.setText(Name)
    btn.setFixedWidth(Width)
    btn.setFixedHeight(Height)
    #btn.setIcon(QtGui.QIcon(Icon))
    #btn.setIconSize(QtCore.QSize(IconW,IconH))
    return btn

SelectedFolderPath = ""
TexList = []
SopNode = None
ObjNode = None

class Class_Create_Material_Dialog(QtWidgets.QWidget):

    def closeEvent(self, event):
        del os.CreateMaterialDialog
        #print "X is clicked"

    def Fn_Exit(self):
        os.CreateMaterialDialog.close()

    def Fn_Change_Type(self, row, index):
        TexTypeWgt = self.Texture_Table.cellWidget(row,2)
        Type = TexTypeWgt.currentText()
        Index = self.TexType_List.index(Type)
        orderLbl = self.Texture_Table.cellWidget(row,5).setText(str(Index))
        TexTypeWgt.setStyleSheet("QComboBox {color: #00ff00;}")
        if Type == "unknown":
            TexTypeWgt.setStyleSheet("QComboBox {color: #ffffff;}")
        self.Fn_Resize_Table(self.Texture_Table)
               
    def Fn_AutoType(self, row):
        TexTypeWgt = self.Texture_Table.cellWidget(row,2) 
        TexName = self.Texture_Table.cellWidget(row,1).text()
        Type =self.fn_GetTexType(TexName)
        TexTypeWgt.setCurrentText(Type)
        
    def Fn_Change_AllType(self, Index):
        for row in range(self.Texture_Table.rowCount()):
            if self.AllTexType_ComboBox.currentText()!="Automatic":
                
                TexTypeWgt = self.Texture_Table.cellWidget(row,2)
                TexTypeWgt.setCurrentText("unknown")
                
            else:
                self.Fn_AutoType(row)

    def Fn_AutoTexName(self, row):
        TexNameWgt = self.Texture_Table.cellWidget(row,1) 
        TokenWgt = self.Texture_Table.cellWidget(row,4) 
        tex = TexNameWgt.tex
        
        Token = self.Fn_TokenParse(row, TokenWgt.currentText())
        TexName = tex[0] + tex[1] + Token + tex[3] + "." + tex[4]  
        TexNameWgt.setText(TexName)
        cnt = len(tex[2])
        TexNameWgt.setToolTip("There are " +fGreen+ str(cnt) + " files" 
            + fEnd + " with this name. Tokens are: \n" 
            +fGreen + str(tex[2])+ fEnd) 
        
    def Fn_AutoColorSpace(self, row):
        ext = self.Texture_Table.cellWidget(row,1).tex[-1]
        if ext != "exr":
            self.AllColorSpace_ComboBox.setCurrentText("Srgb Textures")
        else:
            self.AllColorSpace_ComboBox.setCurrentIndex(0)


        self.Fn_Change_AllColorSpaceCombo()

    def Fn_Change_ColorSpaceCombo(self, row, index):
        pass
        #TexColorSpaceWgt = self.Texture_Table.cellWidget(row,2)
        #if TexColorSpaceWgt.currentIndex()==0:
        #    TexColorSpaceWgt.setStyleSheet("QComboBox {color: #ffffff;}")
        #if TexColorSpaceWgt.currentIndex()==1:
        #    TexColorSpaceWgt.setStyleSheet("QComboBox {color: #ff0000;}")
        #if TexColorSpaceWgt.currentIndex()==2:
        #    TexColorSpaceWgt.setStyleSheet("QComboBox {color: #00ff00;}")

    def Fn_Change_AllColorSpaceCombo(self):

        for row in range(self.Texture_Table.rowCount()):
            TexColorSpaceWgt = self.Texture_Table.cellWidget(row,3)
            Type = self.Texture_Table.cellWidget(row,2).currentText()
            #print self.ColorSpaceAll_List
            if self.AllColorSpace_ComboBox.currentText() == "Linear Textures":
                if 'ACES Textures' not in self.ColorSpaceAll_List:
                    TexColorSpaceWgt.setCurrentText("Linear")
                    #print "Linear Textures"
                else:
                    TexColorSpaceWgt.setCurrentText("Utility - Raw")
                    #print "Utility - Raw"
            if self.AllColorSpace_ComboBox.currentText() == "Srgb Textures":
                if 'ACES Textures' not in self.ColorSpaceAll_List:
                    if Type =="base_color":
                        TexColorSpaceWgt.setCurrentText("sRGB")
                    else:
                        TexColorSpaceWgt.setCurrentText("Linear")
                else:
                    if Type =="base_color":
                        TexColorSpaceWgt.setCurrentText("Utility - Linear - sRGB")
                    else:
                        TexColorSpaceWgt.setCurrentText("Utility - Raw")
                    
            if self.AllColorSpace_ComboBox.currentText() == "ACES Textures":
                TexColorSpaceWgt.setCurrentText("ACES - ACEScg")

                
               # TexColorSpaceWgt.setCurrentIndex(Index)
                #if TexColorSpaceWgt.currentIndex()==0:
                #    TexColorSpaceWgt.setStyleSheet("QComboBox {color: #ffffff;}")
                #if TexColorSpaceWgt.currentIndex()==1:
                #    TexColorSpaceWgt.setStyleSheet("QComboBox {color: #ff0000;}")
               # if TexColorSpaceWgt.currentIndex()==2:
                #    TexColorSpaceWgt.setStyleSheet("QComboBox {color: #00ff00;}")
           # else:
                #print "else"
                #self.Fn_Change_ColorSpaceCombo()
                #self.Fn_AutoColorSpace(row)


#self.ColorSpace_List=['sRGB', 'Linear']
#self.ColorSpaceAll_List=['Linear Textures', 'Srgb Textures']

#self.ColorSpace_List=['Utility - Linear - sRGB', 'Utility - Raw', 'ACES - ACEScg']
#self.ColorSpaceAll_List=[ 'ACES Textures', 'Linear Textures', 'Srgb Textures']

    def Fn_AutoToken(self, row):
        TokenWgt = self.Texture_Table.cellWidget(row,4) 
        tex = self.Texture_Table.cellWidget(row,1).tex
        TokenWgt.setStyleSheet("QComboBox {color: #ffffff;}")
        TokenWgt.setCurrentText("<UDIM>")
        if len(tex[2])==1:
            TokenWgt.setCurrentText("None")
            TokenWgt.setStyleSheet("QComboBox {color: #ff0000;}")

    def Fn_Change_TokenCombo(self, row, index):
        TokenWgt = self.Texture_Table.cellWidget(row,4)
        if TokenWgt.currentText() =="<UDIM>":
            TokenWgt.setStyleSheet("QComboBox {color: #ffffff;}")
        elif TokenWgt.currentText() =="Frames":
            TokenWgt.setStyleSheet("QComboBox {color: #ffffff;}")
        elif TokenWgt.currentText() =="None":
            TokenWgt.setStyleSheet("QComboBox {color: #ff0000;}")
        self.Fn_AutoTexName(row)

    def Fn_Change_AllTokenCombo(self, index):
        for row in range(self.Texture_Table.rowCount()):
            if self.AllToken_ComboBox.currentText()!="Automatic":
                self.Texture_Table.cellWidget(row,4).setCurrentIndex(index)
                self.Fn_Change_TokenCombo(row, index)
            else:
                self.Fn_AutoToken(row)

    def Fn_TokenParse(self, row, TokenName):
        tex = self.Texture_Table.cellWidget(row,1).tex
        #print tex[2]
        if TokenName =="<UDIM>":
            Token = "<UDIM>"
            if tex[2]==['']:
                Token = ""
        if TokenName =="Frames":
            Token = "$F4"
            if tex[2]==['']:
                Token = ""
        if TokenName =="None":
            if len(tex[2])==0:
                Token = ""
            else:
                Token = str(tex[2][0])
        return Token

    def Fn_Create_TexList(self):

        
        global SelectedFolderPath
        if SelectedFolderPath!="":       

            #print 
            #self.TexDirectory = "D:/v002"
            extList = ["exr", "png", "tif", "jpg"] 
            
            TmpTexList = []  
            nameSet = []        
            for x in os.listdir(SelectedFolderPath):
                num = (re.search(r'\d{4}', x))
                before = None
                after = None
                if num!=None:
                    before = (re.search(r'\D', x[num.start()-1]))  
                    after = (re.search(r'\D', x[num.end()]))
                if before ==None or after==None:
                    num = None
                tmp=x.split(".")
                ext = tmp[len(tmp)-1] 
                if num!=None:
                    numpos = num.start()
                    name2 = x[(numpos+4):len((x.split("."+ext))[0])]
                    separ = ""
                    if (x[numpos-1])==".":
                       numpos-=1
                       separ = "."
                    
                    name = x[0:numpos]
                    num = num.group()
                else:
                    separ = ""
                    name = x.split(".")[0]
                    name2 = ""
                    num = ""
                if ext in extList:
                    nameSet.append(name+name2)
                    TmpTexList.append([name, separ, num, name2, ext])

            
            nameSet= list(set(nameSet))
            
            TexList=[]
            for SetItm in nameSet:
                numList=[]
                for ListItm in TmpTexList:
                    if SetItm ==(ListItm[0]+ListItm[3]):
                        numList.append(ListItm[2])
                        ext = ListItm[4]
                        name = ListItm[0]
                        name2 = ListItm[3]
                        separ = ListItm[1]
                
                TexList.append([name, separ, numList, name2, ext])

            return TexList

    def Fn_Create_TexTable(self):
        #self.TexList = self.Fn_Create_TexList()
        #print self.TexList
        global TexList
        if TexList !=[]:
            self.Texture_Table.clearSpans()
            row=0
            self.Texture_Table.setSortingEnabled(0)
            self.Texture_Table.setRowCount(len(TexList))
            self.Fn_NoTextures()

            for tex in TexList:
                ##print tex
                Tex_CheckBox = QCheckBox()
                Tex_CheckBox.setCheckState(QtCore.Qt.Checked)
                #Tex_CheckBox.stateChanged.connect(self.Fn_Group_Check_Selector) 
                self.Texture_Table.setCellWidget(row, 0, Tex_CheckBox)  

                TexName_label = QLabel()
                TexName_label.setMargin(3)
                TexName_label.tex = tex
                TexName_label.setStyleSheet(ToolTipStyle)
                self.Texture_Table.setCellWidget(row, 1, TexName_label)  
                          
                TexType_ComboBox = QComboBox()
                TexType_ComboBox.setStyleSheet(ToolTipStyle)
                for Type in self.TexType_List:       
                    TexType_ComboBox.addItem(Type)
                TexType_ComboBox.currentIndexChanged.connect(partial(self.Fn_Change_Type, row))            
                self.Texture_Table.setCellWidget(row, 2, TexType_ComboBox)
                
                ColorSpace_ComboBox = QComboBox()
                ColorSpace_ComboBox.setStyleSheet(ToolTipStyle)
                for ColorSpace in self.ColorSpace_List:
                    ColorSpace_ComboBox.addItem(ColorSpace)
                ColorSpace_ComboBox.currentIndexChanged.connect(partial(self.Fn_Change_ColorSpaceCombo, row ))
                self.Texture_Table.setCellWidget(row, 3, ColorSpace_ComboBox)

                NumberType_ComboBox = QComboBox()
                NumberType_ComboBox.setStyleSheet(ToolTipStyle)
                for NumberType in self.TokenType_List:
                    NumberType_ComboBox.addItem(NumberType)
                NumberType_ComboBox.currentIndexChanged.connect(partial(self.Fn_Change_TokenCombo, row ))
                self.Texture_Table.setCellWidget(row, 4, NumberType_ComboBox)
                
                Order_label = QLabel()
                self.Texture_Table.setCellWidget(row, 5, Order_label) 
                self.Texture_Table.setColumnHidden(5,1)   
                
                row+=1
                self.Texture_Table.resizeRowsToContents()
                self.Texture_Table.resizeColumnsToContents()
                #self.Texture_Table.setMinimumHeight(self.Texture_Table.rowCount()*31)
                
            self.Fn_SetAuto_TexTable()

            #print self.TexDirectory
        # else:
        #     self.Fn_Exit()

    def Fn_SetAuto_TexTable(self):
        row=0
        for tex in TexList:
            self.Fn_AutoToken(row)
            self.Fn_AutoTexName(row)
            self.Fn_AutoType(row)
            self.Fn_AutoColorSpace(row)
            self.Fn_Change_Type(row, 0)
            self.Fn_Auto_MatName()
            row+=1

        self.Texture_Table.resizeColumnsToContents()
        self.Fn_Resize_Table(self.Texture_Table)
    

    def Fn_Resize_Table(self,table):
   
        width = 0
        for col in range(table.columnCount()):
            width = width + table.columnWidth(col) 
        table.setMinimumWidth(width+30)
        table.setMaximumWidth(width+30)

        Height=0
        for col in range(table.rowCount()):
            Height = Height + table.rowHeight(col) 
        table.setMinimumHeight(Height+30)
        table.setMaximumHeight(Height+30)
        if Height >300:
            table.setMinimumHeight(300)
            table.setMaximumHeight(300)
        

    def Fn_Auto_MatName(self):
        if self.MaterialName_Edit.text() == "":
            #tex = self.Texture_Table.cellWidget(0,0).tex 
            #MatName = tex[0] + tex[1] + "_Material"  
            path = self.SelectFolder_Edit.text()
            MatName = path.split("/")[-3]
            self.MaterialName_Edit.setText(MatName)

    def fn_GetTexType (self, name):
        #['diffuse', 'specular', 'roughnes', 'metalicity', 'normal', 'displace', 'other']
        name = name.lower() 
        FindList = [
        ['base_color', "diff", "diffuse", "base", "basecolor"],
        ["metalness", "metal", "metalicity"],
        ["specular", "spec"],
        ['specular_roughness', "rough", "roughnes", "roughness"],
        ["normal", "norm", "nm"],
        ["displace", "dm", "disp"],
        ]

       # index = 6
        Type = "unknown"
        for x in range(len(FindList)):
            for i in range(len(FindList[x])):
                if name.find((FindList[x])[i]) !=-1:
                    #index = x
                    Type = (FindList[x])[0]
                    break
        ##print Type
        ##print self.TexType_List[index]   
        return Type    

    def sortByFourth (self, val): 
        return val[4]

    def Fn_Create_Image_List(self):
        texCount =self.Texture_Table.rowCount()
        ImgCreateList=[]
        ConectedCount =0
        for row in range(texCount):
            if self.Texture_Table.cellWidget(row,0).isChecked():
                Tex = self.Texture_Table.cellWidget(row,1)
                Type = self.Texture_Table.cellWidget(row,2).currentText()
                ColorSpace = self.Texture_Table.cellWidget(row,2).currentText()
                
                Order = self.Texture_Table.cellWidget(row,5).text()

                XXXX=""
                if Tex.tex[2]!="":
                    XXXX= "XXXX"
                #"__" + Type + "__" + 
                ImgName = (Tex.tex[0] + Tex.tex[1] +"_"+XXXX +"_"+
                 Tex.tex[3] +"."+ Tex.tex[4])
                filepath = SelectedFolderPath + "/" + Tex.text()
                filepath = filepath.replace('\\', '/')
                #print filepath
     
                ImgCreateList.append([ImgName, filepath, Type, ColorSpace, int(Order)])
                if Type!="unknown":
                    ConectedCount +=1
        ImgCreateList.sort(key=self.sortByFourth)
        return [ImgCreateList, ConectedCount]

    def Fn_AllGroups_Chk(self):

        GroupCount = self.Groups_Table.rowCount()
        for row in range(GroupCount):
           # print "aaabb"
            if self.allGroups_Chk.isChecked():
                #print "aa"
                self.Groups_Table.cellWidget(row,0).setChecked(1)
            else:
                #print "bb"
                self.Groups_Table.cellWidget(row,0).setChecked(0)

    def Fn_Create_Group_List(self):
        GroupCount = self.Groups_Table.rowCount()
        GroupList=[]
        TypeList = []
        for row in range(GroupCount):
            Type = self.Groups_Table.cellWidget(row,2).currentText()
            if Type not in TypeList and self.Groups_Table.cellWidget(row,0).isChecked():
                TypeList.append(Type)
        #print TypeList

        for itm in TypeList:
            Groups = []
            On = 0
            for row in range(GroupCount):
                if self.Groups_Table.cellWidget(row,0).isChecked() and self.Groups_Table.cellWidget(row,2).currentText() == itm:  
                    Group = self.Groups_Table.cellWidget(row,1).text()
                    Groups.append(Group)
                #print Groups 
            GroupList.append([itm, Groups]) 
        for Gr in GroupList:
            if Gr[1] ==[]:
                GroupList.remove(Gr)
        #print GroupList
        self.Fn_SetSelectGeoL3_Label(GroupList)
        return GroupList

    def Fn_Group_Check_Selector(self):
        try:
            self.Fn_Create_Group_List()
        except:
            pass

    def Fn_Create_Mat_In_Shop(self):
        shop = hou.node("/shop")
        self.Fn_Create_Mat(shop)

    def Fn_Create_Mat_In_Sop(self):
        global SopNode
        if SopNode.type().name() != "arnold_vopnet":
            shop = Fn_Create_SOP_Shopnet(SopNode.parent())
            if self.Groups_Table.rowCount() < 1 or self.DontUseGroups_Chk.isChecked():
                #MatType = self.MatType_ComboBox.currentText()
                MatName = self.MaterialName_Edit.text() + "---" + self.MatType_ComboBox.currentText()
                material = Fn_Create_SOP_MaterialNode(SopNode, 1, "", MatName)
                self.Fn_Create_Mat(shop)
            else:
                GroupList = self.Fn_Create_Group_List()
                if GroupList ==[]:
                    GroupList = [[self.MatType_ComboBox.currentText(), []]]
                node = SopNode
                cnt = 0
                for GroupType in GroupList:

                    Qty = len(GroupList)
                    MatName = self.MaterialName_Edit.text() + "---" + GroupType[0]
                    NodeChk = Fn_NodeChk(node)
                    material = Fn_Create_SOP_MaterialNode(SopNode, 1, GroupType, MatName)
                    color = hou.Color()
                    H = 360/Qty*cnt
                    color.setHSV([H, 0.6, 1.0])
                    cnt+=1
                    material.setColor(color)   
                    
                    self.Fn_Create_Mat(shop, GroupType[0], color)
        else:
            self.Fn_Create_Mat()


    def Fn_Create_Mat(self, shopnet="", MatType = "", color = ""):
        global SopNode
        PosY = 0
        Type =""
        if SopNode != None:
           Type = SopNode.type().name() 

        if Type != "arnold_vopnet" or SopNode == None :
            if MatType =="":
                MatType = self.MatType_ComboBox.currentText()
            if color == "":
                color = hou.Color((0.1, 0.6, 0.1))
            Matname = self.MaterialName_Edit.text() + "---" + MatType
            MaterialNode = shopnet.createNode("arnold_vopnet", Matname)
            Fn_NewNode_Arrange(MaterialNode)
            MaterialNode.setColor(color)   
            OUT_material = hou.node(MaterialNode.path() + "/OUT_material")
            shader = MaterialNode.createNode("standard_surface", "standard_surface")
            OUT_material.setInput(0, shader, 0)
            shader.move(hou.Vector2((-5.0, 0)))
        else:
            MaterialNode = SopNode 
            
            for itm in MaterialNode.children():
                
                if itm.position()[1] < PosY:
                    PosY = itm.position()[1]
                    print PosY
                if itm.type().name() == "arnold::standard_surface":
                    shader = itm
                if itm.name() == "OUT_material":
                    OUT_material = itm
        ImgCreateList = self.Fn_Create_Image_List()[0]
        ConectedCount = self.Fn_Create_Image_List()[1]
        pos = hou.Vector2((-13.0, ConectedCount*1.5/2-1.5+PosY))
        connectedInputs = [] 
       
        for itm in ImgCreateList:
            image = MaterialNode.createNode("image", itm[0])
            image.parm('filename').set(itm[1])
            #print self.ColorSpaceAll_List
            if 'ACES Textures' in self.ColorSpaceAll_List:
                #print itm[3]
                #print itm[3].split(" ")

                ColorFamily = itm[3].split(" ")[0]
                image.parm('color_family').set(ColorFamily)
            image.parm('color_space').set(itm[3])
            image.move(pos) 
            image.parm('ignore_missing_textures').set(1)

            if itm[2] not in connectedInputs:    
                if itm[2]!="unknown"  and MatType != "Sclera":
                    if itm[2]=='normal':
                        norm = MaterialNode.createNode('arnold::normal_map')
                        norm.setPosition(image.position())
                        norm.move(hou.Vector2((4, 0))) 
                        norm.setInput(0, image, 0)
                        shader.setNamedInput('normal', norm, 0)
                    elif itm[2]=='displace':
                        mult = MaterialNode.createNode('arnold::multiply')
                        mult.setPosition(image.position())
                        mult.move(hou.Vector2((8, 0))) 
                        mult.setInput(0, image, 0)
                        mult.parm('input2r').set(0.01)
                        mult.parm('input2g').set(0.01)
                        mult.parm('input2b').set(0.01)
                        OUT_material.setInput(1, mult, 0)
                    elif itm[2]=='base_color' and MatType == "Skin":
                        shader.setNamedInput('subsurface_color', image, 0)
                        shader.parm('subsurface').set(1)
                        shader.parm('subsurface_radiusr').set(0.1)
                        shader.parm('subsurface_radiusg').set(0.035)
                        shader.parm('subsurface_radiusb').set(0.02)
                        shader.parm('subsurface_scale').set(0.01)
                    elif itm[2]=='specular_roughness' and MatType == "Cloth":
                        Range = MaterialNode.createNode('arnold::range')
                        Range.setPosition(image.position())
                        Range.move(hou.Vector2((4, 0))) 
                        Range.setInput(0, image, 0)
                        shader.setNamedInput('sheen_roughness', Range, 0)
                        shader.setNamedInput('specular_roughness', image, 0)
                        
                    
                    elif itm[2]=='base_color' and MatType == "Cloth":
                        shader.setNamedInput('subsurface_color', image, 0)
                        shader.parm('subsurface').set(.2)
                        shader.parm('subsurface_radiusr').set(0.1)
                        shader.parm('subsurface_radiusg').set(0.1)
                        shader.parm('subsurface_radiusb').set(0.1)
                        shader.parm('subsurface_scale').set(0.01)
                        ColorCorrect = MaterialNode.createNode('arnold::color_correct')
                        ColorCorrect.setPosition(image.position())
                        ColorCorrect.move(hou.Vector2((4, 0))) 
                        ColorCorrect.setInput(0, image, 0)
                        ColorCorrect.parm('gamma').set(1.5)
                        ColorCorrect.parm('saturation').set(0.8)
                        shader.setNamedInput('sheen_color', ColorCorrect, 0)
                        shader.setNamedInput('base_color', image, 0)


                    else:
                        shader.setNamedInput(itm[2], image, 0)
                if MatType == "Inner_eye":
                    if itm[2]=='base_color':
                        shader.setNamedInput('subsurface_color', image, 0)
                    shader.parm('subsurface').set(1)
                    shader.parm('subsurface_type').set('diffusion')
                    shader.parm('subsurface_radiusr').set(0.1)
                    shader.parm('subsurface_radiusg').set(0.035)
                    shader.parm('subsurface_radiusb').set(0.02)
                    shader.parm('subsurface_scale').set(0.01)
                if MatType == "Sclera":
                    shader.parm('specular_roughness').set(.01)
                    shader.parm('transmit_aovs').set(1)
                    shader.parm('transmission').set(1)
            #shader.updateParmStates() 
            connectedInputs.append(itm[2])
            pos[1] -= 1.5
           
#    def Fn_AllInputs_Check(self):        
#        
#        if self.allSlots_Chk.isChecked() ==True:
#            #print "self.allSlots_Chk.isChecked()"
#            self.TexType_List=self.StandartSurfInputs
#        else:
#            self.TexType_List=['base_color', 'metalness', 'specular',
#         'specular_roughness', 'normal', 'displace', 'unknown']  
#        self.Fn_Create_TexTable()

    def Fn_SelectFolderButton(self):
        global SelectedFolderPath
        global TexList
        self.Button_CreateSop.setEnabled(0)
        SelectedFolderPath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))   # , options = QFileDialog.DontUseNativeDialog
        #SelectedFolderPath = str(QFileDialog.getOpenFileNames(self, "Select Directory"))   # , options = QFileDialog.DontUseNativeDialog
        #print SelectedFolderPath
        if path.exists(SelectedFolderPath):
            self.Button_CreateSop.setEnabled(1)
            self.SelectFolder_Edit.setText(SelectedFolderPath)
            TexList = self.Fn_Create_TexList()
            #print TexList
            self.Fn_Create_TexTable()

    
    def Fn_AutoMatType(self):
        TypeSet = [
        ['Metal', []], 
        ['Leather',["Leather"]], 
        ["Cloth",["cloth", "Fabric", "rags", ]], 
        ["Skin", ['nail', 'skin', "eye", "eyes", "tongue", "hand", "hands", "face", "teeth", "mouth"]], 
        ["Sclera", ['out_', "outer_", "sclera_", "tear_"]], 
        ["Inner_eye", ["inner", "inner_eye", "eyeball"]]]

        for row in range(self.Groups_Table.rowCount()):
            Name = self.Groups_Table.cellWidget(row,1).text()
            Name = Name.lower() 
            for Type in TypeSet:
                for itm in Type[1]:
                    itm = itm.lower() 
                    if Name.find(itm) !=-1:
                        self.Groups_Table.cellWidget(row,2).setCurrentText(Type[0])
   
   
    def Fn_SelectFolderEdit(self):
        self.Button_CreateSop.setEnabled(0)
        self.Button_Create.setEnabled(0)
        self.Texture_Table.clearSpans()
        self.Texture_Table.setSortingEnabled(0)
        self.Texture_Table.setRowCount(0) 
        self.Fn_Resize_Table(self.Texture_Table)
        global SelectedFolderPath
        global TexList

        SelectedFolderPath = self.SelectFolder_Edit.text()
        #print SelectedFolderPath
        if path.exists(SelectedFolderPath):
            self.Button_CreateSop.setEnabled(1)
            self.Button_Create.setEnabled(1)
            TexList = self.Fn_Create_TexList()
            #print TexList
            self.Fn_Create_TexTable()  
        self.Fn_NoTextures()
 
    def Fn_SetSelectGeoL3_Label(self, grouplist):
        tmp = []
        for gr in grouplist:
            tmp.append(gr[0])
        groups = ', ' .join(tmp)
        cnt = fGreen + str(len(tmp)) + fEnd
        if len(tmp) == 0 or self.DontUseGroups_Chk.isChecked():
            Type = self.MatType_ComboBox.currentText()
            msg = fRed + "Will create 1 material using Material type selector selection: " + fEnd +  fGreen + Type + fEnd
        else:
            msg = "Will create " + cnt + " materials with folowing types: \n" +  fGreen + groups + fEnd
        self.SelectGeoL3_Label.setText(msg)

    def Fn_SelectGeo(self):
        global ObjNode
        global SopNode

        sel = hou.selectedItems()
        #print sel[0].type()
        SopNode = Fn_FindSop(sel[0])
        
        if sel[0].type().name() != "arnold_vopnet":
            ObjNode = SopNode.parent()
            self.SelectGeoL2_Label.setText("materials will be created after " + fGreen + SopNode.name() + fEnd + " node")
            self.Button_CreateSop.setText("Create in Geo")
            self.Button_CreateSop.setFixedWidth(100)
        if sel[0].parent().type().name() == "arnold_vopnet":
            self.SelectGeoL2_Label.setText("Node inside of shader selected. Textures will be added to " + fGreen + sel[0].parent().name() + fEnd + " shader")
            self.Button_CreateSop.setText("Add Textures to Shader")
            self.Button_CreateSop.setFixedWidth(150)
            SopNode = sel[0].parent()
        if sel[0].type().name() == "arnold_vopnet":
            SopNode = sel[0]
            self.SelectGeoL2_Label.setText("Textures will be added to " + fGreen + SopNode.name() + fEnd + " shader")
            self.Button_CreateSop.setText("Add Textures to shader")
            self.Button_CreateSop.setFixedWidth(150)
                
        if SopNode != None:
            self.Groups_Table.clearSpans()
            self.SelectGeo_Label.setText(fGreen + sel[0].name() + fEnd + " selected")
                
            self.Groups_Table.setSortingEnabled(0)
            self.Groups_Table.setRowCount(0)
            groups=[]
            if SopNode != None:
                if SopNode.type().name() != "arnold_vopnet":
                    if self.SGOnly_Chk.isChecked():
                        print "self.SGOnly_Chk.isChecked"
                        groups = [g.name() for g in SopNode.geometry().primGroups() if g.name().find("SG_") != -1 or g.name().find("_SG") != -1]
                    else:
                        groups = [g.name() for g in SopNode.geometry().primGroups()]
                    #print groups
                
                row=0
                self.Groups_Table.setRowCount(len(groups))
                for SG in groups:

                    SG_CheckBox = QCheckBox()
                    SG_CheckBox.setCheckState(QtCore.Qt.Checked)
                    SG_CheckBox.stateChanged.connect(self.Fn_Group_Check_Selector) 
                    
                    self.Groups_Table.setCellWidget(row, 0, SG_CheckBox) 

                    SG_label = QLabel()
                    SG_label.setMargin(3)
                    SG_label.setText(SG)
                    SG_label.setStyleSheet(ToolTipStyle)
                    self.Groups_Table.setCellWidget(row, 1, SG_label) 
                    self.Groups_Table.cellWidget(row,1).setStyleSheet("QLabel {color: #ff0000;}")
                    if SG.find("SG_") != -1 or SG.find("_SG") != -1:
                        self.Groups_Table.cellWidget(row,1).setStyleSheet("QLabel {color: #00ff00;}")

                    MatType_ComboBox = QComboBox()
                    MatType_ComboBox.setStyleSheet(ToolTipStyle)
                    for MatType in self.MatType_List:
                        MatType_ComboBox.addItem(MatType)
                    self.Groups_Table.setCellWidget(row, 2, MatType_ComboBox)
                    MatType_ComboBox.currentIndexChanged.connect(self.Fn_Create_Group_List)
                    
                    row+=1
                    self.Groups_Table.resizeRowsToContents()
                    self.Groups_Table.resizeColumnsToContents()
                    
                self.Fn_AutoMatType()    
            self.Fn_Resize_Table(self.Groups_Table)
            self.Fn_DontUseGroups()
            self.Fn_Create_Group_List()
        else:
            self.Groups_Table.clearSpans()
            self.SelectGeo_Label.setText(fRed + sel[0].name() + fEnd + " is not supported")
            self.SelectGeoL2_Label.setText(fRed + "Select Geo node, Sop node, Arnold shader node or Node inside Arnold Shader" + fEnd)
            self.Fn_Resize_Table(self.Groups_Table)
            self.Fn_DontUseGroups()
            self.Fn_Create_Group_List()



    def Fn_DontUseGroups(self):
        self.Fn_Create_Group_List()
        global SopNode
        if self.DontUseGroups_Chk.isChecked() or SopNode == None:
            self.Groups_Table.setHidden(1)
            self.allGroups_Chk.setHidden(1)
            self.SGOnly_Chk.setHidden(1)
            #self.DontUseGroups_Chk.setEnabled(0)
        else:
            self.Groups_Table.setHidden(0)
            self.allGroups_Chk.setHidden(0)
            self.SGOnly_Chk.setHidden(0)
            #self.DontUseGroups_Chk.setEnabled(1)

    def Fn_MatTypeLabel(self):
        msg = "Material will be created using " + fGreen +self.MatType_ComboBox.currentText() +fEnd + " preset"
        self.MatType_Label.setText(msg)
        self.Fn_Create_Group_List()
                
    def Fn_NoTextures(self):
        
        if self.Texture_Table.rowCount() == 0:
            tmp = 0
        else:
            tmp = 1
        self.MatType_ComboBox.setEnabled(tmp)
        self.MatType_Label.setEnabled(tmp)
        self.Texture_Table.setEnabled(tmp)
        self.MaterialName_Edit.setEnabled(tmp)
        self.AllTexType_ComboBox.setEnabled(tmp)
        self.AllColorSpace_ComboBox.setEnabled(tmp)
        self.AllToken_ComboBox.setEnabled(tmp)



    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)    

        self.setGeometry(600, 500, 300, 100)
        self.setWindowTitle('Create new Material')
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(58, 58, 58, 255))
        self.setPalette(p)

        self.setStyleSheet(hou.qt.styleSheet()) 
        #self.StandartSurfInputs 
        self.TexType_List = ['base', 'base_color', 'diffuse_roughness',
         'metalness', 'specular', 'specular_color', 'specular_roughness', 
         'specular_IOR', 'specular_anisotropy', 'specular_rotation',
         'transmission', 'transmission_color', 'transmission_scatter',
         'transmission_scatter_anisotropy', 'transmission_dispersion',
         'transmission_extra_roughness', 'subsurface', 'subsurface_color',
         'subsurface_radius', 'subsurface_scale', 'subsurface_anisotropy',
         'coat', 'coat_color', 'coat_roughness', 'coat_IOR', 'coat_normal',
         'coat_affect_color', 'coat_affect_roughness', 'thin_film_thickness',
         'thin_film_IOR', 'sheen', 'sheen_color', 'sheen_roughness',
         'emission', 'emission_color', 'opacity', 'normal', 'tangent', 'displace', 'unknown']

        #self.TexType_List=['base_color', 'metalness', 'specular',
        # 'specular_roughness', 'normal', 'displace', 'unknown']      

        self.MatType_List=['Metal', 'Leather', "Cloth",  "Skin", "Sclera", "Inner_eye"]       

        #if self.allSlots_Chk.checkState() ==1:
        #    self.TexType_List=self.StandartSurfInputs

        self.TokenType_List=['<UDIM>', 'Frames', 'None']

        shopnet = hou.node("/shop")
        MaterialNode = shopnet.createNode("arnold_vopnet")
        image = MaterialNode.createNode("image")
        MenuItems = image.parm('color_family').menuItems()
        if "ACES" not in MenuItems:
            self.ColorSpace_List=['sRGB', 'Linear']
            self.ColorSpaceAll_List=['Linear Textures', 'Srgb Textures']
        else:
            self.ColorSpace_List=['Utility - Linear - sRGB', 'Utility - Raw', 'ACES - ACEScg']
            self.ColorSpaceAll_List=[ 'ACES Textures', 'Linear Textures', 'Srgb Textures']
        MaterialNode.destroy()  

#--------------------------------------------------------------------

        self.SelectFolder_Edit = QLineEdit()
        self.SelectFolder_Edit.setStyleSheet(ToolTipStyle)
        self.SelectFolder_Edit.setToolTip("""Input path to folder with textures""") 
        self.SelectFolder_Edit.textChanged.connect(self.Fn_SelectFolderEdit)

        self.Button_SelectFolder = Fn_NewToolButton("Select Folder", 100 ,30)
        self.Button_SelectFolder.pressed.connect(self.Fn_SelectFolderButton)
        self.Button_SelectFolder.setStyleSheet(ToolTipStyle)
        self.Button_SelectFolder.setToolTip("""Select Folder with textures""")

        self.SelectedFolder_Label = QLabel("No texture Folder selected") 
        Fn_CreateLayout("SelectFolder", "H")
        SelectFolder_Layout.addWidget(self.Button_SelectFolder)
        SelectFolder_Layout.addWidget(self.SelectFolder_Edit)
        #electFolder_Layout.addWidget(self.SelectedFolder_Label)
        #SelectFolder_Layout.addStretch(1)
        SelectFolder_Layout.setContentsMargins(0,0,0,0)

        Fn_CreateLayout("MatType", "H")
        self.PreMatType_Label = QLabel("Material Type")

        self.MatType_ComboBox = QComboBox()
        self.MatType_ComboBox.setStyleSheet(ToolTipStyle)
        for Type in self.MatType_List:       
            self.MatType_ComboBox.addItem(Type)
        self.MatType_ComboBox.currentIndexChanged.connect(self.Fn_MatTypeLabel)
        self.MatType_ComboBox.setToolTip("""Set Material Type for material created in 
    /Shop and Materials created in Geo 
    if there are no Shading Groups. 

    Metal, Leather - metalness pipeline.
    Cloth - metalness + sss + sheen.
    Skinn, Inner_Eye - SSS value =1, base color goes to SSS color.
    Sclera - clean translucent material.
     . 
     . 
     . 
     """) 
        
        self.MatType_Label = QLabel()
        MatType_Layout.addWidget(self.PreMatType_Label)
        MatType_Layout.addWidget(self.MatType_ComboBox)
        MatType_Layout.addWidget(self.MatType_Label)
        MatType_Layout.addStretch(1)

        self.Texture_Table = QTableWidget()
        self.Texture_Table.setColumnCount(6)
        self.Texture_Table.setHorizontalHeaderLabels(('Use','Texture name',
                         'Texture type','Colorspace', 'Token'))
        Fn_CreateLayout("Table", "H")
        Table_Layout.addWidget(self.Texture_Table)
        Table_Layout.setContentsMargins(0,0,0,0)
        
        Fn_CreateLayout("Options", "H")
        self.MaterialName_Edit = QLineEdit()
        self.MaterialName_Edit.setStyleSheet(ToolTipStyle)
        self.MaterialName_Edit.setToolTip("""Material will be saved with this name. 
 If left blank - Will Autamaticaly generate name 
 (using folder name of a folder 2 steps higher 
 than texture folder) """) 
        self.MaterialName_Edit.editingFinished.connect(self.Fn_Auto_MatName)  
        MaterialName_Label = QLabel(fGray +"Material Name"+fEnd)
        Fn_CreateLayout("MaterialName", "V")
        #MaterialName_Layout.addStretch(1)
        MaterialName_Layout.addWidget(MaterialName_Label)
        MaterialName_Layout.addWidget(self.MaterialName_Edit)
        MaterialName_Layout.setContentsMargins(0,0,0,0)

        #self.allSlots_Chk = QCheckBox("Show All Tex Types")
        #self.allSlots_Chk.setStyleSheet(ToolTipStyle)
        #self.allSlots_Chk.stateChanged.connect(self.Fn_AllInputs_Check)
        #self.allSlots_Chk.setToolTip("""Show all avaliable shader inputs  
#in "Texture Type" combo boxes.""") 

        self.AllTexType_ComboBox = QComboBox()
        self.AllTexType_ComboBox.setStyleSheet(ToolTipStyle)
       # for Type in self.TexType_List:       
        #    self.AllTexType_ComboBox.addItem(Type)
        self.AllTexType_ComboBox.addItem("unknown")
        self.AllTexType_ComboBox.addItem("Automatic")
        self.AllTexType_ComboBox.setCurrentText("Automatic")
        self.AllTexType_ComboBox.setToolTip("""Set Texture Type for all textures. 
Set "Automatic" to let the script choose for you""") 
        
        self.AllTexType_ComboBox.currentIndexChanged.connect(self.Fn_Change_AllType)        
        AllTexType_Label = QLabel(fGray +"All Types"+fEnd)    
        Fn_CreateLayout("AllTexType", "V")
        #AllTexType_Layout.addStretch(1)
        #AllTexType_Layout.addWidget(self.allSlots_Chk)
        AllTexType_Layout.addWidget(AllTexType_Label)
        AllTexType_Layout.addWidget(self.AllTexType_ComboBox)
        AllTexType_Layout.setContentsMargins(0,0,0,0)

        self.AllColorSpace_ComboBox = QComboBox()
        self.AllColorSpace_ComboBox.setStyleSheet(ToolTipStyle)
        for ColorSpace in self.ColorSpaceAll_List:
            self.AllColorSpace_ComboBox.addItem(ColorSpace)
        self.AllColorSpace_ComboBox.setToolTip("""Set ColorSpace for all textures. 
Set "Automatic" to let the script choose for you""") 
        self.AllColorSpace_ComboBox.currentIndexChanged.connect(self.Fn_Change_AllColorSpaceCombo)
        AllColorSpace_Label = QLabel(fGray +"All ColorSpaces"+fEnd)    
        Fn_CreateLayout("AllColorSpace", "V")
        #AllColorSpace_Layout.addStretch(1)
        AllColorSpace_Layout.addWidget(AllColorSpace_Label)
        AllColorSpace_Layout.addWidget(self.AllColorSpace_ComboBox)
        AllColorSpace_Layout.setContentsMargins(0,0,0,0)

        self.AllToken_ComboBox = QComboBox()
        self.AllToken_ComboBox.setStyleSheet(ToolTipStyle)
        self.AllToken_ComboBox.setToolTip("""Set Token for all textures. 
Set "Automatic" to let the script choose for you""") 
        for Token in self.TokenType_List:
            self.AllToken_ComboBox.addItem(Token)
        self.AllToken_ComboBox.addItem("Automatic")
        self.AllToken_ComboBox.setCurrentText("Automatic")
        self.AllToken_ComboBox.currentIndexChanged.connect(self.Fn_Change_AllTokenCombo)
        AllToken_Label = QLabel(fGray +"All Tokens"+fEnd)    
        Fn_CreateLayout("AllToken", "V")
        #AllToken_Layout.addStretch(1)
        AllToken_Layout.addWidget(AllToken_Label)
        AllToken_Layout.addWidget(self.AllToken_ComboBox)
        AllToken_Layout.setContentsMargins(0,0,0,0)

        Options_Layout.addWidget(MaterialName_Wgt)
        Options_Layout.addWidget(AllTexType_Wgt)
        Options_Layout.addWidget(AllColorSpace_Wgt)
        Options_Layout.addWidget(AllToken_Wgt)

        Fn_CreateLayout("Buttons", "H")
        
        self.Button_Create = Fn_NewToolButton("Create in /Shop", 100 ,30)
        self.Button_Create.pressed.connect(self.Fn_Create_Mat_In_Shop)
        self.Button_Create.setStyleSheet(ToolTipStyle)
        self.Button_Create.setToolTip("""Create Material. Will create arnold shader network containing selected textures""") 
        self.Button_Create.setEnabled(0) 

        Button_Cancel = Fn_NewToolButton("Close", 100 ,30)
        Button_Cancel.setStyleSheet(ToolTipStyle)
        Button_Cancel.setToolTip("""Cancel.""") 
        Button_Cancel.pressed.connect(self.Fn_Exit)
        Buttons_Layout.addStretch(1)
        
        Buttons_Layout.addWidget(self.Button_Create)
        
        Buttons_Layout.addWidget(Button_Cancel)
        Buttons_Layout.setContentsMargins(0,0,0,0)

        Fn_CreateLayout("MainL", "V")
        
        MainL_Layout.addWidget(SelectFolder_Wgt)
        MainL_Layout.addWidget(MatType_Wgt)
        MainL_Layout.addWidget(Table_Wgt)
        MainL_Layout.addWidget(Options_Wgt)
        MainL_Layout.addWidget(Buttons_Wgt)

        self.SelectGeoL0_Label = QLabel("Select Geo node or Sop Node to create Material nodes, Shopnet inside Geometry, and arnold shaders with textures") 
        self.SelectGeoL0_Label.setWordWrap(1)

        Fn_CreateLayout("SelectGeo", "H")
        self.Button_SelectGeo = Fn_NewToolButton("Select Geo", 100 ,30)
        self.Button_SelectGeo.pressed.connect(self.Fn_SelectGeo)
        self.Button_SelectGeo.setStyleSheet(ToolTipStyle)
        self.Button_SelectGeo.setToolTip("""Select Geo node or Sop Node - to create Material nodes,
 Shopnet inside Geometry, and arnold shaders with textures inside created shopnet
 Select Arnold Shader or Node inside it  - to Add textures to the existing shader""") 


        self.SelectGeo_Label = QLabel("Nothing selected") 
        self.SelectGeoL2_Label = QLabel("") 
        self.SelectGeo_Label.setWordWrap(1)
        self.SelectGeoL2_Label.setWordWrap(1)

        #Fn_CreateLayout("GroupsChk", "H")
        

        
        #GroupsChk_Layout.addWidget(self.SGOnly_Chk)
        #GroupsChk_Layout.addWidget(self.DontUseGroups_Chk)

        SelectGeo_Layout.addWidget(self.Button_SelectGeo)
        SelectGeo_Layout.addWidget(self.SelectGeo_Label)
        
        SelectGeo_Layout.addStretch(1)

        
#--------------------------------------------------------


        self.Groups_Table = QTableWidget()
        self.Groups_Table.setColumnCount(3)
        self.Groups_Table.setHorizontalHeaderLabels(('Use',
                         'GroupName', "Mat Type"))
        Fn_CreateLayout("GroupsTable", "H","Fixed","Fixed")
        self.Groups_Table.setMaximumHeight(200)
        GroupsTable_Layout.addWidget(self.Groups_Table)
        GroupsTable_Layout.setContentsMargins(0,0,0,0)

        Fn_CreateLayout("SetAllGroups", "H")
        self.allGroups_Chk = QCheckBox("Switch all groups")
        self.allGroups_Chk.setStyleSheet(ToolTipStyle)
        self.allGroups_Chk.stateChanged.connect(self.Fn_AllGroups_Chk)
        self.allGroups_Chk.setToolTip("""Turn all groups On/Off.""") 
        self.allGroups_Chk.setChecked(1)

        self.SGOnly_Chk = QCheckBox("SG Only")
        self.SGOnly_Chk.setStyleSheet(ToolTipStyle)
        self.SGOnly_Chk.setChecked(1)
        self.SGOnly_Chk.stateChanged.connect(self.Fn_SelectGeo)
        self.SGOnly_Chk.setToolTip("""When enabled uses only Groups with SG_ in its name (aka Shading Groups)""") 

        SetAllGroups_Layout.addWidget(self.allGroups_Chk)
        SetAllGroups_Layout.addWidget(self.SGOnly_Chk)

        Fn_CreateLayout("ButtonsGroups", "H")
        
        self.DontUseGroups_Chk = QCheckBox("Don't use Groups")
        self.DontUseGroups_Chk.setStyleSheet(ToolTipStyle)
        self.DontUseGroups_Chk.setChecked(0)
        self.DontUseGroups_Chk.stateChanged.connect(self.Fn_DontUseGroups)
        self.DontUseGroups_Chk.setToolTip("""When enabled ignores all groups, and will create single material
         based on Material Type Selector to the left""") 

        self.Button_CreateSop = Fn_NewToolButton("Create in Geo", 100 ,30)
        self.Button_CreateSop.pressed.connect(self.Fn_Create_Mat_In_Sop)
        self.Button_CreateSop.setStyleSheet(ToolTipStyle)
        self.Button_CreateSop.setToolTip("""Create Material. Will create arnold shader network containing selected textures""") 
        self.Button_CreateSop.setEnabled(0) 
        self.SelectGeoL3_Label = QLabel("No Geo selected_line2") 
        self.SelectGeoL3_Label.setWordWrap(1)
        ButtonsGroups_Layout.addWidget(self.DontUseGroups_Chk)

        ButtonsGroups_Layout.addWidget(self.Button_CreateSop)

        Fn_CreateLayout("MainR", "V")
        #MainR_Layout.addWidget(self.SelectGeoL0_Label)
        MainR_Layout.addWidget(SelectGeo_Wgt)
        MainR_Layout.addWidget(self.SelectGeoL2_Label)
        #MainR_Layout.addWidget(GroupsChk_Wgt)
        MainR_Layout.addWidget(GroupsTable_Wgt)
        MainR_Layout.addWidget(SetAllGroups_Wgt)
        MainR_Layout.addWidget(self.SelectGeoL3_Label)
        MainR_Layout.addWidget(ButtonsGroups_Wgt)
        MainR_Layout.addStretch(1)
        MainR_Layout.addStretch(1)
     

        Fn_CreateLayout("Main", "H","Fixed","Fixed")
        Main_Layout.addWidget(MainL_Wgt)
        Main_Layout.addWidget(MainR_Wgt)

        self.setLayout(Main_Layout)
        self.Fn_DontUseGroups()
        self.Fn_MatTypeLabel()
        self.Fn_NoTextures()
        #self.Fn_SetAuto_TexTable()

try:    
    os.CreateMaterialDialog.close() 
except:    
    pass
os.CreateMaterialDialog = Class_Create_Material_Dialog()
os.CreateMaterialDialog.show()
#if os.CreateMaterialDialog.TexList ==None:
 #   os.CreateMaterialDialog.close()