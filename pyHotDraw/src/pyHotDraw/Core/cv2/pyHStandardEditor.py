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

import pyHotDraw
from pyHotDraw.Core.cv2.pyHStandardView import pyHStandardView
from pyHotDraw.Core.pyHAbstractEditor import pyHAbstractEditor
from pyHotDraw.Tools.pyHSelectionTool import pyHSelectionTool
from pyHotDraw.Figures.pyHPolylineFigure import pyHPolylineFigure
from pyHotDraw.Figures.pyHSplineFigure import pyHSplineFigure
from pyHotDraw.Figures.pyHEllipseFigure import pyHEllipseFigure
from pyHotDraw.Figures.pyHArcFigure import pyHArcFigure
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
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
from pyHotDraw.Geom.pyHTransform2D import pyHTransform2D

class pyHStandardEditor(pyHAbstractEditor):
    def __init__(self,title):
        super(pyHStandardEditor, self).__init__() 
        self.title=title
        self.img=np.zeros((480,640,3), np.uint8)    
        self.img[:]=255  
        self.initUI()
        
        d=self.getView().getDrawing()
        
        txt=pyHTextFigure(100,200,20,20,"Hola Caracola")
        d.addFigure(txt)
      
        rf=pyHRectangleFigure(10,10,40,40)
        rf.setColor(255,0,0)
        d.addFigure(rf)
        
        
        cam=pyHCameraFigure(0,50,50,50,0)
        d.addFigure(cam)
        img0=pyHImageFigure(250,60,320,240)
        cam.addChangedImageObserver(img0)
        d.addFigure(img0)
        
        #self.getView().setTransformFitToDrawing()
        
#Redefinning abstract methods
    def createMenuBar(self):
        pass
    def addMenuAndToolBar(self,name):
        pass
    def addAction(self,menuName,icon,name,container,sortCut,statusTip,connect,addToActionGroup=False):
        pass        
    def initActionMenuToolBars(self):
        pass
    
    def onScaleChanged(self,index):
        s=float(index)
        t=self.getView().getTransform()
        t.sx=s+0.50
        t.sy=s+0.50
        self.getView().update()
    def newFile(self):
        pass
    def openFile(self):
        pass
        
    def updateDraw(self,item,col):
        pass
    def initUI(self):                       
        self.setView(pyHStandardView(self))
        #this command before than the next in order to make transform working
        self.getView().setTransform(pyHTransform2D(1,1))
        self.getView().setImg(self.img)

        cv2.namedWindow(self.title)

def main():
    ex = pyHStandardEditor("pyHotDraw.cv2-"+cv2.__version__)
    while(1):
        cv2.imshow(ex.title,ex.img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()        