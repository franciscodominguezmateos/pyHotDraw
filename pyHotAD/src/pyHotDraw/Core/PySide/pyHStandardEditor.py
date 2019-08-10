#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 25/03/2013

@author: paco
'''
import sys
import datetime as dt
import serial
import cv2
import numpy as np
from OpenCVQImage import OpenCVQImage
from Highlighter import Highlighter
from pydxfreader import dxfreader
from pypltreader import pltreader
from PySide import QtGui, QtCore
from pyHotDraw.Core.PySide.pyHStandardView import pyHStandardView
from pyHotDraw.Core.pyHAbstractEditor import pyHAbstractEditor
from pyHotDraw.Figures.pyHPolylineFigure import pyHPolylineFigure
from pyHotDraw.Figures.pyHSplineFigure import pyHSplineFigure
from pyHotDraw.Figures.pyHEllipseFigure import pyHEllipseFigure
from pyHotDraw.Figures.pyHArcFigure import pyHArcFigure
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Visitors.pyHGcodeGenerator import pyHGcodeGenerator
from pyHotDraw.Visitors.pyHPLTGenerator import pyHPLTGenerator
from pyHotDraw.Images.pyHImage import pyHImage
from pyHotDraw.Figures.pyHImageFigure import pyHImageFigure
from pyHotDraw.Figures.pyHImageFigure import pyHCameraFigure
from pyHotDraw.Figures.pyHImageFigure import pyHImageFilterFigure
from pyHotDraw.Images.pyHImageFilters import SobelX
from pyHotDraw.Images.pyHImageFilters import Gaussian

class pyHStandardEditor(QtGui.QMainWindow,pyHAbstractEditor):
    def __init__(self):
        super(pyHStandardEditor, self).__init__()
        pyHAbstractEditor.__init__(self)
        self.initActionMenuToolBars()
        self.statusBar()        
        self.initUI()
        
#Redefinning abstract methods
    def createMenuBar(self):
        return self.menuBar()
    def addMenuAndToolBar(self,name):
        self.menu[name]=self.menuBar.addMenu(name)
        self.toolBar[name]=self.addToolBar(name)
        self.actionGroup[name]=QtGui.QActionGroup(self)
    def addAction(self,menuName,icon,name,container,sortCut,statusTip,connect,addToActionGroup=False):
        a=QtGui.QAction(QtGui.QIcon(icon),name,container)
        a.setObjectName(name)
        a.setShortcut(sortCut)
        a.setStatusTip(statusTip)
        a.triggered.connect(connect)
        if addToActionGroup:
            a.setCheckable(True)
            self.actionGroup[menuName].addAction(a)
        self.menu[menuName].addAction(a)
        self.toolBar[menuName].addAction(a)
        #print "a.objectName:"+a.objectName()
        
    def initActionMenuToolBars(self):
        self.addMenuAndToolBar("&File")
        self.addAction("&File","../images/fileNew.png",'New',self,"Ctrl+N","New document",self.newFile)
        self.addAction("&File","../images/fileOpen.png",'Open',self,"Ctrl+O","Open document",self.openFile)
        self.addAction("&File","../images/fileSave.png",'Save',self,"Ctrl+Q","Save document",self.selectingFigures)
        self.addAction("&File","",'Exit',self,"Ctrl+Q","Exit application",self.close)
        self.addMenuAndToolBar("&Edit")
        self.addAction("&Edit","../images/editCopy.png",'Copy',self,"Ctrl+C","Copy",self.copy)
        self.addAction("&Edit","../images/editCut.png",'Cut',self,"Ctrl+X","Cut",self.cut)
        self.addAction("&Edit","../images/editPaste.png",'Paste',self,"Ctrl+V","Paste",self.paste)
        self.addAction("&Edit","../images/editUndo.png",'Paste',self,"Ctrl+V","Paste",self.selectingFigures)
        self.addAction("&Edit","../images/editRedo.png",'Paste',self,"Ctrl+V","Paste",self.selectingFigures)
        dbUnits=QtGui.QComboBox(self)
        dbUnits.addItem("Milimetros")
        dbUnits.addItem("Pulgadas")
        dbUnits.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        # create a menu item for our context menu.
        a = QtGui.QAction("A try...", self)
        dbUnits.addAction(a)
        a = QtGui.QAction("A try...", self)
        dbUnits.addAction(a)
        a = QtGui.QAction("A try...", self)
        dbUnits.addAction(a)
        self.toolBar["&Edit"].addWidget(dbUnits)
        self.addAction("&Edit","../images/zoom.png",'Zoom',self,"Ctrl+V","Zoom",self.selectingFigures)
        sceneScaleCombo = QtGui.QComboBox()
        sceneScaleCombo.addItems(["50%", "75%", "100%", "125%", "150%", "200%", "250%", "300%", "350%", "400%"])
        sceneScaleCombo.setCurrentIndex(2)
        sceneScaleCombo.setEditable(True)
        sceneScaleCombo.currentIndexChanged.connect(self.onScaleChanged)
        self.toolBar["&Edit"].addWidget(sceneScaleCombo)
        self.addMenuAndToolBar("&CAD")
        self.addAction("&CAD","../images/selectionTool.png",'Selection',self,"Ctrl+S","Selection Tool",self.selectingFigures,True)
        self.addAction("&CAD","../images/move.png",'View trasnlate',self,"Ctrl+v","View Translate Tool",self.viewTranslate,True)
        self.addAction("&CAD","../images/bug.png",'Rectangle',self,"Ctrl+S","Create Rectangle Tool",self.creatingCamera,True)
        self.addAction("&CAD","../images/createRoundRectangle.png",'Round Rectangle',self,"Ctrl+S","Selection Tool",self.creatingImage,True)
        self.addAction("&CAD","../images/createLineConnection.png",'Rectangle',self,"Ctrl+S","Create Rectangle Tool",self.creatingLineConnection,True)
        self.addAction("&CAD","../images/createPolygon.png",'Polyline',self,"Ctrl+S","Creatting Polyline",self.creatingPolyline,True)
        self.addAction("&CAD","../images/createLine.png",'Line',self,"Ctrl+S","Selection Tool",self.creatingLine,True)
        self.addAction("&CAD","../images/createRectangle.png",'Rectangle',self,"Ctrl+S","Create Rectangle Tool",self.creatingRectangle,True)
        self.addAction("&CAD","../images/createRoundRectangle.png",'Round Rectangle',self,"Ctrl+S","Selection Tool",self.creatingRectangle,True)
        self.addAction("&CAD","../images/createEllipse.png",'Ellipse',self,"Ctrl+S","Selection Tool",self.creatingEllipse,True)
        self.addAction("&CAD","../images/createDiamond.png",'Ellipse',self,"Ctrl+S","Selection Tool",self.creatingDiamond,True)
        self.addAction("&CAD","../images/createScribble.png",'Spline',self,"Ctrl+S","Spline Tool",self.creatingSpline,True)
        self.addAction("&CAD","../images/jointPoints1.png",'Join',self,"Ctrl+S","Join points",self.join,False)
        self.addAction("&CAD","../images/selectionGroup.png",'Selection Group',self,"Ctrl+S","Selection Group",self.selectionGroup,False)
        self.addAction("&CAD","../images/selectionUngroup.png",'Selection Ungroup',self,"Ctrl+S","Selection Ungroup",self.selectionUngroup,False)
        self.addAction("&CAD","../images/moveToBack.png",'Move to Back',self,"Ctrl+S","Move to Back",self.moveBack,False)
        self.addAction("&CAD","../images/moveToFront.png",'Move to Front',self,"Ctrl+S","Move to Front",self.moveFront,False)
        self.addMenuAndToolBar("CA&M")
        self.addAction("CA&M","../images/profile.png",'Profile',self,"Ctrl+C","Copy",self.close)
        self.addAction("CA&M","../images/pocket.png",'Pocket',self,"Ctrl+C","Copy",self.close)
        self.addAction("CA&M","../images/drill.png",'Drill',self,"Ctrl+C","Copy",self.close)
        self.addAction("CA&M","../images/engraver.png",'Engraving',self,"Ctrl+C","Copy",self.close)
        self.addMenuAndToolBar("&GCode-Host")
        self.addAction("&GCode-Host","../images/moveWest.png",'Left',self,"Ctrl+o","Left",self.close)
        self.addAction("&GCode-Host","../images/moveNorth.png",'Up',self,"Ctrl+q","Up",self.close)
        self.addAction("&GCode-Host","../images/moveSouth.png",'Down',self,"Ctrl+a","Down",self.close)
        self.addAction("&GCode-Host","../images/moveEast.png",'Right',self,"Ctrl+p","Right",self.close)
        self.addAction("&GCode-Host","../images/home.png",'Copy',self,"Ctrl+C","Copy",self.close)
        txGcode=QtGui.QComboBox()
        txGcode.setMinimumWidth(100)
        txGcode.addItems(["G0 ","G1 ","G2 ","G3 ","F ","M3 ","M5"])
        txGcode.setEditable(True)
        self.toolBar["&GCode-Host"].addWidget(txGcode)
        self.addAction("&GCode-Host","../images/play.png",'Play',self,"Ctrl+C","Play",self.close)
        self.addAction("&GCode-Host","../images/bug.png",'Simulation',self,"Ctrl+C","Simulation",self.close)
        self.addMenuAndToolBar("&Align")
        self.addAction("&Align","../images/alignGrid.png",'Grid',self,"Ctrl+g","Align Grid",self.selectingFigures)
        self.addAction("&Align","../images/alignWest.png",'West',self,"Ctrl+w","Align West",self.selectingFigures)
        self.addAction("&Align","../images/alignEast.png",'East',self,"Ctrl+e","Align East",self.selectingFigures)
        self.addAction("&Align","../images/alignNorth.png",'North',self,"Ctrl+s","Align North",self.selectingFigures)
        self.addAction("&Align","../images/alignSouth.png",'South',self,"Ctrl+n","Align South",self.selectingFigures)
        self.addAction("&Align","../images/alignVertical.png",'Vertical',self,"Ctrl+C","Align Vertical",self.selectingFigures)
        self.addAction("&Align","../images/alignHorizontal.png",'Horizontal',self,"Ctrl+C","Align Horizontal",self.selectingFigures)

    def onScaleChanged(self,index):
        s=float(index)
        t=self.getView().getTransform()
        t.sx=s+0.50
        t.sy=s+0.50
        self.getView().update()
    def newFile(self):
        self.getView().getDrawing().clearFigures()
        self.getView().update()
    def openFile(self):
        self.getView().getDrawing().clearFigures()
        fileNames = QtGui.QFileDialog.getOpenFileName(self,("Open Image"), QtCore.QDir.currentPath(), ("Image Files (*.dxf)"))
        if not fileNames:
            fileName="C:\\Users\\paco\\Desktop\\a4x2laser.dxf"
        else:
            fileName=fileNames[0]
        self.openDXF(fileName)
        self.getView().update()
        
    def fillTreePoints(self,wgTree,fPoints):
        for i,p in enumerate(fPoints.getPoints()):
            cName=p.__class__.__name__+"(%0.2f,%0.2f)" % (p.getX(),p.getY())
            tw=QtGui.QTreeWidgetItem(wgTree,[str(i)+" "+cName])
            tw.setData(3,QtCore.Qt.ItemDataRole.UserRole,p)
    def fillTreeWidget(self,wgTree,fSet):
        for i,f in enumerate(fSet.getFigures()):
            cName=f.__class__.__name__
            tw=QtGui.QTreeWidgetItem(wgTree,[str(i)+" "+cName])
            tw.setData(3,QtCore.Qt.ItemDataRole.UserRole,f)
            if cName=="pyHCompositeFigure":
                self.fillTreeWidget(tw,f)            
            if cName=="pyHPolylineFigure" or cName=="pyHSplineFigure":
                self.fillTreePoints(tw,f)    
    def fillTree(self):
        justNow=dt.datetime.now()
        if (justNow-self.timeElapsed).microseconds<200000:
            return
        self.timeElapsed=justNow
        items=[]
        i=0
        d=self.getView().getDrawing()
        self.treeWidget.clear()
        ic=QtGui.QIcon("../images/fileNew.png")
        for f in d.getFigures():
            cName=f.__class__.__name__
            tw=QtGui.QTreeWidgetItem(None,[str(i)+" "+cName])
            tw.setData(3,QtCore.Qt.ItemDataRole.UserRole,f)
            tw.setIcon(0,ic)
#            tw.setFlags(QtCore.qt.ItemIsUserCheckable)
            items.append(tw)
            if cName=="pyHCompositeFigure":
                self.fillTreeWidget(tw,f)
            if cName=="pyHPolylineFigure" or cName=="pyHSplineFigure":
                self.fillTreePoints(tw,f)
            i+=1
        self.treeWidget.insertTopLevelItems(0, items)

    def nodoClick(self,item,colum):
        f=item.data(3,QtCore.Qt.ItemDataRole.UserRole)
        cName=f.__class__.__name__
        if cName!="pyHPoint" and cName!="NoneType":
            if self.getView().isThisFigureInSelectedFigures(f):
                self.getView().unSelectFigure(f)
            else:
                self.getView().selectFigure(f)
            self.getView().update()
            #self.treeProperties=QtGui.QTreeWidget(self)
            self.treeProperties.clear()
            self.treeProperties.setColumnCount(2)
            self.treeProperties.setHeaderLabels(["Key","Value"])
            twi=QtGui.QTreeWidgetItem(self.treeProperties,["Name","TopBox"])
            twi.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
            twi=QtGui.QTreeWidgetItem(self.treeProperties,["Type",cName])
            twi.setFlags(QtCore.Qt.ItemIsEnabled  | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable)
            twi.setCheckState(1,QtCore.Qt.Checked)
            twi=QtGui.QTreeWidgetItem(self.treeProperties,["X","100.00"])
            twi.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
            twi=QtGui.QTreeWidgetItem(self.treeProperties,["Y","100.00"])
            twi.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
            twi=QtGui.QTreeWidgetItem(self.treeProperties,["Width","30.00"])
            twi.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
            twi=QtGui.QTreeWidgetItem(self.treeProperties,["Height","50.0"])
            twi.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
        else:
            self.treeProperties.clear()
            self.treeProperties.setColumnCount(2)
            self.treeProperties.setHeaderLabels(["Key","Value"])
            QtGui.QTreeWidgetItem(self.treeProperties,["Name","point#"])
            QtGui.QTreeWidgetItem(self.treeProperties,["Type",cName])
            QtGui.QTreeWidgetItem(self.treeProperties,["X",str(f.getX())])
            QtGui.QTreeWidgetItem(self.treeProperties,["Y",str(f.getY())])

    def updateDraw(self,item,col):
        print ("item changed "+str(col)+"="+item.data(col,QtCore.Qt.DisplayRole)+" "+item.data(3,QtCore.Qt.ItemDataRole.UserRole).__class__.__name__)
    def generateCode(self):
        item=self.treeWidget.currentItem()
        f=item.data(3,QtCore.Qt.ItemDataRole.UserRole)
        gc=pyHGcodeGenerator()
        sgc=f.visit(gc)
        self.gCodeEditor.setPlainText(sgc)
    def generatePLT(self):
        item=self.treeWidget.currentItem()
        f=item.data(3,QtCore.Qt.ItemDataRole.UserRole)
        gc=pyHPLTGenerator()
        sgc=f.visit(gc)
        self.gCodeEditor.setPlainText(sgc)
    def initUI(self):                       
        self.treeWidget = QtGui.QTreeWidget(self)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(["Figuras de colores"])
        self.treeWidget.itemClicked.connect(self.nodoClick)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        # create a menu item for our context menu.
        a = QtGui.QAction("Generate G-Code", self)
        a.triggered.connect(self.generateCode)
        self.treeWidget.addAction(a)
        a = QtGui.QAction("Generate PLT code", self)
        a.triggered.connect(self.generatePLT)
        self.treeWidget.addAction(a)

        dockWidget = QtGui.QDockWidget("Explorer Widget", self)
        dockWidget.setWidget(self.treeWidget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockWidget)
        
        dockWidget2 = QtGui.QDockWidget("CAM Widget", self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockWidget2)
                
        self.treeProperties=QtGui.QTreeWidget(self)
        self.treeProperties.setColumnCount(2)
        self.treeProperties.setAlternatingRowColors(True)
        self.treeProperties.setHeaderLabels(["Name","Value"])
        self.treeProperties.itemChanged.connect(self.updateDraw)

        dockWidget1 = QtGui.QDockWidget("Properties Widget", self)
        dockWidget1.setWidget(self.treeProperties)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockWidget1)
        
        dockWgGcodeEditor=QtGui.QDockWidget("G-Code editor",self)
        self.gCodeEditor=QtGui.QTextEdit()
        self.gCodeEditor.setViewportMargins(15,0,0,0)
        self.gCodeEditor.setPlainText("""G21 (All units in mm)
M02
#6  = 0 (X axis offset)
#7  = 0 (Y axis offset)
G0 X0 Y0 Z0 F1000
G00 X[10+#7] Y[10+#8]
G01 X75 Z-20 F400
G02 X20 Y20 I2 J.7
data error
M05""")
        hl=Highlighter(self.gCodeEditor.document())
        dockWgGcodeEditor.setWidget(self.gCodeEditor)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,dockWgGcodeEditor)
        self.setView(pyHStandardView(self))
        
#         scrollArea = QtGui.QScrollArea()
#         scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
#         scrollArea.setWidget(self.getView())
        
        self.setCentralWidget(self.getView())
        self.setGeometry(300, 30,900,500)
        self.setWindowTitle('TinyCADCAMCNC')    
        self.sb=QtGui.QLabel(self)
        self.sb.setText("x=0,y=0")
        self.statusBar().addPermanentWidget(self.sb)
        self.sb1=QtGui.QLabel(self)
        self.show()    
 
              
    def openDXF(self,fileName):
        d=self.getView().getDrawing()
        for et in dxfreader.getEtt(fileName):
            if et["0"]=="LINE":
                x0=float(et["10"])
                y0=float(et["20"])
                p0=pyHPoint(x0,y0)
                x1=float(et["11"])
                y1=float(et["21"])
                p1=pyHPoint(x1,y1)
                l=pyHPolylineFigure()
                l.addPoint(p0)
                l.addPoint(p1)
                d.addFigure(l)
            if et["0"]=="CIRCLE":
                x0=float(et["10"])
                y0=float(et["20"])
                r =float(et["40"])
                c=pyHEllipseFigure(x0-r,y0-r,2*r,2*r)
                d.addFigure(c)
            if et["0"]=="POINT":
                x0=float(et["10"])
                y0=float(et["20"])
                r =2
                c=pyHEllipseFigure(x0-r,y0-r,2*r,2*r)
                d.addFigure(c)
            if et["0"]=="ARC":
                x0=float(et["10"])
                y0=float(et["20"])
                r =float(et["40"])
                ans=float(et["50"])
                ane=float(et["51"])
                c=pyHArcFigure(x0-r,y0-r,2*r,2*r,ans,ane)
                d.addFigure(c)
            if et["0"]=="LWPOLYLINE":
                xs=et["10"]
                ys=et["20"]
                c=pyHPolylineFigure()
                for i,x in enumerate(xs):
                    p=pyHPoint(float(x),float(ys[i]))
                    c.addPoint(p)
                d.addFigure(c)
            if et["0"]=="SPLINE":
                xs=et["10"]
                ys=et["20"]
                c=pyHSplineFigure()
                for i,x in enumerate(xs):
                    p=pyHPoint(float(x),float(ys[i]))
                    c.addPoint(p)
                d.addFigure(c)
        self.fillTree()
        
    def openPLT(self,fileName):
        d=self.getView().getDrawing()
        f=pyHPolylineFigure()
        for t in pltreader.getPLT(fileName):
            if len(t)==3:
                c,x,y=t
                if pltreader.isPU(c):
                    if f:
                        if len(f.getPoints())>1:
                            d.addFigure(f)
                    f=pyHPolylineFigure()
                    xf=float(x)*0.025
                    yf=float(y)*0.025
                    p=pyHPoint(xf,yf)
                    f.addPoint(p)
                elif pltreader.isPD(c):
                    xf=float(x)*0.025
                    yf=float(y)*0.025
                    p=pyHPoint(xf,yf)
                    f.addPoint(p)
                    
def scan(num_ports = 20, verbose=False):
    #-- Lista de los dispositivos serie. Inicialmente vacia
    dispositivos_serie = []
    if verbose:
        print ("Escanenado %d puertos serie:" % num_ports)
    
    #-- Escanear num_port posibles puertos serie
    for i in range(num_ports):
        if verbose:
            sys.stdout.write("puerto %d: " % i)
            sys.stdout.flush()
        try:
            #-- Abrir puerto serie
            s = serial.Serial(i)
            if verbose: print ("OK --> %s" % s.portstr)
            #-- Si no hay errores, anadir el numero y nombre a la lista
            dispositivos_serie.append( (i, s.portstr))
            #-- Cerrar puerto
            s.close()
        #-- Si hay un error se ignora
        except:
            if verbose: 
                print ("NO")
    #-- Devolver la lista de los dispositivos serie encontrados    
    return dispositivos_serie

               
def main():
    app = QtGui.QApplication(sys.argv)
    ex = pyHStandardEditor()
    
    ex.timeElapsed=dt.datetime.now()
    ex.openDXF("a4x2laser.dxf")
    #puertos_disponibles=scan(num_ports=20,verbose=True)
    #ex.openPLT("a4x2laser.plt")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        