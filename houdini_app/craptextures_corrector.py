import os, sys, time, shutil , subprocess

os.environ[  'OCIO'] = "X:/app/win/Pipeline/aces_1.0.3/config.ocio"
itool = "X:/app/win/Pipeline/p_utils/oiio/oiiotool.exe"


try :
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

except Exception as e :
    from PySide.QtGui import *
    from PySide.QtCore import *

def GetFileLsFromDirPath ( dirPath, allowedExts = None, mask = None) :
    files = []
    if os.path.exists(dirPath) :
        for f in os.listdir(dirPath) :
            if os.path.isfile(os.path.join(dirPath, f)) :
                if f. find (".")==-1:
                    continue
                bs,ext= f.rsplit('.',1)
                if allowedExts != None and ext not in allowedExts :
                    continue
                if mask != None and GetMaskedFl(bs) != mask :
                    continue
                files .append((bs,ext))
    return files




def GetColorSpacesLs () :
    itool_ =  itool # "//vpstorage.plarium.local/visual/00_Development/oiio/oiiotool.exe"
    args = " ".join((itool_, '--help'))
    retTxt = subprocess.check_output(args)
    stTok = "Known color spaces: "
    enTok = "Known displays: "
    retTxt = retTxt[retTxt.find(stTok) + len(stTok):]
    retTxt = retTxt[:retTxt.find(enTok)]
    retTxt = retTxt .replace( " (linear)", "" ) # fix for ocio name
    spacesLs = [sp.replace("\"", "").strip() for sp in retTxt.split(",")]
    return spacesLs

spacesLs = GetColorSpacesLs()



allowedExtsLs =  ('exr','png','tif','tiff','jpg','jpeg') #,'tga')

targetFormatsLs = {'exr 16-bit': ('exr','half'),
                   'exr 32-bit':('exr','float'),
                    'exr 1ch 32-bit':('exr','float'),
                    'exr 1ch 16-bit':('exr','half'),
                   'png':('png','uint8'),
                   'tif':('tif','uint8'),
                   'jpg': ('jpg','uint8')
                    #,  'tga' :('tga,uint8')
                   }

typesMapping =   {
'base_color' : ['base_color', "diff", "diffuse", "base", "basecolor"],
'metalness':["metalness", "metal", "metalicity"] ,
'specular':["specular", "spec"],
'specular_roughness' :['specular_roughness', "rough", "roughnes", "roughness"] ,
'normal':["normal", "norm", "nm" ],
'displace':["displace", "dm", "disp" , "height"],
'height':["height"],
'emissive' : ["emissive"]
}


class Sequence :
    toktype_invalid = 0
    toktype_4dgt = 1 # final numeration
    toktype_udim = 2 # requires conversion to 4dgt

    def __init__(self , ext,  stdtype, maskedname , toktype ):
        self.ext =ext
        self.type =stdtype
        self.maskedname =maskedname
        self.toktype = toktype


def GetLikelyTxType(fl) :
    likelyTxType = 'base_color'
    for validTypeKey in typesMapping:
        for crapType in typesMapping[validTypeKey]:  # search for aliases
            if fl.lower().find(crapType) > -1:  # type is ok
                likelyTxType = validTypeKey
                break
    return likelyTxType


def GetMaskedFl (fl) :
    return   ''.join("*" if c.isdigit() else c for c in fl)


def GetNumtokType (fl) :
    maskedFl = "?" + GetMaskedFl(fl) + "?"
    # check fo 4 digits at the end
    idx = maskedFl.rfind("****")
    #if idx > -1 and maskedFl[idx - 1] != "*" and maskedFl[idx + 4] != "*":
    if idx > -1  and maskedFl[idx + 4] != "*":
        #tpsGrpsFinal.setdefault(likelyTxType, set()).add(maskedFl.strip("?"))
        return Sequence.toktype_4dgt, maskedFl.strip("?"), fl [idx-1:idx-1+4]

    # no 4 digits, lets try to find u*_v* pattern
    idx = maskedFl.rfind("u*_v*")
    if idx > -1:
        #tpsGrpsUV.setdefault(likelyTxType, set()).add(maskedFl.strip("?"))
        return  Sequence .toktype_udim,  maskedFl.strip("?"), fl [idx-1:idx-1+5]

    # nothing valid found
    #invalidGrps.add(''.join("*" if c.isdigit() else c for c in fl))
    return Sequence .toktype_invalid,  maskedFl.strip("?"), "_"


