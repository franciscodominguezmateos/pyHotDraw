#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 25/03/2013

@author: paco
'''
import cv2
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QImage

class pyHStandardGraphic:
    def __init__(self,qp,v):
        self.qPainter=qp
        #qp.setPen(QtWidgets.QPen(QtCore.Qt.green, 3, QtCore.Qt.DashDotLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        self.t=v.getTransform()
        self.v=v
    def getTransformation(self):
        return self.t
    def setTransformation(self,t):
        self.t=t
    def drawLine(self,x0,y0,x1,y1):
        h=self.v.height()
        x0,y0=self.t.transform(x0,y0)
        x1,y1=self.t.transform(x1,y1)
        self.qPainter.drawLine(x0,h-y0,x1,h-y1)
    def drawRect(self,x0,y0,rx,ry):
        h=self.v.height()
        x0,y0=self.t.transform(x0,y0)
        rx=self.t.sx*rx
        ry=self.t.sy*ry
        self.qPainter.drawRect(x0,h-y0,rx,-ry)
    def drawRoundedRect(self,x0,y0,rx,ry):
        h=self.v.height()
        x0,y0=self.t.transform(x0,y0)
        rx=self.t.sx*rx
        ry=self.t.sy*ry
        self.qPainter.drawRoundedRect(x0,h-y0,rx,-ry,20.0,20.0)
    def drawEllipse(self,x0,y0,rx,ry):
        h=self.v.height()
        x0,y0=self.t.transform(x0,y0)
        rx=self.t.sx*rx
        ry=self.t.sy*ry
        self.qPainter.drawEllipse(x0,h-y0,rx,-ry)
    def drawArc(self,x0,y0,rx,ry,ans,ane):
        h=self.v.height()
        x0,y0=self.t.transform(x0,y0)
        rx=self.t.sx*rx
        ry=self.t.sy*ry
        if ane>ans:
            anl=ane-ans
        else:
            anl=360+(ane-ans)
            anl=-anl
            ans=ane
        #angles are counterclockwise in Qt and unit is 1/16º
        self.qPainter.drawArc(x0,h-y0,rx,-ry,ans*16,anl*16)
    def drawPoint(self,x0, y0):
        h=self.v.height()
        x0,y0=self.t.transform(x0,y0)
        self.qPainter.drawPoint(x0,h-y0)
    def drawText(self,x,y,rx,ry,text):
        h=self.v.height()
        x0,y0=self.t.transform(x,y)
        rx,ry=self.t.scale(rx,ry)
        f=self.qPainter.font()
        m=self.qPainter.fontMetrics()
        # before resizing
        tw=m.width(text)
        th=m.height()
        ch=(ry-th)/2
        rate=rx/tw
        f.setPointSizeF(f.pointSizeF()*rate)
        self.qPainter.setFont(f)
        # after resizing vertical center. triky!!!
        m=self.qPainter.fontMetrics()
        ts=m.size(0,text) #m.width(text)
        tw=ts.width()
        th=ts.height()*0.55 # 55??? it works
        if ry>th: ch=(ry-th)/2
        else: ch=0
        self.qPainter.drawText(x0,h-(y0+ch),text)
        #self.qPainter.drawRect(x0,h-y0,m.width(text),-m.height())
    def drawImage(self,x,y,rx,ry,hImg):
        h=self.v.height()
        x0,y0=self.t.transform(x,y)
        #rx=self.t.sx*rx
        #ry=self.t.sy*ry
        rx,ry=self.t.scale(rx,ry)
        #self.qPainter.drawRect(x0,h-y0,rx,-ry)
        r=QRectF(x0,h-y0-ry,rx,ry)
        qImg=hImg.convertMatToQImage(rx,ry)
        #r=QRectF(x0,h-y0-ry,qImg.width()/2,qImg.height()/2)
        #qImg=QImage('../images/im2.png')
        #mat=hImg.convertQImageToMat(qImg)
        #cv2.imshow('nada',hImg.getData())
        #print mat.shape
        #qImg=OpenCVQImage(mat)
        #qImgs=qImg.scaled(int(rx),int(ry))
        #qImg=QImage('../images/CAM00293.jpg')
        #cvi=cv2.imread('../images/CAM00293.jpg')  
        self.qPainter.drawImage(r,qImg)
    def setColor(self,r,g,b,a=255):
        #self.qPainter.pen().setColor(QtWidgets.QColor(r, g, b, a))
        self.qPainter.setPen(QtWidgets.QPen(QtWidgets.QColor(r, g, b, a)))
    def setWidth(self,w):
        self.qPainter.pen().setWidthF(w)
    def setSolidLine(self):
        self.qPainter.pen().setStyle(QtCore.Qt.SolidLine)
    def setDotLine(self):
        self.qPainter.pen().setStyle(QtCore.Qt.DotLine)
