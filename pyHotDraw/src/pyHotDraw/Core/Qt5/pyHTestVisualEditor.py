#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 25/03/2013

@author: paco
'''
import sys
import datetime as dt
import os
import serial
import cv2
import numpy as np
#from pydxfreader import dxfreader
#from pypltreader import pltreader
from PyQt5 import QtGui,QtWidgets, QtCore
import pyHotDraw
from pyHotDraw.Core.Qt5.pyHStandardView import pyHStandardView
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
from matplotlib.backends.qt_compat import QtWidgets

class pyHStandardEditor(QtWidgets.QMainWindow,pyHAbstractEditor):
    def __init__(self):
        super(pyHStandardEditor, self).__init__()
        pyHAbstractEditor.__init__(self)
        self.initActionMenuToolBars()
        self.statusBar()        
        self.initUI()
        
        d=self.getView().getDrawing()
        txt=pyHTextFigure(0,0,20,20,"Hola Caracola")
        d.addFigure(txt)
        #cam1=pyHCameraFigure(0,200,50,50,1)
        #d.addFigure(cam1)
        imgc1=pyHImageDottedFigure(150,250,320,240)
        imgc1.setPoints([pyHPoint(20,20),pyHPoint(30,30)])
        d.addFigure(imgc1)
        #cam1.addChangedImageObserver(imgc1)
        cam=pyHCameraFigure(0,100,50,50,0)
        d.addFigure(cam)
        img0=pyHImageFigure(50,10,320,240)
        d.addFigure(img0)
        cam.addChangedImageObserver(img0)
        img1=pyHImageFigure(400,10,320,240)
        d.addFigure(img1)
        fimg=pyHImageFilterFigure(300,300,40,40)
        d.addFigure(fimg)
        cam.addChangedImageObserver(fimg)
        fimg.addChangedImageObserver(img1)
        #img2=pyHImageFigure(0,300,320,240)
        #d.addFigure(img2)
        img3=pyHImageFigure(400,10,320,240)
        d.addFigure(img3)
        fimg1=pyHImageFilterFigure(300,400,40,40)
        d.addFigure(fimg1)
        fimg1.setFilter(Gaussian())
        cam.addChangedImageObserver(fimg1)
        fimg1.addChangedImageObserver(img3)
        
        fimgH=pyHImageFilterFigure(400,500,30,30)
        d.addFigure(fimgH)
        fimgH.setFilter(HistogramColor())
        fimg1.addChangedImageObserver(fimgH)
        imgH=pyHImageFigure(500,0,256,150)
        d.addFigure(imgH)
        fimgH.addChangedImageObserver(imgH)
        fimg2=pyHImageFilterFigure(300,500,40,40)
        d.addFigure(fimg2)
        fimg2.setFilter(SobelX())
        fimg1.addChangedImageObserver(fimg2)
        img4=pyHImageFigure(0,300,320,240)
        d.addFigure(img4)
        fimg2.addChangedImageObserver(img4)
        fimg2y=pyHImageFilterFigure(240,300,40,40)
        d.addFigure(fimg2y)
        fimg2y.setFilter(SobelY())
        fimg1.addChangedImageObserver(fimg2y)
        img4y=pyHImageFigure(240,300,320,240)
        d.addFigure(img4y)
        fimg2y.addChangedImageObserver(img4y)

        img4=pyHImageFigure(10,600,320,240)
        d.addFigure(img4)
        fimg4=pyHImageFilterFigure(0,600,40,40)
        d.addFigure(fimg4)
        fimg4.setFilter(OpticalFlow())
        cam.addChangedImageObserver(fimg4)
        fimg4.addChangedImageObserver(img4)

#         img5=pyHImageFigure(400,600,320,240)
#         d.addFigure(img5)
#         fimg5=pyHImageFilterFigure(400,600,40,40)
#         d.addFigure(fimg5)
#         fimg5.setFilter(FastFeatureDetector())
#         cam.addChangedImageObserver(fimg5)
#         img5.setImageSourceFigure(fimg5)



#         #imgCm1=pyHImage('/Users/paco/Pictures/sfm/urjcMostolesMobilLG440-15011301/CAM00295.jpg')
#         imgCm1=pyHImage('/media/francisco/Packard Bell/Users/paco/Pictures/sfm/pistaTenis/CAM00698.jpg')
#         #imgCm1=pyHImage('../images/im2.png')
#         ifcm1=pyHImageDottedFigure(0,0,240,320,imgCm1)
#         ifcm1.setPoints([pyHPoint(400,690),pyHPoint(1776,690),pyHPoint(1394,560),pyHPoint(737,560)])
#         d.addFigure(ifcm1)
#         
#         fd=FeatureDetector("SIFT")
#         imgCvCm1Fd=fd.process(imgCm1.data)
#         #imgCm1=pyHImage('../images/im2.png')
#         imgCm1Fd=pyHImage()
#         imgCm1Fd.setData(imgCvCm1Fd)
#         ifcm1Fd=pyHImageFigure(0,320,240,320,imgCm1Fd)
#         d.addFigure(ifcm1Fd)
#         
#         #imgCm2=pyHImage('/Users/paco/Pictures/sfm/urjcMostolesMobilLG440-15011301/CAM00294.jpg')
#         imgCm2=pyHImage('/media/francisco/Packard Bell/Users/paco/Pictures/sfm/pistaTenis/CAM00699.jpg')
#         #imgCm1=pyHImage('../images/im2.png')
#         ifcm2=pyHImageDottedFigure(240,0,240,320,imgCm2)
#         ifcm2.setPoints([pyHPoint(400,690),pyHPoint(1776,690),pyHPoint(1394,560),pyHPoint(737,560)])
#         d.addFigure(ifcm2)
#         
#         imgCvCm2Fd=fd.process(imgCm2.data)
#         imgCm2Fd=pyHImage()
#         imgCm2Fd.setData(cv2.addWeighted(imgCvCm1Fd,0.5,imgCvCm2Fd,0.5,0))
#         ifcm2Fd=pyHImageFigure(0,0,240,320,imgCm2Fd)
#         d.addFigure(ifcm2Fd)
#         
        
        #imgCm10=pyHImage('/media/francisco/Packard Bell/Users/paco/Dropbox/Tranquinet/I+D+I/Electronica/robotica/software/tracking/tranquiTrack/images/logitech/shot_0_000.bmp')
        #imgCm11=pyHImage('/media/francisco/Packard Bell/Users/paco/Dropbox/Tranquinet/I+D+I/Electronica/robotica/software/tracking/tranquiTrack/images/logitech/shot_0_001.bmp')
#         imgCm10=pyHImage('/Users/paco/Dropbox/Tranquinet/I+D+I/Electronica/robotica/software/tracking/tranquiTrack/images/logitech/shot_0_000.bmp')
#         imgCm11=pyHImage('/Users/paco/Dropbox/Tranquinet/I+D+I/Electronica/robotica/software/tracking/tranquiTrack/images/logitech/shot_0_001.bmp')
#         #fm=FlannMacher()
#         fm=FundamentalMatrix()
#         #fm=HomographyMatrix()
#         fm.imgcv1=imgCm10.data
#         fm.imgcv2=imgCm11.data
#         #fm.imgcv1=cam1.getImage().data
#         #fm.imgcv2=cam.getImage().data
#         imgCm5=pyHImage()
#         imgCm5.setData(fm.process())
#         ifcm5=pyHImageFigure(0,0,640,240,imgCm5)
#         d.addFigure(ifcm5)
#         
#         immf=pyHImagesMixedFigure(20,20,640,240,imgCm10)
#         immf.setImage2(imgCm11)
#         immf.setFilter(fm)
#         immf.setImageSourceFigure1(cam)
#         immf.setImageSourceFigure2(cam1)
#         d.addFigure(immf)
#         
#         imsf=pyHImageSecFilterFigure(300,20,50,50)
#         imsf.setFilter(fm)
#         imfsec=pyHImageFigure(330,20,640,240)
#         imsf.addChangedImageObserver(imfsec)
#         cam.addChangedImageObserver(imsf)
#         d.addFigure(imsf)
#         d.addFigure(imfsec)
        


        
        #imgCm3=pyHImage('../images/googleEarth_CampusMostoles15031101.png')
        #ifcm3=pyHImageFigure(0,0,320*2,240*2,imgCm3)
        #d.addFigure(ifcm3)
        #imgCm4=pyHImage('../images/googleEarth_CampusMostolesZoom15031101.png')
        #ifcm4=pyHImageFigure(0,0,320*2,240*2,imgCm4)
        #d.addFigure(ifcm4)
        
        self.getView().setTransformFitToDrawing()
        
        #self.setupCamera()
        
#Redefinning abstract methods
    def createMenuBar(self):
        return QtWidgets.QMainWindow.menuBar(self)
    def addMenuAndToolBar(self,name):
        self.menu[name]=self.menuBar.addMenu(name)
        self.toolBar[name]=self.addToolBar(name)
        self.actionGroup[name]=QtWidgets.QActionGroup(self)
    def addAction(self,menuName,icon,name,container,sortCut,statusTip,connect,addToActionGroup=False):
        a=QtWidgets.QAction(QtGui.QIcon(icon),name,container)
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
        path=pyHotDraw.ICONS_PATH
        self.addMenuAndToolBar("&File")
        self.addAction("&File",os.path.join(path,"fileNew.png"),'New',self,"Ctrl+N","New document",self.newFile)
        self.addAction("&File",os.path.join(path,"fileOpen.png"),'Open',self,"Ctrl+O","Open document",self.openFile)
        self.addAction("&File",os.path.join(path,"images/fileSave.png"),'Save',self,"Ctrl+Q","Save document",self.selectingFigures)
        self.addAction("&File","",'Exit',self,"Ctrl+Q","Exit application",self.close)
        self.addMenuAndToolBar("&Edit")
        self.addAction("&Edit",os.path.join(path,"editCopy.png" ),'Copy',self,"Ctrl+C","Copy",self.copy)
        self.addAction("&Edit",os.path.join(path,"editCut.png"  ),'Cut',self,"Ctrl+X","Cut",self.cut)
        self.addAction("&Edit",os.path.join(path,"editPaste.png"),'Paste',self,"Ctrl+V","Paste",self.paste)
        self.addAction("&Edit",os.path.join(path,"editUndo.png" ),'Paste',self,"Ctrl+V","Paste",self.selectingFigures)
        self.addAction("&Edit",os.path.join(path,"editRedo.png" ),'Paste',self,"Ctrl+V","Paste",self.selectingFigures)
        dbUnits=QtWidgets.QComboBox(self)
        dbUnits.addItem("Milimetros")
        dbUnits.addItem("Pulgadas")
        dbUnits.addItem("Pixels")
        dbUnits.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        # create a menu item for our context menu.
        a = QtWidgets.QAction("A try...", self)
        dbUnits.addAction(a)
        a = QtWidgets.QAction("A try...", self)
        dbUnits.addAction(a)
        a = QtWidgets.QAction("A try...", self)
        dbUnits.addAction(a)
        self.toolBar["&Edit"].addWidget(dbUnits)
        self.addAction("&Edit",path+"zoom.png",'Zoom',self,"Ctrl+V","Zoom",self.selectingFigures)
        sceneScaleCombo = QtWidgets.QComboBox()
        sceneScaleCombo.addItems(["50%", "75%", "100%", "125%", "150%", "200%", "250%", "300%", "350%", "400%"])
        sceneScaleCombo.setCurrentIndex(2)
        sceneScaleCombo.setEditable(True)
        sceneScaleCombo.currentIndexChanged.connect(self.onScaleChanged)
        self.toolBar["&Edit"].addWidget(sceneScaleCombo)
        self.addMenuAndToolBar("&CAD")
        self.addAction("&CAD",os.path.join(path,"selectionTool.png"),'Selection',self,"Ctrl+S","Selection Tool",self.selectingFigures,True)
        self.addAction("&CAD",os.path.join(path,"move.png"),'View trasnlate',self,"Ctrl+v","View Translate Tool",self.viewTranslate,True)
        self.addAction("&CAD",os.path.join(path,"bug.png"),'Camera',self,"Ctrl+S","Create Camera",self.creatingCamera,True)
        self.addAction("&CAD",os.path.join(path,"createRoundRectangle.png"),'Create Image',self,"Ctrl+S","Selection Tool",self.creatingImage,True)
        self.addAction("&CAD",os.path.join(path,"createLineConnection.png"),'Create Image Filter connection',self,"Ctrl+S","Create Image Filter connection Tool",self.creatingLineImageFilterConnection,True)
        self.addAction("&CAD",os.path.join(path,"createLineConnection.png"),'Create connection',self,"Ctrl+S","Create connection Tool",self.creatingLineConnection,True)
        self.addAction("&CAD",os.path.join(path,"createPolygon.png"),'Polyline',self,"Ctrl+S","Creatting Polyline",self.creatingPolyline,True)
        self.addAction("&CAD",os.path.join(path,"createLine.png"),'Line',self,"Ctrl+S","Selection Tool",self.creatingLine,True)
        self.addAction("&CAD",os.path.join(path,"createRectangle.png"),'Rectangle',self,"Ctrl+S","Create Rectangle Tool",self.creatingRectangle,True)
        self.addAction("&CAD",os.path.join(path,"createRoundRectangle.png"),'Round Rectangle',self,"Ctrl+S","Selection Tool",self.creatingRectangle,True)
        self.addAction("&CAD",os.path.join(path,"createEllipse.png"),'Ellipse',self,"Ctrl+S","Selection Tool",self.creatingEllipse,True)
        self.addAction("&CAD",os.path.join(path,"createDiamond.png"),'Ellipse',self,"Ctrl+S","Selection Tool",self.creatingDiamond,True)
        self.addAction("&CAD",os.path.join(path,"createScribble.png"),'Spline',self,"Ctrl+S","Spline Tool",self.creatingSpline,True)
        self.addAction("&CAD",os.path.join(path,"jointPoints1.png"),'Join',self,"Ctrl+S","Join points",self.join,False)
        self.addAction("&CAD",os.path.join(path,"selectionGroup.png"),'Selection Group',self,"Ctrl+S","Selection Group",self.selectionGroup,False)
        self.addAction("&CAD",os.path.join(path,"selectionUngroup.png"),'Selection Ungroup',self,"Ctrl+S","Selection Ungroup",self.selectionUngroup,False)
        self.addAction("&CAD",os.path.join(path,"moveToBack.png"),'Move to Back',self,"Ctrl+S","Move to Back",self.moveBack,False)
        self.addAction("&CAD",os.path.join(path,"moveToFront.png"),'Move to Front',self,"Ctrl+S","Move to Front",self.moveFront,False)

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
        fileNames = QtWidgets.QFileDialog.getOpenFileName(self,("Open Image"), QtCore.QDir.currentPath(), ("Image Files (*.dxf)"))
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
        
#         scrollArea = QtWidgets.QScrollArea()
#         scrollArea.setBackgroundRole(QtWidgets.QPalette.Dark)
#         scrollArea.setWidget(self.getView())
        
        self.setCentralWidget(self.getView())
        self.setGeometry(300, 30,900,500)
        self.setWindowTitle('pyHotVision')    
        self.sb=QtWidgets.QLabel(self)
        self.sb.setText("x=0,y=0")
        self.statusBar().addPermanentWidget(self.sb)
        self.sb1=QtWidgets.QLabel(self)
        self.setCurrentTool(pyHSelectionTool(self.getView()))
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
        print "Escanenado %d puertos serie:" % num_ports
    
    #-- Escanear num_port posibles puertos serie
    for i in range(num_ports):
        if verbose:
            sys.stdout.write("puerto %d: " % i)
            sys.stdout.flush()
        try:
            #-- Abrir puerto serie
            s = serial.Serial(i)
            if verbose: print "OK --> %s" % s.portstr
            #-- Si no hay errores, anadir el numero y nombre a la lista
            dispositivos_serie.append( (i, s.portstr))
            #-- Cerrar puerto
            s.close()
        #-- Si hay un error se ignora
        except:
            if verbose: 
                print "NO"
    #-- Devolver la lista de los dispositivos serie encontrados    
    return dispositivos_serie

               
def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = pyHStandardEditor()
    
    ex.timeElapsed=dt.datetime.now()
    #ex.openDXF("a4x2laser.dxf")
    #puertos_disponibles=scan(num_ports=20,verbose=True)
    #ex.openPLT("a4x2laser.plt")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        