def ConvertUDIMto4dgt (origName, uOffset,vOffset  ):

    # get wrong name part
    uvStartPos = origName.rfind('u')
    uvVals = origName [uvStartPos :]

    # parse u and v values
    it = 1
    uValStr = ""
    while True:
        currChar = uvVals[it]
        if currChar == u'_':
            it = it+2
            break
        uValStr += uvVals[it]
        it = it+1

    vValStr = ""
    while True:
        if it == len(uvVals):
            break

        vValStr += uvVals[it]
        it = it+1

    # result numeric values of u and v
    uVal = int (uValStr)-uOffset
    vVal = int (vValStr)-vOffset

    # target final name
    newName = origName[:uvStartPos] + str(1001 + uVal + (10 * vVal))
    return newName





def GetSqLsFromDirPath (  dirPath, allowedExts  ) :
    flDataLs = GetFileLsFromDirPath (dirPath ,allowedExts)
    extGrps = dict()
    for flData in flDataLs :
        extGrps .setdefault (flData [1] ,  []) .append( flData[0])

    sqLs = dict ()

    for ext  in extGrps :
        flLs = extGrps [ext]
        tpsGrpsFinal = dict() # no need to resolve num
        tpsGrpsUV = dict () # convert udim to 4 digit num
        invalidGrps =  set () # unrecognized

        # loop over files with given extension
        for fl in flLs :

            # get txtype
            likelyTxType = GetLikelyTxType (fl)

            # get num type
            toktype, maskedFl, numtok = GetNumtokType (fl)
            if toktype == Sequence .toktype_udim :
                tpsGrpsUV.setdefault(likelyTxType, set()).add(maskedFl)
            elif toktype == Sequence .toktype_4dgt :
                tpsGrpsFinal.setdefault(likelyTxType, set()).add(maskedFl)
            elif toktype == Sequence .toktype_invalid :
                invalidGrps.add(maskedFl)
            else:
                assert  0

        #   ======================

        # collect all 4 digit
        for stdTypeKey in tpsGrpsFinal :
            maskedSet = tpsGrpsFinal[stdTypeKey]
            for mskFl in maskedSet :
                sq = Sequence (ext, stdTypeKey, mskFl , Sequence .toktype_4dgt )
                sqLs[mskFl + '.' + ext] = sq

        # all udims
        for stdTypeKey in tpsGrpsUV :
            maskedSet = tpsGrpsUV[stdTypeKey]
            for mskFl in maskedSet:
                sq = Sequence(ext, stdTypeKey, mskFl, Sequence.toktype_udim)
                sqLs[mskFl+'.'+ext]=sq

        # invalids
        for fl in invalidGrps :
            sq = Sequence (ext,"UNRECOGNIZED_TYPE",fl, Sequence .toktype_invalid)
            sqLs[fl+'.'+ext]=sq
    return sqLs


class Manager (QObject) :
    sig_dirchanged = Signal ()
    sig_assnamechanged = Signal ()

    def __init__(self ):
        QObject .__init__(self )
        self. srcpath = ""
        self.dstpath_ = ""
        self .assnm = "USERASS"
        self. validImgSqLs = []
        self. unrecImgSqLs= []
        self.inpl = False

    def GetDstPath (self):
        if self .inpl :  return self. srcpath #+ "/__txconv_backup"
        else :   return self. dstpath_

    def GetBackupPath (self) :
        return self. srcpath  + "/__txconv_backup"



    def GetValidSqLs (self) :
        return self.validImgSqLs

    def GetAssname (self) :
        return self. assnm

    def SetAssname (self, assnm) :
        self. assnm = assnm
        self.sig_assnamechanged .emit ()

    def SetSourceDir (self, src  ) :
        if self. srcpath ==src:
            return

        self.validImgSqLs = []
        self.unrecImgSqLs = []

        if os .path .exists(src)  and  self. srcpath !=src:
            self.validImgSqLs = GetSqLsFromDirPath ( src, allowedExtsLs ) # fetch images

        self.srcpath = src

        # are we under  ftrack ?
        fldrs = self. srcpath .replace ("\\","/") .split("/")
        if len(fldrs) > 1 and  GetMaskedFl (fldrs [-1] ) == "v***" :
            self.assnm = fldrs[-2]
            self.sig_assnamechanged .emit ()
        self. sig_dirchanged .emit()

    def SetDstDir (self, dst ) :
        self.dstpath_ = dst

        # are we under  ftrack ?
        fldrs = self.dstpath_.replace("\\", "/").split("/")
        if len(fldrs) > 1 and  GetMaskedFl (fldrs [-1] ) == "v***" :
            self.assnm = fldrs[-2]
            self.sig_assnamechanged .emit ()


    def SetInplace (self, state ) :
        self. inpl = state
    def IsInplace (self) :
        return self.inpl


