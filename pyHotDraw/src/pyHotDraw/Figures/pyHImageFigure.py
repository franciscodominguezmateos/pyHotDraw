#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 17/04/2015

@author: Francisco Dominguez
+03/02/2016
'''
from threading import Timer
import numpy as np
import cv2
#from PyQt5 import QtCore
from pyHotDraw.Core.pyHExceptions import pyHFigureNotFound
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHAbstractFigure import pyHAbstractFigure
from pyHRectangleFigure import pyHRectangleFigure
from pyHArrowFigure import pyHArrowFigure
from pyHEllipseFigure import pyHEllipseFigure
from pyHConnectionFigure import pyHConnectionFigure
from pyHotDraw.Images.pyHImage import pyHImage
from pyHotDraw.Images.pyHImageFilters import *
from pyHotDraw.Figures.pyHTextFigure import pyHTextFigure
class pyHImageFigure(pyHRectangleFigure):
    def __init__(self,x0,y0,w,h,img=None):
        super(pyHImageFigure,self).__init__(x0,y0,w,h)
        if img is None:
            self.setImage(pyHImage())
        else:
            self.img=img
        self.border=True
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
        if self.border:
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
    def __init__(self,x0,y0,w,h,text="ImageFilter"):
        #super(pyHImageFilterFigure,self).__init__(x0,y0,w,h)
        super(pyHImageFilterFigure,self).__init__(x0,y0,w,h)
        self.changedImageObservers=[]
        self.imageSink=None
        self.imageFilter=FaceShapeDetection()
        #self.outputConnectionFigure=None #more than one output allowed
        self.textFigure=pyHTextFigure(x0,y0,w,h,text,border=False)
        self.inputConnectionFigure=None
    def draw(self,g):
        pyHArrowFigure.draw(self,g)
        self.textFigure.setDisplayBox(self.getDisplayBox())
        self.textFigure.draw(g)
    def addPreviewFigure(self,drawing):
        r=self.getDisplayBox()
        pc=r.getCenterPoint()
        img0=pyHImageFigure(pc.getX()-240/2,pc.getY()-r.getHeight()-320-10,320,240)
        drawing.addFigure(img0)
        #cam.addChangedImageObserver(img0)
        cf=self.getOutputConnectionFigure(img0)
        drawing.addFigure(cf)  
    #TODO create a connectionFigure from filter to f
    #     f must be a image observer
    def getOutputConnectionFigure(self,f):
        #if self.outputConnectionFigure!=None:
        #    raise Exception("outputConnectionFigure already exist")
        if not 'imageChanged' in set(dir(f)):
            raise pyHFigureNotFound("Figure is not an image observer")
        #this may not be necessary
        self.addChangedImageObserver(f)
        
        cf=pyHConnectionFigure()
        #self.outputConnectionFigure=cf

        fr=f.getDisplayBox()
        fpc=fr.getCenterPoint()
        cStart=self.findConnector(fpc) 
        cStart.getOwner().addChangedFigureObserver(cf)
        cf.setConnectorStart(cStart)
        p0=cStart.findStart(cf)
        cf.addPoint(p0)
        
        sr=self.getDisplayBox()
        spc=sr.getCenterPoint()
        cEnd=f.findConnector(spc)
        cEnd.getOwner().addChangedFigureObserver(cf)
        cf.setConnectorEnd(cEnd)
        p1=cEnd.findEnd(self)
        cf.addPoint(p1)
        return cf
    def getInputConnectionFigure(self,f):
        if self.inputConnectionFigure!=None:
            raise Exception("inputConnectionFigure already exist")
        #if not 'imageChanged' in set(dir(f)):
        #    raise pyHFigureNotFound("Figure is not an image observer")
        #this may not be necessary
        f.addChangedImageObserver(self)
        
        cf=pyHConnectionFigure()
        self.inputConnectionFigure=cf

        fr=f.getDisplayBox()
        fpc=fr.getCenterPoint()
        cEnd=self.findConnector(fpc) 
        cEnd.getOwner().addChangedFigureObserver(cf)
        cf.setConnectorEnd(cEnd)
        p0=cEnd.findStart(cf)
        cf.addPoint(p0)
        
        sr=self.getDisplayBox()
        spc=sr.getCenterPoint()
        cStart=f.findConnector(spc)
        cStart.getOwner().addChangedFigureObserver(cf)
        cf.setConnectorStart(cStart)
        p1=cStart.findStart(self)
        cf.addPoint(p1)
        return cf
           
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
        self.width=w
        self.height=h
    def setImage(self,hImg):
        self.hImgPrev=self.hImg
        self.hImg=hImg
    def getImage(self):
        return self.hImg
    def getImagePrev(self):
        return self.hImgPrev
    def addPreviewFigure(self,drawing):
        r=self.getDisplayBox()
        pc=r.getCenterPoint()
        img0=pyHImageFigure(pc.getX()-240/2,pc.getY()-r.getHeight()-320-10,320,240)
        drawing.addFigure(img0)
        #cam.addChangedImageObserver(img0)
        cf=self.getOutputConnectionFigure(img0)
        drawing.addFigure(cf)  
    def getOutputConnectionFigure(self,f):
        if not 'imageChanged' in set(dir(f)):
            raise pyHFigureNotFound("Figure is not an image observer")
        #this may not be necessary
        self.addChangedImageObserver(f)
        
        cf=pyHConnectionFigure()
        self.outputConnectionFigure=cf

        fr=f.getDisplayBox()
        fpc=fr.getCenterPoint()
        cStart=self.findConnector(fpc) 
        cStart.getOwner().addChangedFigureObserver(cf)
        cf.setConnectorStart(cStart)
        p0=cStart.findStart(cf)
        cf.addPoint(p0)
        
        sr=self.getDisplayBox()
        spc=sr.getCenterPoint()
        cEnd=f.findConnector(spc)
        cEnd.getOwner().addChangedFigureObserver(cf)
        cf.setConnectorEnd(cEnd)
        p1=cEnd.findEnd(self)
        cf.addPoint(p1)
        return cf
#Observer pattern methods
    def addChangedImageObserver(self,fo):  
        self.changedImageObservers.append(fo)
    def removeChangedImageObserver(self,fo):  
        self.changedImageObservers.remove(fo)
    def notifyImageChanged(self):
        for fo in self.changedImageObservers:
            fo.imageChanged(self)        
class pyHCameraFigure(pyHImageSourceFigure):
    def __init__(self,x,y,w=80,h=40,camID=0,text=" Camera "):
        super(pyHCameraFigure,self).__init__(x,y,w,h)
        #pyHImageSourceFigure.__init__(self, x, y, w, h)
        """Initialize camera."""
        self.camID=camID
        self.capture = cv2.VideoCapture(camID)
        #figure width and height same that image width and hegight. ????
        #self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        #self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
#         self.timer = QtCore.QTimer()
#         self.timer.timeout.connect(self.displayVideoStream)
#         self.timer.start(200)
        self.timer = Timer(0.2,self.displayVideoStream)
        self.timer.start()
        self.textFigure=pyHTextFigure(x,y,w,h,text,border=False)
        self.inputConnectionFigure=None
    def draw(self,g):
        super(pyHCameraFigure,self).draw(g)
        self.textFigure.setDisplayBox(self.getDisplayBox())
        self.textFigure.draw(g)
        
    def displayVideoStream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        self.timer = Timer(0.2,self.displayVideoStream)
        self.timer.start()
        ret, frame = self.capture.read()
        if ret==False:
            self.capture = cv2.VideoCapture(self.camID)            
            ret, frame = self.capture.read()
            print "displayVideoStream capture error"
        #save this image to previous image
        img=self.getImage().getData()
        self.getImagePrev().setData(img)
        self.getImage().setData(frame)
        self.notifyImageChanged()
         