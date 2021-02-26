#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/07/2019

@author: paco
'''
import sys
import datetime as dt

import numpy as np
import cv2

from matrix import matrix
from robot import make_data
from PyQt5 import QtGui,QtWidgets, QtCore
from pyHotDraw.Core.Qt5.pyHStandardView import pyHStandardView
from pyHotDraw.Core.pyHAbstractEditor import pyHAbstractEditor
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Tools.pyHSelectionTool import pyHSelectionTool
from pyHotDraw.Tools.pyHCreationDropTool import pyHCreationDropTool
from pyHotDraw.Figures.pyHEllipseFigure import pyHEllipseFigure
from pyHotDraw.Figures.pyHDiamondFigure import pyHDiamondFigure
from pyHotDraw.Figures.pyHStarFigure import pyHStarFigure
from pyHotDraw.Figures.pyHTextFigure import pyHTextFigure
from pyHotDraw.Figures.pyHImageFigure import pyHImageFigure

from pyHotDraw.Geom.pyHTransform2D import pyHTransform2D

from pyHotDraw.Figures.pyHConnectionFigure import pyHConnectionFigure
from pyHotDraw.Figures.pyHGridFigure import pyHGridFigure
from pyHotDraw.Figures.pyHCompositeFigure import pyHCompositeFigure

from Figures.pyHNodeLandMarkPredictionFigure import pyHLandMarkPredictionFigure
from Figures.pyHNodePosePredictionFigure import pyHNodePosePredictionFigure
from Figures.pyHNodeLandMarkFigure import pyHNodeLandMarkFigure
from Figures.pyHNodePoseFigure import pyHNodePoseFigure
from Figures.pyHConnectionMeasureFigure import pyHConnectionMeasureFigure
from Figures.pyHNodeLandMarkMeasureFigure import pyHNodeLandMarkMeasureFigure
from Figures.pyHNodePoseMeasureFigure import pyHNodePoseMeasureFigure

# ######################################################################

# --------------------------------
#
# full_slam - retains entire path and all landmarks
#             Feel free to use this for comparison.
#

# def setSubmatrix(Omega,Xi,pn,pm,dataOmega,dataXi):
#     subDim=2
#     n=subDim*int(pn)
#     m=subDim*int(pm)
#     for b in range(2):
#         Omega.value[n+b][n+b] +=  dataOmega
#         Omega.value[m+b][m+b] +=  dataOmega
#         Omega.value[n+b][m+b] += -dataOmega
#         Omega.value[m+b][n+b] += -dataOmega
#         Xi.value[n+b][0]      += -dataXi[b]
#         Xi.value[m+b][0]      +=  dataXi[b]
#     
# def buildInformationMatrix(data, N, num_landmarks, motion_noise, measurement_noise):
#     # Set the dimension of the filter
#     dim = 2 * (N + num_landmarks) 
#     # make the constraint information matrix and vector
#     Omega = matrix()
#     Omega.zero(dim, dim)
#     Omega.value[0][0] = 1.0
#     Omega.value[1][1] = 1.0
# 
#     Xi = matrix()
#     Xi.zero(dim, 1)
#     Xi.value[0][0] = world_size / 2.0
#     Xi.value[1][0] = world_size / 2.0
#     
#     # process the data
#     for n in range(len(data)):
#         # n is the index of the robot pose in the matrix/vector
#         measurement = np.array(data[n][0])
#         motion      = np.array(data[n][1])
#         # integrate the measurements
#         for i in range(len(measurement)):
#             # m is the index of the landmark coordinate in the matrix/vector
#             lid=measurement[i][0] 
#             measurements=measurement[i][1:]
#             m =  (N + lid) 
#             # update the information maxtrix/vector based on the measurement
#             setSubmatrix(Omega,Xi,n,m,1.0 / measurement_noise,measurements/measurement_noise)
#         # update the information maxtrix/vector based on the robot motion
#         # next pose id
#         pid=motion[0] 
#         # delta motino from pose n to pose pid
#         dMotion=motion[1:]
#         m=pid # m is always next there is not closeloop
#         setSubmatrix(Omega,Xi,n,m,1.0/motion_noise,dMotion/motion_noise)
#     return Omega,Xi

from pyLinearGraphSLAM import pyLinearGraphSLAM
from pyHotDraw.Images.pyHImage import pyHImage

def buildInformationMatrixNew(data, N, num_landmarks, motion_noise, measurement_noise):
    # Set the dimension of the filter
    lgs=pyLinearGraphSLAM(2,(world_size/2.0,world_size/2.0))    
    # process the data
    for n in range(len(data)):
        # n is the index of the robot pose in the matrix/vector
        measurement = np.array(data[n][0])
        motion      = np.array(data[n][1])
        # integrate the measurements
        for i in range(len(measurement)):
            # m is the index of the landmark coordinate in the matrix/vector
            lid=measurement[i][0] 
            measurements=measurement[i][1:]
            lgs.setPose2MeasurementEdge(n,lid,measurements,measurement_noise)
        # update the information maxtrix/vector based on the robot motion
        # next pose id
        pid=motion[0] 
        # delta motino from pose n to pose pid
        dMotion=motion[1:]
        m=pid # m is always next there is not closeloop
        lgs.setPose2PoseEdge(n,m, dMotion, motion_noise)
    return lgs.Omega,lgs.Xi,lgs

def solve(Omega,Xi):
    # compute best estimate
    mu = Omega.inverse() * Xi
    return mu

def slam(data, N, num_landmarks, motion_noise, measurement_noise):
    # Build the information matrix
    Omega,Xi,g=buildInformationMatrixNew(data, N, num_landmarks, motion_noise, measurement_noise)
    # compute best estimate
    #mu = solve(Omega,Xi)
    mu = g.solve()
    # return the result
    return mu, Omega, Xi,g


# --------------------------------
#
# print the result of SLAM, the robot pose(s) and the landmarks
#

def print_result(N, num_landmarks, result):
    print
    print 'Estimated Pose(s):'
    for i in range(N):
        print '    ['+ ', '.join('%.3f'%x for x in result.value[2*i]) + ', ' \
            + ', '.join('%.3f'%x for x in result.value[2*i+1]) +']'
    print 
    print 'Estimated Landmarks:'
    for i in range(num_landmarks):
        print '    ['+ ', '.join('%.3f'%x for x in result.value[2*(N+i)]) + ', ' \
            + ', '.join('%.3f'%x for x in result.value[2*(N+i)+1]) +']'

# ------------------------------------------------------------------------
#
# Main routines
#

N                  = 5       # time steps
num_landmarks      = 2#int(N/3) # number of landmarks
world_size         = 200.0    # size of world
measurement_range  = 50.0     # range at which we can sense landmarks
motion_noise       = 5.0      # noise in robot motion
measurement_noise  = 1.0      # noise in the measurements
distance           = 50.0     # distance by which robot (intends to) move each iteratation 

class pyHInformationMatrixFigure(pyHCompositeFigure):
    def __init__(self,g):
        pyHCompositeFigure.__init__(self)
        ''' build information matrix figure '''
        d=self
        #Units metres
        cellSize=3
        # HEADER
        Xi=g.Xi
        Omega=g.Omega
        NM=g.N+g.L
        NM2=NM*g.subDim
        gf=pyHGridFigure(100,NM2*cellSize,1,NM,cellSize*2,cellSize*2)
        for i in range(NM):
            if i>N-1:
                tf=pyHTextFigure(0,0,cellSize*2,cellSize*2,i-N)
                tf.setColor(0,0,255)
            else:
                tf=pyHTextFigure(0,0,cellSize*2,cellSize*2,i)                
            gf.addFigure(tf)
        d.addFigure(gf)
        # BODY
        # Xi grid figure
        XiFigure=pyHGridFigure(100+NM2*cellSize,0,NM2,1,cellSize*2,cellSize)
        d.addFigure(XiFigure)
        for i in range(NM2):
            if abs(Xi.value[i][0])>0.000001:
                tf=pyHTextFigure(0,0,cellSize*2,cellSize,Xi.value[i][0])
                tf.setFillColor(255, 255, 255)
            else:
                tf=pyHTextFigure(0,0,cellSize*2,cellSize,"0.00")   
            XiFigure.addFigure(tf)
        # Omega grid figure       
        OmegaFigure=pyHGridFigure(100,0,NM2,NM2,cellSize,cellSize)
        for i in range(NM2):
            for j in range(NM2):
                if abs(Omega.value[i][j])>0.000001:
                    tf=pyHTextFigure(0,0,cellSize,cellSize,Omega.value[i][j])
                    tf.setFillColor(255,255,200)
                    if i>N*2-1 or j>N*2-1:
                        tf.setColor(0,0,255)
                else:
                    tf=pyHTextFigure(0,0,cellSize,cellSize," ")
                    if i>N*2-1 or j>N*2-1:
                        tf.setColor(0,0,255,50)
                    else:
                        tf.setColor(0,0,0,50)
                OmegaFigure.addFigure(tf)
        d.addFigure(OmegaFigure)
        
class pyHGraphSLAMEditor(QtWidgets.QMainWindow,pyHAbstractEditor):
    def __init__(self):
        super(pyHGraphSLAMEditor, self).__init__()
        pyHAbstractEditor.__init__(self)
        self.initActionMenuToolBars()
        self.statusBar()        
        self.initUI()
        self.getView().setDrawingGrid(False)
        pyImg=pyHImage("itc_corridors_2020030301.jpg")
        #pyImg=pyHImage("../images/20200923_095151.jpg")
        bf=pyHImageFigure(0,0,160*2,140,pyImg)
        self.getView().setBackground(bf)
        # Init data
        self.data,self.r = make_data(N, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)
        data=self.data
        r=self.r
        result,Omega,Xi,g = slam(data, N, num_landmarks, motion_noise, measurement_noise)
        print_result(N, num_landmarks, result)

        d=self.getView().getDrawing()
#         ''' build information matrix figure '''
        imf=pyHInformationMatrixFigure(g)
        d.addFigure(imf)
        txt=pyHTextFigure(45,100,20,3.5," pyHotGraphSLAM ",border=True)
        d.addFigure(txt)
        ''' s h o w   p r e d i c t i o n s '''
        self.showPredictions(g)        
        ''' show last groundtruth pose '''
        rf=pyHStarFigure(r.x,r.y,0.5,1.5,5)
        rf.setColor(0,255,0)
        rf.setWidth(4)
        d.addFigure(rf)
        ''' s h o w landmarks groundtruth  '''
        ''' Just the map '''
        landmarks=[]
        for i,(x,y) in enumerate(self.r.landmarks):
            #x=result.value[2*(N+i)][0]
            #y=result.value[2*(N+i)+1][0]
            f=pyHNodeLandMarkFigure(x-0.5,y-0.5,4,4,i)
            f.setColor(100,100,100)
            f.setFillColor(255, 255, 230,100)
            d.addFigure(f)
            landmarks.append(f)
            
        ''' s h o w   g r a p h  '''
        x=world_size/2
        y=world_size/2
        fs=pyHNodePoseFigure(x-0.5,y-0.5,5,5,0)
        d.addFigure(fs)
        for k in range(len(data)):

            # n is the index of the robot pose in the matrix/vector
            n = k * 2 
        
            measurement = data[k][0]
            motion      = data[k][1]
        
            # integrate the measurements
            for i in range(len(measurement)):
                idx=measurement[i][0]
                mdx=measurement[i][1]
                mdy=measurement[i][2]
                mx=x+mdx
                my=y+mdy
                lmf=pyHNodeLandMarkMeasureFigure(mx-1,my-1,2,2,idx)
                d.addFigure(lmf)
                cf=pyHConnectionFigure()
                cf.setColor(0,0,255,100)
                cf.connectFigures(fs, lmf)
                d.addFigure(cf)
                f=landmarks[idx] #pyHNodeLandMarkFigure(mx-0.25,my-0.25,2.0,2.0,idx)
                cf=pyHConnectionFigure()
                cf.setColor(100,0,0,100)
                cf.connectFigures(lmf, f)
                d.addFigure(cf)
                #d.addFigure(plm)
            pid=motion[0]
            dx =motion[1]
            dy =motion[2]
            x+=dx
            y+=dy
            nmf=pyHNodePoseMeasureFigure(x-1,y-1,2,2,pid)
            d.addFigure(nmf)
            cf=pyHConnectionFigure()
            cf.setColor(0,100,0,100)
            cf.connectFigures(fs, nmf)
            d.addFigure(cf)
            #print x,y,dx,dy
            fe=pyHNodePoseFigure(x-2.5,y-2.5,5,5,k+1)
            d.addFigure(fe)
            cf=pyHConnectionFigure()
            cf.setColor(100,0,0,100)
            cf.connectFigures(nmf, fe)
            d.addFigure(cf)
            fs=fe

            
        self.getView().setTransformFitToDrawing()

 
    def showPredictions(self,g):
        ''' show predictions '''
        result=g.mu
        #d=self.getView().getDrawing()
        # predictions
        self.lanmarkFigures=[]
        self.predictionFigures=pyHCompositeFigure()
        d=self.predictionFigures
        i=0
        x=result.value[2*i][0]
        y=result.value[2*i+1][0]
        fs=pyHLandMarkPredictionFigure(x-0.5,y-0.5,5,5,i)
        fs.setColor(255,0,0)
        d.addFigure(fs)
        # motion prediction
        for i in range(1,N):
            x=result.value[2*i][0]
            y=result.value[2*i+1][0]
            fe=pyHNodePosePredictionFigure(x-0.5,y-0.5,5,5,i)
            fe.setColor(255,0,0)
            d.addFigure(fe)
            cf=pyHConnectionFigure()
            cf.setColor(255,0,0,100)
            cf.connectFigures(fs, fe)
            d.addFigure(cf)
            fs=fe
        # landmark prediction
        for i in range(num_landmarks):
            x=result.value[2*(N+i)][0]
            y=result.value[2*(N+i)+1][0]
            f=pyHLandMarkPredictionFigure(x-0.5,y-0.5,2,2,i)
            f.setColor(0,0,255)
            d.addFigure(f)
        self.getView().getDrawing().addFigure(d)
               
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

    def creatingEllipse(self):
        f=pyHEllipseFigure(0,0,1.5,1.5)
        self.setCurrentTool(pyHCreationDropTool(self.getView(),f))
    def creatingDiamond(self):
        f=pyHDiamondFigure(0,0,1.5,1.5)
        f.setColor(100,100,100,100)
        self.setCurrentTool(pyHCreationDropTool(self.getView(),f))
    # it doesn't work pickle error on phPoint in pyHStarFigure
    def creatingStar(self):
        self.setCurrentTool(pyHCreationDropTool(self.getView(),pyHStarFigure(0,0,50,150)))
                
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
        self.addAction("&CAD","../images/createLineConnection.png",'Create connection',self,"Ctrl+S","Create connection Tool",self.creatingLineConnection,True)
        self.addAction("&CAD","../images/createEllipse.png",'Ellipse',self,"Ctrl+S","Selection Tool",self.creatingEllipse,True)
        self.addAction("&CAD","../images/star.png",'Diamond',self,"Ctrl+S","Star",self.creatingStar,True)
        self.addAction("&CAD","../images/createDiamond.png",'Diamond',self,"Ctrl+S","Selection Tool",self.creatingDiamond,True)
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
        fileNames = QtWidgets.QFileDialog.getOpenFileName(self,("Open GraphSLAM"), QtCore.QDir.currentPath(), ("Files (*.phgs)"))
        if not fileNames:
            fileName="default.phgs"
        else:
            fileName=fileNames[0]
        self.saveFileName(fileName)
        self.getView().update()
    def saveFile(self):
        self.getView().getDrawing().clearFigures()
        fileNames = QtWidgets.QFileDialog.getSaveFileName(self,("Save GraphSLAM"), QtCore.QDir.currentPath(), ("Files (*.phgs)"))
        if not fileNames:
            fileName="default.phgs"
        else:
            fileName=fileNames[0]
        self.saveFileName(fileName)
        self.getView().update()
         
    def updateDraw(self,item,col):
        print "item changed "+str(col)+"="+item.data(col,QtCore.Qt.DisplayRole)+" "+item.data(3,QtCore.Qt.ItemDataRole.UserRole).__class__.__name__

    def initUI(self):                       
        self.setView(pyHStandardView(self))
        self.getView().setTransform(pyHTransform2D(10,10,self.width()/2,self.height()/2))
        
        self.setCentralWidget(self.getView())
        self.setGeometry(300, 30,900,900)
        self.setWindowTitle('Qt5 - pyHotGraphSLAM')    
        self.sb=QtWidgets.QLabel(self)
        self.sb.setText("x=0,y=0")
        self.statusBar().addPermanentWidget(self.sb)
        self.sb1=QtWidgets.QLabel(self)
        self.setCurrentTool(pyHSelectionTool(self.getView()))
        self.show()

                                   
def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = pyHGraphSLAMEditor()  
    ex.timeElapsed=dt.datetime.now()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        