class HeaderRow (QWidget) :
    _0w = 150
    _1w = 200
    _2w = 0
    _3w = 120
    _4w = 85
    _5w = 60
    _6w = 60


    def __init__(self):
        QWidget .__init__(self)
        self.lbl_0 = QLabel("Source name")
        self.lbl_1 = QLabel("Color space")
        self.lbl_2 = QLabel("Fit")
        self.lbl_3 = QLabel("Target type")
        self.lbl_4 = QLabel("Target format")
        self.lbl_5 = QLabel("Preview")
        self.lbl_6  = QLabel(" ")

        self.lbl_0.setMinimumWidth(HeaderRow._0w)
        self.lbl_1.setFixedWidth(HeaderRow._1w)
        self.lbl_2.setFixedWidth(HeaderRow._2w)
        self.lbl_3.setFixedWidth(HeaderRow._3w)
        self.lbl_4 .setFixedWidth(HeaderRow._4w)
        self.lbl_5 .setMinimumWidth(HeaderRow._5w)
        self.lbl_6.setFixedWidth(HeaderRow._6w)

        lay_root = QHBoxLayout()
        lay_root.addWidget(self.lbl_0)
        lay_root.addWidget(self.lbl_1)
        lay_root.addWidget(self.lbl_2)
        lay_root.addWidget(self.lbl_3)
        lay_root.addWidget(self.lbl_4)
        lay_root.addWidget(self.lbl_5)
        lay_root.addWidget(self.lbl_6)

        rm = 4; lay_root.setContentsMargins(rm, rm, rm, rm);  lay_root.setSpacing(rm)
        self.setLayout(lay_root)



