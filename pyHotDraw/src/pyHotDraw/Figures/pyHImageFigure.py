#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 17/04/2015

@author: Francisco Dominguez
+03/02/2016
'''
import numpy as np
import cv2
from PyQt4 import QtCore
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHAbstractFigure import pyHAbstractFigure
from pyHRectangleFigure import pyHRectangleFigure
from pyHArrowFigure import pyHArrowFigure
from pyHEllipseFigure import pyHEllipseFigure
from pyHotDraw.Images.pyHImage import pyHImage
from pyHotDraw.Images.pyHImageFilters import *
class pyHImageFigure(pyHRectangleFigure):
    def __init__(self,x0,y0,w,h,img=None):
        super(pyHImageFigure,self).__init__(x0,y0,w,h)
        if img!=None:
            self.img=img
        else:
            self.setImage(pyHImage())
        self.imageSourceFigure=None
    def setImageSourceFigure(self,imageSourceFigure):
        if self.imageSourceFigure!=None:
            self.imageSourceFigure.removeChangedImageObserver(self)
        self.imageSourceFigure=imageSourceFigure
        imageSourceFigure.addChangedImageObserver(self)
    def setImage(self,img):
        self.img=img
        self.notifyFigureChanged()
    def getImage(self):
        return self.img
    def draw(self,g):
        super(pyHImageFigure,self).draw(g)
        #pyHAbstractFigure.draw(self,g)
        g.drawImage(self.x0,self.y0,self.w,self.h,self.img)
    def imageChanged(self,fImageSource):
        self.setImage(fImageSource.getImage())
    #visitor method
    def visit(self,visitor):
        return visitor.visitImageFigure(self)
class pyHImageDottedFigure(pyHImageFigure):
    def __init__(self,x0,y0,w,h,img=None,points=None):
        super(pyHImageDottedFigure,self).__init__(x0,y0,w,h,img)
        #points are in image coordiantes not in this rectangle coordinates
        #sx and sy scale in order to make coordinates change
        self.sx=float(self.w)/float(self.getImage().getWidth())
        self.sy=float(self.h)/float(self.getImage().getHeight())
        self.points=[]
    def setImage(self,img):
        self.img=img
        self.sx=float(self.w)/float(self.getImage().getWidth())
        self.sy=float(self.h)/float(self.getImage().getHeight())
        self.notifyFigureChanged()
    def draw(self,g):
        super(pyHImageDottedFigure,self).draw(g)
        for p in self.points:
            g.setColor(255,255,0)
            g.drawEllipse(self.x0+p.getX()*self.sx-2,(self.y0+self.h)-p.getY()*self.sy-2,4,4)
    def getPoints(self):
        return self.points
    def setPoints(self,points):
        self.points=points
    def addPoint(self,p):
        self.points.append(p)
    def imageChanged(self,fImageSource):
        self.setImage(fImageSource.getImage())
        #self.setPoints([pyHPoint(x,y) for x,y in fImageSource.getPoints()])
class pyHImagesMixedFigure(pyHImageFigure):
    """ This class has two images and mix them """
    def __init__(self,x0,y0,w,h,img=None,points=None):
        super(pyHImagesMixedFigure,self).__init__(x0,y0,w,h,img)
        self.filter=MixImages()
        self.imageSourceFigure=None
        self.imageSourceFigure2=None
    def setImageSourceFigure1(self,imageSourceFigure):
        if self.imageSourceFigure!=None:
            self.imageSourceFigure.removeChangedImageObserver(self)
        self.imageSourceFigure=imageSourceFigure
        imageSourceFigure.addChangedImageObserver(self)
    def setImageSourceFigure2(self,imageSourceFigure):
        if self.imageSourceFigure2!=None:
            self.imageSourceFigure2.removeChangedImageObserver(self)
        self.imageSourceFigure2=imageSourceFigure
        imageSourceFigure.addChangedImageObserver(self)
    def setFilter(self,filter):
        self.filter=filter
    def setImage(self,img):
        self.img=img
        self.notifyFigureChanged()
    def setImage1(self,img):
        self.img=img
        self.notifyFigureChanged()
    def setImage2(self,img):
        self.img2=img
        self.notifyFigureChanged()
    def draw(self,g):
        #super(pyHImageDottedFigure,self).draw(g)
        self.filter.imgcv1=self.img.getData()
        self.filter.imgcv2=self.img2.getData()
        imgcv=self.filter.process()
        hImg=pyHImage()
        hImg.setData(imgcv)
        g.drawImage(self.x0,self.y0,self.w,self.h,hImg)
    def imageChanged(self,fImageSource):
        if fImageSource==self.imageSourceFigure:
            self.setImage(fImageSource.getImage())
        if fImageSource==self.imageSourceFigure2:
            self.setImage2(fImageSource.getImage())
class pyHImageFilterFigure(pyHArrowFigure):
    def __init__(self,x0,y0,w,h):
        #super(pyHImageFilterFigure,self).__init__(x0,y0,w,h)
        super(pyHImageFilterFigure,self).__init__(x0,y0,w,h)
        self.changedImageObservers=[]
        self.imageSink=None
        self.imageFilter=FaceDetection()
    def setFilter(self,imageFilter):
        self.imageFilter=imageFilter
    def getImage(self):
        return self.imageSink
    def launchFilter(self,hImgI):
        #get numpy or cv2 image from pyHImage and make a new copy
        matI=hImgI.getData()
        #lauch the filter and get theh numpy or cv2 image
        matO=self.imageFilter.process(matI)
        #build a new pyHImage
        hImgO=pyHImage()
        #set internal image to this pyHImage
        hImgO.setData(matO)
        return hImgO     
    def imageChanged(self,img):
        self.imageSink=self.launchFilter(img.getImage())
        self.notifyImageChanged()
# Observer pattern methods
    def addChangedImageObserver(self,fo):  
        self.changedImageObservers.append(fo)
    def removeChangedImageObserver(self,fo):  
        self.changedImageObservers.remove(fo)
    def notifyImageChanged(self):
        if self.imageSink!=None:
            for fo in self.changedImageObservers:
                fo.imageChanged(self)   
class pyHImageSecFilterFigure(pyHImageFilterFigure):
    """ Apply a two input filter to the actual image and previous image """
    def __init__(self,x0,y0,w,h):
        super(pyHImageSecFilterFigure,self).__init__(x0,y0,w,h)
    def launchFilter(self,hImg1,hImg2):
        mat1=hImg1.getData()
        mat2=hImg2.getData()
        self.imageFilter.imgcv1=mat1
        self.imageFilter.imgcv2=mat2
        matO=self.imageFilter.process()
        hImgO=pyHImage()
        hImgO.setData(matO)
        return hImgO     
    def imageChanged(self,fImageSource):
        self.imageSink=self.launchFilter(fImageSource.getImagePrev(),fImageSource.getImage())
        self.notifyImageChanged()
class pyHImages2I1OFilterFigure(pyHImageSecFilterFigure):
    """ This class filter has two images as input and one image as output """
    def __init__(self,x0,y0,w,h):
        super(pyHImages2I1OFilterFigure,self).__init__(x0,y0,w,h)
        self.imageSourceFigure=None
        self.imageSourceFigure2=None
    def setImageSourceFigure1(self,imageSourceFigure):
        if self.imageSourceFigure!=None:
            self.imageSourceFigure.removeChangedImageObserver(self)
        self.imageSourceFigure=imageSourceFigure
        imageSourceFigure.addChangedImageObserver(self)
    def setImageSourceFigure2(self,imageSourceFigure):
        if self.imageSourceFigure2!=None:
            self.imageSourceFigure2.removeChangedImageObserver(self)
        self.imageSourceFigure2=imageSourceFigure
        imageSourceFigure.addChangedImageObserver(self)
    def imageChanged(self,fImageSource):
        """ TO FINISH """
        if fImageSource==self.imageSourceFigure:
            self.setImage(fImageSource.getImage())
        if fImageSource==self.imageSourceFigure2:
            self.setImage2(fImageSource.getImage())
        self.imageSink=self.launchFilter(fImageSource.getImagePrev(),fImageSource.getImage())
        self.notifyImageChanged()

class pyHImageSourceFigure(pyHEllipseFigure):  
    def __init__(self,x,y,w,h):
        super(pyHImageSourceFigure,self).__init__(x,y,w,h) 
        self.changedImageObservers=[]
        self.hImg=pyHImage()
        self.hImgPrev=pyHImage()
    def setImage(self,hImg):
        self.hImgPrev=self.hImg
        self.hImg=hImg
    def getImage(self):
        return self.hImg
    def getImagePrev(self):
        return self.hImgPrev
#Observer pattern methods
    def addChangedImageObserver(self,fo):  
        self.changedImageObservers.append(fo)
    def removeChangedImageObserver(self,fo):  
        self.changedImageObservers.remove(fo)
    def notifyImageChanged(self):
        for fo in self.changedImageObservers:
            fo.imageChanged(self)        
class pyHCameraFigure(pyHImageSourceFigure):
    def __init__(self,x,y,w=50,h=40,camID=0):
        super(pyHCameraFigure,self).__init__(x,y,w,h)
        #pyHImageSourceFigure.__init__(self, x, y, w, h)
        """Initialize camera."""
        self.capture = cv2.VideoCapture(camID)
        self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.displayVideoStream)
        self.timer.start(200)
    def displayVideoStream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        _, frame = self.capture.read()
        #save this image to previous image
        img=self.getImage().getData()
        self.getImagePrev().setData(img)
        self.getImage().setData(frame)
        self.notifyImageChanged()
         