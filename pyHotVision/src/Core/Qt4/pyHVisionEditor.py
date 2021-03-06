#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 13/07/2019
@author: Francisco Dominguez
'''
import sys
import datetime as dt
import glob
import cv2
import numpy as np
from PyQt4 import QtGui, QtCore
from pyHotDraw.Core.Qt4.pyHStandardView import pyHStandardView
from pyHotDraw.Core.pyHAbstractEditor import pyHAbstractEditor
from pyHotDraw.Tools.pyHSelectionTool import pyHSelectionTool
from pyHotDraw.Figures.pyHPolylineFigure import pyHPolylineFigure
from pyHotDraw.Figures.pyHSplineFigure import pyHSplineFigure
from pyHotDraw.Figures.pyHEllipseFigure import pyHEllipseFigure
from pyHotDraw.Figures.pyHArcFigure import pyHArcFigure
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Visitors.pyHGcodeGenerator import pyHGcodeGenerator
from pyHotDraw.Visitors.pyHPLTGenerator import pyHPLTGenerator
from pyHotDraw.Images.pyHImage import pyHImage
from pyHotDraw.Figures.pyHImageFigure import pyHImageFigure
from pyHotDraw.Figures.pyHImageFigure import pyHImageDottedFigure
from pyHotDraw.Figures.pyHImageFigure import pyHImagesMixedFigure
from pyHotDraw.Figures.pyHImageFigure import pyHCameraFigure
from pyHotDraw.Figures.pyHImageFigure import pyHImageFilterFigure
from pyHotDraw.Figures.pyHImageFigure import pyHImageSecFilterFigure
from pyHotDraw.Figures.pyHTextFigure import pyHTextFigure
from pyHotDraw.Images.pyHImageFilters import SobelX
from pyHotDraw.Images.pyHImageFilters import SobelY
from pyHotDraw.Images.pyHImageFilters import Gaussian
from pyHotDraw.Images.pyHImageFilters import OpticalFlow
from pyHotDraw.Images.pyHImageFilters import FeatureDetector
from pyHotDraw.Images.pyHImageFilters import FastFeatureDetector
from pyHotDraw.Images.pyHImageFilters import FlannMacher
from pyHotDraw.Images.pyHImageFilters import FundamentalMatrix
from pyHotDraw.Images.pyHImageFilters import HomographyMatrix
from pyHotDraw.Images.pyHImageFilters import HistogramColor

def draw_boxes(img, bboxes, color=(0, 0, 255), thick=6):
    # Make a copy of the image
    imcopy = np.copy(img)
    # Iterate through the bounding boxes
    for bbox in bboxes:
        # Draw a rectangle given bbox coordinates
        irec0=(int(bbox[0][0]),int(bbox[0][1]))
        irec1=(int(bbox[1][0]),int(bbox[1][1]))
        #cv2.rectangle(imcopy, irec0 , irec1, color, thick)
        cv2.rectangle(imcopy, bbox[0] , bbox[1], color, thick)
    # Return the image copy with boxes drawn
    return imcopy

class pyHVisionEditor(QtGui.QMainWindow,pyHAbstractEditor):
    def __init__(self):
        super(pyHVisionEditor, self).__init__()
        pyHAbstractEditor.__init__(self)
        self.initActionMenuToolBars()
        self.statusBar()        
        self.initUI()
        d=self.getView().getDrawing()
        
        txt=pyHTextFigure(0,400,20,20,"Hola Caracola")
        d.addFigure(txt)
        #cam1=pyHCameraFigure(0,200,50,50,0)
        #d.addFigure(cam1)
        cam=pyHCameraFigure(200,500,50,50,0)
        d.addFigure(cam)
        cam.addPreviewFigure(d)     
        
        fimg=pyHImageFilterFigure(500,500,40,40)
        d.addFigure(fimg)
        fimg.setFilter(Gaussian())
        fimg.addPreviewFigure(d)
        cf=fimg.getInputConnectionFigure(cam)
        d.addFigure(cf)
        
        fimg1=pyHImageFilterFigure(800,500,40,40)
        d.addFigure(fimg1)
        fimg1.addPreviewFigure(d)
        #cam.addChangedImageObserver(fimg1)
        cf=fimg1.getInputConnectionFigure(cam)
        d.addFigure(cf)
        #fimg1.addChangedImageObserver(img3)
#         
#         fimgH=pyHImageFilterFigure(400,500,30,30)
#         d.addFigure(fimgH)
#         fimgH.setFilter(HistogramColor())
#         fimg1.addChangedImageObserver(fimgH)
#         imgH=pyHImageFigure(500,0,256,150)
#         d.addFigure(imgH)
#         fimgH.addChangedImageObserver(imgH)
#         
        fimg2=pyHImageFilterFigure(800,800,40,40)
        d.addFigure(fimg2)
        fimg2.setFilter(SobelX())
        fimg2.addPreviewFigure(d)
        cf=fimg2.getInputConnectionFigure(fimg)
        d.addFigure(cf)
       
        fimg2y=pyHImageFilterFigure(800,300,40,40)
        d.addFigure(fimg2y)
        fimg2y.setFilter(SobelY())
        fimg2y.addPreviewFigure(d)
        cf=fimg2y.getInputConnectionFigure(fimg)
        d.addFigure(cf)

        fimg4=pyHImageFilterFigure(0,600,40,40)
        d.addFigure(fimg4)
        fimg4.setFilter(OpticalFlow())
        fimg4.addPreviewFigure(d)
        cf=fimg4.getInputConnectionFigure(fimg)
        d.addFigure(cf)
        
        fimg4=pyHImageFilterFigure(800,600,40,40)
        d.addFigure(fimg4)
        fimg4.setFilter(OpticalFlow())
        fimg4.addPreviewFigure(d)
        cf=fimg4.getInputConnectionFigure(fimg2y)
        d.addFigure(cf)
        
        self.getView().setTransformFitToDrawing()

        
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
        dbUnits.addItem("Pixels")
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
        self.addAction("&CAD","../images/bug.png",'Camera',self,"Ctrl+S","Create Camera",self.creatingCamera,True)
        self.addAction("&CAD","../images/createRoundRectangle.png",'Create Image',self,"Ctrl+S","Selection Tool",self.creatingImage,True)
        self.addAction("&CAD","../images/createLineConnection.png",'Create Image Filter connection',self,"Ctrl+S","Create Image Filter connection Tool",self.creatingLineImageFilterConnection,True)
        self.addAction("&CAD","../images/createLineConnection.png",'Create connection',self,"Ctrl+S","Create connection Tool",self.creatingLineConnection,True)
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
        
    def updateDraw(self,item,col):
        print "item changed "+str(col)+"="+item.data(col,QtCore.Qt.DisplayRole)+" "+item.data(3,QtCore.Qt.ItemDataRole.UserRole).__class__.__name__
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
        self.setView(pyHStandardView(self))
        
#         scrollArea = QtGui.QScrollArea()
#         scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
#         scrollArea.setWidget(self.getView())
        
        self.setCentralWidget(self.getView())
        self.setGeometry(300, 30,1000,600)
        self.setWindowTitle('Qt4 - pyHotVision Face Tool '+cv2.__version__)    
        self.sb=QtGui.QLabel(self)
        self.sb.setText("x=0,y=0")
        self.statusBar().addPermanentWidget(self.sb)
        self.sb1=QtGui.QLabel(self)
        self.setCurrentTool(pyHSelectionTool(self.getView()))
        self.show()
                                   
def main():
    app = QtGui.QApplication(sys.argv)
    ex = pyHVisionEditor()
    
    ex.timeElapsed=dt.datetime.now()
    #ex.openDXF("a4x2laser.dxf")
    #puertos_disponibles=scan(num_ports=20,verbose=True)
    #ex.openPLT("a4x2laser.plt")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        