class ImageRow (QWidget):
    def __init__(self  , sq, man ):
        QWidget .__init__(self)

        self.sq = sq
        self.man = man

        self.lbl_srcname = QLabel (sq.maskedname + "." + sq.ext  )
        self.cmbx_colorspace = QComboBox()
        self.chbx_fit = QCheckBox ()
        self.cmbx_ext = QComboBox()
        self.lbl_dstname = QLabel ()
        self.pbtn_do = QPushButton("Convert")


        self.cmbx_txtype = QComboBox ()
        self.cmbx_txtype .setEditable(True )
        for stdTypeKey in typesMapping:
            self.cmbx_txtype.addItem(stdTypeKey, stdTypeKey)

        self. cmbx_txtype .setCurrentIndex( self.cmbx_txtype .findText(  sq.type ) )    # set to most likely type
        self.cmbx_txtype.currentIndexChanged.connect( self.UpdateTargetName , Qt.QueuedConnection)
        self.cmbx_txtype .editTextChanged .connect ( self.UpdateTargetName )



        # color spaces
        self.cmbx_colorspace.addItem("as is", "as is")
        for sp in spacesLs:
            self.cmbx_colorspace.addItem(sp, sp)



        # fill in allowed exts
        self.cmbx_ext .addItem("as is", (sq.ext,"n/a"))
        for key in targetFormatsLs:
            self.cmbx_ext.addItem(key, targetFormatsLs[key])

        self.cmbx_ext .setCurrentIndex(0)




        #  ====
        lay_root = QHBoxLayout ()

        self.lbl_srcname .setMinimumWidth( HeaderRow._0w)
        self.cmbx_colorspace.setFixedWidth(HeaderRow._1w)
        self.chbx_fit.setFixedWidth(HeaderRow._2w)
        self.cmbx_txtype.setFixedWidth(HeaderRow._3w)
        self.cmbx_ext.setFixedWidth(HeaderRow._4w)
        self.lbl_dstname.setMinimumWidth(HeaderRow._5w)
        self.pbtn_do.setFixedWidth(HeaderRow._6w)


        lay_root .addWidget(self.lbl_srcname)
        lay_root .addWidget(self.cmbx_colorspace)
        lay_root.addWidget(self.chbx_fit)
        lay_root .addWidget(self.cmbx_txtype)

        lay_root.addWidget(self.cmbx_ext)
        lay_root .addWidget(self.lbl_dstname)
        lay_root.addWidget(self.pbtn_do )


        rm = 4; lay_root.setContentsMargins(rm, rm, rm, rm);  lay_root.setSpacing(rm)
        self.setLayout(lay_root)


        self.cmbx_ext .currentIndexChanged .connect  ( self .UpdateTargetName)
        self.pbtn_do .released .connect (self.DoConversion )

        self. UpdateTargetName( )



    def UpdateTargetName (self  ) :
        #if self.sq.toktype == Sequence .toktype_invalid :
        #    self.lbl_dstname.setText ("N/A")
        #    return

        txtype = self.cmbx_txtype .currentText ()

        # check if we have such type already


        assName =  self. man.GetAssname()
        dstExt = self.cmbx_ext .itemData( self.cmbx_ext .currentIndex()) [0]
        self. lbl_dstname .setText( txtype + "_" + assName + "." + "####" + "." + dstExt)







    def DoConversion (self) :
        if os.path.exists( self.man .GetDstPath()  ) == False :
            if QDir ().mkpath(self.man .GetDstPath() ) == False :
                QMessageBox .warning(None, "Error", "Unable to create the specified directory: " + self.man .GetDstPath() )
                return
        if self.man .IsInplace() and  QDir().mkpath(self.man .GetBackupPath() )  == False :
            QMessageBox.warning(None, "Error", "Unable to create backup directory "  )
            return

        flLs = GetFileLsFromDirPath (self .man .srcpath,( self.sq. ext,) ,self.sq.maskedname ) # only get with the original extension


        pbar = QProgressBar ()
        pbar .setMinimum(0)
        pbar.setMaximum( len(flLs ))
        pbar.show()
        pbar .setTextVisible(False)
        QApplication.processEvents()


        for idx, flData in enumerate( flLs) :
            fl, ext = flData[0],  flData[1]

            # now gather a new name
            txtype = self.cmbx_txtype.currentText()
            assName = self.man.GetAssname()
            extTpl = self.cmbx_ext .itemData( self.cmbx_ext .currentIndex())  # self.sq.ext
            lblExt, dstExt, bitdepth = self.cmbx_ext .currentText() , extTpl [0], extTpl[1]

            # convert udim if any
            unused1, unused2, num = GetNumtokType (fl)
            if self.sq .toktype == Sequence .toktype_udim :
                num= ConvertUDIMto4dgt (num, 1, 1)


            resName = txtype + "_" + assName + "." + num + "." + dstExt
            resFullPath = self.man .GetDstPath() + "/" + resName
            origFullPath = self.man .srcpath  + "/" + fl + "." + ext
            backupFullPath = self.man.GetBackupPath() + "/" + resName

            if self.man .IsInplace ():  print origFullPath, "convert inplace and move src to:", backupFullPath
            else: print origFullPath, "copy to:", resFullPath

            executable = itool
            colorspace = ""
            if self .cmbx_colorspace .currentText() != "as is":
                colorspace =  "--colorconvert \""+self .cmbx_colorspace .currentText()+"\" \"ACES - ACEScg\""

            if ext  == dstExt and lblExt != 'exr 1ch 32-bit' and lblExt != 'exr 1ch 16-bit' and colorspace =="" :
                if origFullPath !=  resFullPath:
                    shutil.copyfile(origFullPath, resFullPath)
            else:
                origFullPath = "\""  + origFullPath + "\""
                resFullPath = "\""  + resFullPath + "\""
                if  lblExt == 'exr 1ch 32-bit' : # hacky, but hopefully no more requirements here

                    args = " ".join((executable, origFullPath, colorspace , '-d float --ch 0 -o',resFullPath))
                    print ("###", args)
                    process = subprocess.Popen(args)
                    process.wait()
                    print process.returncode
                elif   lblExt == 'exr 1ch 16-bit' :

                    args = " ".join((executable, origFullPath, colorspace,'-d half --ch 0 -o', resFullPath))
                    print ("###", args)
                    process = subprocess.Popen(args)
                    process.wait()
                    print process.returncode
                else:

                    outdepth = ""
                    if bitdepth != "n/a":
                        outdepth =  "-d " +  bitdepth
                    args = " ".join((executable, origFullPath, colorspace, outdepth, " -o" , resFullPath))
                    print ("###", args)
                    process = subprocess.Popen(args)
                    process.wait()
                    print process.returncode

            if self.man .IsInplace () :
                shutil .move(origFullPath, backupFullPath)
                self.pbtn_do .setEnabled(False )

            pbar.setValue(idx+1)
            QApplication .processEvents()
            if  pbar .isVisible() == False :
                return False

        return True





