#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 13/07/2019
@author: Francisco Dominguez
'''
import sys
import datetime as dt
import glob
import pickle
import cv2
import numpy as np
from PyQt5 import QtGui,QtWidgets, QtCore
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
from pyHotDraw.Figures.pyHImageFigure import pyHImages2I1OFilterFigure
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
from pyHotDraw.Images.pyHImageFilters import Undistorter
from pyHotDraw.Images.pyHImageFilters import Rectify
from pyHotDraw.Images.pyHImageFilters import StereoSplitLeft
from pyHotDraw.Images.pyHImageFilters import StereoSplitRight
from pyHotDraw.Images.pyHImageFilters import FlannMacher
import pyHotDraw


class pyHVisionEditor(QtWidgets.QMainWindow,pyHAbstractEditor):
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
        camD=pyHCameraFigure(200,500,80,50,0,width=640*2)
        d.addFigure(camD)
        camD.addPreviewFigure(d,2)     
        
        camL=pyHImageFilterFigure(240,500,80,50,"Camera Left")        
        d.addFigure(camL)
        camL.setFilter(StereoSplitLeft())
        camL.addPreviewFigure(d)
        cf=camL.getInputConnectionFigure(camD)
        d.addFigure(cf)        
        camR=pyHImageFilterFigure(240,500,80,50,"Camera Right")        
        d.addFigure(camR)
        camR.setFilter(StereoSplitRight())
        camR.addPreviewFigure(d)
        cf=camR.getInputConnectionFigure(camD)
        d.addFigure(cf)        
        
        #CALIBRATIOM INFO
        KL=np.array([[917.407239  ,   0.        , 328.52914613],
                     [  0.        , 919.1541511 , 224.78093398],
                     [  0.        ,   0.        ,   1.        ]])
        distL=np.array([[-4.51526228e-01,  3.58762955e-01,  1.17374106e-04, -1.83499141e-03, -1.87366908e-01]])
        KR=np.array([[918.22817005,   0.        , 302.54145304],
                     [  0.        , 920.02185944, 242.24430011],
                     [  0.        ,   0.        ,   1.        ]])
        distR=np.array([[-4.56781581e-01,  6.13760382e-01,  4.19512761e-04,  4.46799077e-04, -1.92449009e+00]])
        R=np.array([[ 9.99720798e-01,  5.23223467e-04, -2.36231162e-02],
                    [-1.85366840e-04,  9.99897706e-01,  1.43018752e-02],
                    [ 2.36281828e-02, -1.42935031e-02,  9.99618630e-01]])
        T=np.array([[-59.30552545],
                    [  0.09056016],
                    [  0.42453778]])
        E=np.array([[ 2.21846721e-03, -4.25788770e-01,  8.44539355e-02],
                    [ 1.82570104e+00, -8.47461585e-01,  5.92728792e+01],
                    [-7.95415963e-02, -5.92995062e+01, -8.46040909e-01]])
        F=np.array([[-3.40628961e-09,  6.52508079e-07, -2.70309936e-04],
                    [-2.79783019e-06,  1.29620844e-06, -8.27887809e-02],
                    [ 7.66496661e-04,  8.28977953e-02,  1.00000000e+00]])

        KL=np.array([[922.45198566,   0.,         317.57070143],
         [  0.,         924.16244459, 228.66603252],
         [  0.,           0.,           1.,        ]])
        distL=np.array([[-0.44497071,  0.20006589,  0.,          0.,          0.51140312]])
        KR=np.array([[922.45198566,   0.,         306.07490755],
         [  0.,         924.16244459, 240.69430766],
         [  0.,           0.,           1.,        ]])
        distR=np.array([[-0.47532508,  0.81778056,  0.,          0.,         -2.89338016]])
        R=np.array([[ 9.99942658e-01,  3.81501933e-04, -1.07021197e-02],
         [-3.69180797e-04,  9.99999267e-01,  1.15323195e-03],
         [ 1.07025518e-02, -1.14921481e-03,  9.99942066e-01]])
        T=np.array([[-5.93499276e+01],
         [ 3.76647220e-02],
         [ 5.29152796e-01]])
        E=np.array([[ 5.98461691e-04, -5.29195693e-01,  3.70523040e-02],
         [ 1.16431813e+00, -6.80039429e-02,  5.93408262e+01],
         [-1.57517087e-02, -5.93498985e+01, -6.80411407e-02]])
        F=np.array([[-8.92108636e-10,  7.87395889e-07, -2.30716939e-04],
         [-1.73240131e-06,  1.00996515e-07, -8.09197674e-02],
         [ 4.38911905e-04,  8.11939734e-02,  1.00000000e+00]])
        ucamL=pyHImageFilterFigure(240,500,80,50,"Rectify Left")
        d.addFigure(ucamL)
        #ucamL.setFilter(Undistorter(KL,distL))
        ucamL.setFilter(Rectify(KL,distL,KR,distR,R,T,left=True))
        ucamL.addPreviewFigure(d)
        cf=ucamL.getInputConnectionFigure(camL)
        d.addFigure(cf)

        ucamR=pyHImageFilterFigure(240,500,80,50,"Rectify Right")
        d.addFigure(ucamR)

        #ucamR.setFilter(Undistorter(K,dist))
        ucamR.setFilter(Rectify(KL,distL,KR,distR,R,T,left=False))
        ucamR.addPreviewFigure(d)
        cf=ucamR.getInputConnectionFigure(camR)
        d.addFigure(cf)        
       
        fmf=pyHImages2I1OFilterFigure(400,500,80,50,"FundamentalMatrix")
        d.addFigure(fmf)
        fmf.setImageSourceFigure1(ucamL)
        fmf.setImageSourceFigure2(ucamR)
        fmf.setFilter(FundamentalMatrix())
        fmf.addPreviewFigure(d,2)
       
        self.getView().setTransformFitToDrawing()

        
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
        self.addMenuAndToolBar("&File")
        self.addAction("&File","../images/fileNew.png",'New',self,"Ctrl+N","New document",self.newFile)
        self.addAction("&File","../images/fileOpen.png",'Open',self,"Ctrl+O","Open document",self.openFile)
        self.addAction("&File","../images/fileSave.png",'Save',self,"Ctrl+Q","Save document",self.saveFile)
        self.addAction("&File","",'Exit',self,"Ctrl+Q","Exit application",self.close)
        self.addMenuAndToolBar("&Edit")
        self.addAction("&Edit","../images/editCopy.png",'Copy',self,"Ctrl+C","Copy",self.copy)
        self.addAction("&Edit","../images/editCut.png",'Cut',self,"Ctrl+X","Cut",self.cut)
        self.addAction("&Edit","../images/editPaste.png",'Paste',self,"Ctrl+V","Paste",self.paste)
        self.addAction("&Edit","../images/editUndo.png",'Paste',self,"Ctrl+V","Paste",self.selectingFigures)
        self.addAction("&Edit","../images/editRedo.png",'Paste',self,"Ctrl+V","Paste",self.selectingFigures)
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
        self.addAction("&Edit","../images/zoom.png",'Zoom',self,"Ctrl+V","Zoom",self.selectingFigures)
        sceneScaleCombo = QtWidgets.QComboBox()
        sceneScaleCombo.addItems(["50%", "75%", "100%", "125%", "150%", "200%", "250%", "300%", "350%", "400%"])
        sceneScaleCombo.setCurrentIndex(2)
        sceneScaleCombo.setEditable(True)
        sceneScaleCombo.currentIndexChanged.connect(self.onScaleChanged)
        self.toolBar["&Edit"].addWidget(sceneScaleCombo)
        self.addMenuAndToolBar("&CAD")
        self.addAction("&CAD","../images/selectionTool.png",'Selection',self,"Ctrl+S","Selection Tool",self.selectingFigures,True)
        self.addAction("&CAD","../images/move.png",'View trasnlate',self,"Ctrl+v","View Translate Tool",self.viewTranslate,True)
        self.addAction("&CAD","../images/camera.png",'Camera',self,"Ctrl+S","Create Camera",self.creatingCamera,True)
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
    def saveFile(self):
        fileNames = QtWidgets.QFileDialog.getSaveFileName(self,("Save file"), QtCore.QDir.currentPath(), ("Image Files (*.phv)"))
        if not fileNames:
            fileName="default.phv"
        else:
            fileName=fileNames[0]
        drawing=self.getView().getDrawing()
        ''' picle doesn't work '''
        pickle_file = file(fileName, 'w')
        pickle.dump(drawing,pickle_file)
    def openFile(self):
        self.getView().getDrawing().clearFigures()
        fileNames = QtWidgets.QFileDialog.getOpenFileName(self,("Open file"), QtCore.QDir.currentPath(), ("Image Files (*.phv)"))
        if not fileNames:
            fileName="C:\\Users\\paco\\Desktop\\a4x2laser.dxf"
        else:
            fileName=fileNames[0]
        pickled_file = open(fileName)
        drawing = pickle.load(pickled_file)
        self.getView().setDrawing(drawing)
        self.getView().update()
        
    def updateDraw(self,item,col):
        print "item changed "+str(col)+"="+item.data(col,QtCore.Qt.DisplayRole)+" "+item.data(3,QtCore.Qt.ItemDataRole.UserRole).__class__.__name__
    def initUI(self):                       
        self.setView(pyHStandardView(self))
        
#         scrollArea = QtWidgets.QScrollArea()
#         scrollArea.setBackgroundRole(QtWidgets.QPalette.Dark)
#         scrollArea.setWidget(self.getView())
        
        self.setCentralWidget(self.getView())
        self.setGeometry(300, 30,1000,600)
        self.setWindowTitle('Qt5 - pyHotVision Stereo '+cv2.__version__)    
        self.sb=QtWidgets.QLabel(self)
        self.sb.setText("x=0,y=0")
        self.statusBar().addPermanentWidget(self.sb)
        self.sb1=QtWidgets.QLabel(self)
        self.setCurrentTool(pyHSelectionTool(self.getView()))
        self.show()
                                   
def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = pyHVisionEditor()
    
    ex.timeElapsed=dt.datetime.now()
    #ex.openDXF("a4x2laser.dxf")
    #puertos_disponibles=scan(num_ports=20,verbose=True)
    #ex.openPLT("a4x2laser.plt")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        