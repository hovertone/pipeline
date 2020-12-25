import nuke
import nukescripts


def separateChannels(ask, complete):
    if nuke.selectedNodes():
        nReadNode = nuke.selectedNode()    
        
        # Tests to guarantee that it is a ReadNode   
        if nReadNode.Class() == 'Read':            

            # creates a LayerContactSheet
            if complete== 'Y':
                lcsNode = nuke.nodes.LayerContactSheet( showLayerNames=True, postage_stamp=True, inputs=[nReadNode] )    
        
            readLayers = list(set(chan.split('.')[0] for chan in nReadNode.channels() ) )  

            totalItems= len(readLayers)
            iCnt = 0
            iCntDEL = 0
   
            #print readLayers
            for layer in readLayers:
                #break

                # creates a shuffle node to separate the channel
                layerName = layer
                if ask=='Y':
                    #Counter
                    iCnt = iCnt + 1

                    layerName = nuke.getInput('Layer %d de %d \n Type the LayerName you want in shuffle label: \n (type DEL to delete the pass from the output) ' % (iCnt, totalItems), layerName)
                    if layerName == 'DEL':
                        iCntDEL = iCntDEL + 1
                        continue

                shfNode = nuke.nodes.Shuffle(inputs=[nReadNode], postage_stamp=True) 
                shfNode['in'].setValue(layer)

                shfNode['label'].setValue(layerName)

                if complete == 'Y':
                    # creates a curve tool to calculate the autocrop data
                    crvNode = nuke.nodes.CurveTool(inputs=[shfNode], operation='Auto Crop') 
                    crvNode['ROI'].setValue( [0, 0, nReadNode.width(), nReadNode.height()] )                
                    nuke.execute( crvNode, nReadNode.knob('first').value(), nReadNode.knob('last').value() )
    
                    # creates a crop tool to crop based on curve tool crop data calculation
                    crpNode = nuke.nodes.Crop(inputs=[crvNode]) 
                    crpNode.knob('box').copyAnimations( crvNode.knob('autocropdata').animations() )
    
                    # creates a diskcache node to avoid processing the data every change on the remaining tree
                    dscNode = nuke.nodes.DiskCache(inputs=[crpNode]) 

                #break
            nuke.scriptSave("")

            if ask == 'Y':
                nuke.message('Layers Separation completed successfully! \n%d Layers processed \n %d were deleted by user decision' % (totalItems, iCntDEL) )  
            else:
                nuke.message('Layers Separation completed successfully! \n%d Layers processed.' % totalItems)          
        else: # If it is not a ReadNode, show an information message
            nuke.message('You must select a ReadNode for the Pass Separator to work.')
    else:
        nuke.message('You must select a ReadNode for the Pass Separator to work.')


class passSepPanel(nukescripts.panels.PythonPanel):
 
    def __init__(self, name):
        nukescripts.panels.PythonPanel.__init__(self, name)
#=================
        #self.ask = 'N'
        #self.complete='Y'

        self.addKnob(nuke.Text_Knob("DO NOT ASK Layers Name:"))
 
        newline = nuke.Text_Knob("")
        newline.setVisible(False)
 
        # btn01 = NA SHUFFLE ONLY
        self.btn01 = nuke.PyScript_Knob("btn01", "Shuffle Only", "pass_sep.separateChannels(\"N\", \"N\")")
        self.addKnob(self.btn01)

        # btn02 = NA COMPLETE
        self.btn02 = nuke.PyScript_Knob("btn02", "Complete", "pass_sep.separateChannels(\"N\", \"Y\")")
        self.addKnob(self.btn02)
        self.addKnob(newline)

        self.addKnob(nuke.Text_Knob("ASK Layers Name:"))

        # btn03 = A SHUFFLE ONLY
        self.btn03 = nuke.PyScript_Knob("btn03", "Shuffle Only", "pass_sep.separateChannels(\"Y\", \"N\")")
        self.addKnob(self.btn03)

        # btn04 = A COMPLETE
        self.btn04 = nuke.PyScript_Knob("btn04", "Complete", "pass_sep.separateChannels(\"Y\", \"Y\")")
        self.addKnob(self.btn04)
 
#========== show up script run seperately
def callPassSep():
    panel = None
    global panel
    if not panel:
        panel = passSepPanel("Pass Separator")
    panel.show()