class ImgTable (QListWidget) :
    def __init__(self , man):
        QListWidget .__init__(self)

        self.setMouseTracking(True )
        self.viewport().installEventFilter(self)

        self.man = man
        self .viewport() .setAutoFillBackground ( False )

        # add header
        hdrow = HeaderRow ()
        hd = QListWidgetItem()
        hd.setSizeHint(QSize(80, 30))
        self.addItem(hd)
        self.setItemWidget(hd, hdrow)

        rm = 0; self.setContentsMargins(rm, rm, rm, rm) ;self.setSpacing(rm)

        self.man .sig_dirchanged .connect ( self. Refetch)
        self.man .sig_assnamechanged   .connect ( self. UpdateAssName )
        self.Refetch ()

    def UpdateAssName (self ) :
        for idx in range( 1,self.count()  ) :
            self.itemWidget(  self.item(idx)  )   .UpdateTargetName   ( )

    def ConvertAll (self):
        for idx in range( 1,self.count()  ) :
            if self.itemWidget(  self.item(idx)  )   .DoConversion   ( ) == False :
                return

    def Refetch (self) :
        while self .count() > 1 :
            self.takeItem(1)

        sqLs = self.man .GetValidSqLs ()
        for sqMskNameKey in sqLs:
            imgrow = ImageRow(sqLs[sqMskNameKey] , self.man )

            item = QListWidgetItem()
            item.setSizeHint(QSize(80, 30))
            self.addItem(item)
            self.setItemWidget(item, imgrow)







class MainWidnow (  QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setMouseTracking(True)

        self.man = Manager ()

        #self.lbl_srcdir = QLabel("source dir")
        #self.lbl_dstdir = QLabel("target dir")
        self.led_srcdir = QLineEdit ("<source dir>")
        self.led_dstdir = QLineEdit ("<destination dir>")
        self.pbtn_srcdir = QPushButton ("browse")
        self.pbtn_dstdir = QPushButton ("browse")
        self.chbx_inplace = QCheckBox ("Inplace rename with backup")
        #self.chbx_inplace .setEnabled(False )

        self.lbl_assname = QLabel("asset name")
        self.led_assname = QLineEdit ( self.man .assnm)

        self.tbl = ImgTable (self.man )
        self.pbtn_do = QPushButton ("Convert All")

        lay_src = QHBoxLayout()
        #lay_src.addWidget(self.lbl_srcdir)
        lay_src .addWidget(self.led_srcdir)
        lay_src.addWidget(self.pbtn_srcdir)
        lay_dst = QHBoxLayout()
        #lay_dst.addWidget(self.lbl_dstdir)
        lay_dst .addWidget(self.led_dstdir)
        lay_dst.addWidget(self.pbtn_dstdir)

        lay_assname = QHBoxLayout ()
        lay_assname .addWidget(self.lbl_assname)
        lay_assname .addWidget(self.led_assname)

        lay_root = QVBoxLayout ()
        lay_root .addLayout(lay_src)
        lay_root .addLayout(lay_dst)
        lay_root.addLayout( lay_assname)
        lay_root .addWidget( self.chbx_inplace )
        lay_root .addWidget(self.tbl)
        lay_root .addWidget(self.pbtn_do)

        rm = 4; lay_root .setContentsMargins(rm,rm,rm,rm) ; lay_root.setSpacing(rm)
        self.setLayout(lay_root)

        # hacks, need to be refactor to pure MV

        self.pbtn_srcdir . released .connect (self._OnSrcPressed)
        self.pbtn_dstdir.released.connect(self._OnDstPressed)

        self.led_assname .textChanged .connect (self ._OnAssnmChanged  )
        self .led_srcdir .textChanged .connect( self ._OnDirChanged   )
        self.led_dstdir .textChanged .connect ( self. _OnDirChanged )
        self.pbtn_do .released .connect (self ._OnConvertAll)


        self.man .sig_assnamechanged .connect ( lambda : self.led_assname .setText(self.man .GetAssname()), Qt.QueuedConnection )
        self. chbx_inplace .stateChanged .connect ( self._OnInplChanged )

        self.resize(900, 600)


        self.led_srcdir .setParent(self)
        self.led_dstdir .setParent(self)



    def _OnInplChanged (self , newstate ) :
        self .led_dstdir .setEnabled(not bool(newstate))
        self.man .SetInplace ( bool(newstate) )





    def _OnSrcPressed (self) :
        dirpath = QFileDialog .getExistingDirectory(self, "Browse source", self.led_srcdir .text()  )
        if dirpath and  os.path.exists( dirpath)  :
            dirpath  = dirpath .replace("\\","/")
            self.led_srcdir .setText(dirpath )
            self.led_dstdir .setText(dirpath + "/converted")


    def _OnDstPressed (self) :
        dirpath = QFileDialog.getExistingDirectory(self, "Browse destination", self.led_dstdir .text()  )
        if dirpath and os.path.exists(dirpath):
            dirpath = dirpath.replace("\\", "/")
            self.led_dstdir.setText(dirpath)

    def _OnDirChanged (self) :
        self.man.SetDstDir(  self.led_dstdir.text())
        self.man.SetSourceDir(self.led_srcdir.text())
        if len( self.man.GetDstPath() )==0:
            self.led_dstdir .setText( self.led_srcdir .text() + "/converted")

    def _OnAssnmChanged  (self):
        self .man .SetAssname( self .led_assname .text())

    def _OnConvertAll(self):
        self .tbl .ConvertAll ()







def main(arguments=None):


   #  spin = "\"Input - ARRI - Curve - V3 LogC (EI800)\""
   #  spout = "acescg" #
   #  test = "\"ACES - ACEScg\""
   # # cmd = "Z:/00_Development/oiio/oiiotool.exe F:/exr/base_hdr_v01.exr --colorconvert "+spin+" " +test+ " -d uint8 -o F:/exr/converted/picture.png"
   #  cmd = "Z:/00_Development/oiio/oiiotool.exe \"F:/exr/file.1014.exr\" --colorconvert \"ACES - ACES2065-1\" \"ACES - ACEScg\" -o \"F:/exr/converted/base_color_USERASS.1014.exr\""
   #  process = subprocess.Popen(cmd)
   #  process.wait()
   #  print process.returncode
   #
   #
   #  exit(0)
   #



    # inpath = '"F:/samp le.png"'
    # outpath = '"F:/out.exr"'
    # iconv = "Z:/00_Development/oiio/iconvert.exe"
    # outdepth = "-d float" # byte, short, half, float
    #
    #
    # args = " " .join (  (iconv, outdepth,   inpath, outpath )  )
    #
    #
    # process = subprocess.Popen(args )
    # process.wait()
    # print process.returncode
    #
    #
    # exit(0)




    qapp = QApplication (sys.argv)


    gui = MainWidnow ()

    #pal=gui .palette()
    #pal.setColor(QPalette.Window, QColor(46,46,46))
    #gui.setPalette(pal)

    gui  .led_srcdir .setText ("F:/exr")
    gui. led_dstdir.setText("F:/exr/converted")
    gui .show ()




    sys.exit(qapp.exec_())




if __name__ == '__main__':
    main ()
    #raise SystemExit(main(sys.argv[1:]))