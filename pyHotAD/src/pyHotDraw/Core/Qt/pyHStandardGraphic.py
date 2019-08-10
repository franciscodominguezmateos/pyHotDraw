#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 25/03/2013

@author: paco
'''
import cv2
from PyQt5 import QtGui,QtCore
from PyQt5.QtCore import QRectF

class pyHStandardGraphic:
    def __init__(self,qp,v):
        self.qPainter=qp
        #qp.setPen(QtGui.QPen(QtCore.qt.green, 3, QtCore.qt.DashDotLine, QtCore.qt.RoundCap, QtCore.qt.RoundJoin))
        self.t=v.getTransform()
        self.v=v
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
        #angles are counterclockwise in qt and unit is 1/16º
        self.qPainter.drawArc(x0,h-y0,rx,-ry,ans*16,anl*16)
    def drawPoint(self,x0, y0):
        h=self.v.height()
        x0,y0=self.t.transform(x0,y0)
        self.qPainter.drawPoint(x0,h-y0)
    def drawText(self,x,y,rx,ry,text):
        h=self.v.height()
        x0,y0=self.t.transform(x,y)
        self.qPainter.drawText(x0,h-y0,text)
    def drawImage(self,x,y,rx,ry,hImg):
        h=self.v.height()
        x0,y0=self.t.transform(x,y)
        rx=self.t.sx*rx
        ry=self.t.sy*ry

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
        #self.qPainter.pen().setColor(QtGui.QColor(r, g, b, a))
        self.qPainter.setPen(QtGui.QPen(QtGui.QColor(r, g, b, a)))

    """ Editado, no funcionaba """
    def setWidth(self,w):
        pen = self.qPainter.pen()
        pen.setWidthF(w)
        self.qPainter.setPen(pen)
    def setSolidLine(self):
        self.qPainter.pen().setStyle(QtCore.Qt.SolidLine)
    def setDotLine(self):
        self.qPainter.pen().setStyle(QtCore.Qt.DotLine)



    def setFontSize(self, size):
        # nf = QtGui.QFont(self.qPainter.font().family(), size, bold)

        self.qPainter.setFont(QtGui.QFont('Arial', size))


    def setFillColor(self,r,g,b,a=255):
        self.qPainter.setBrush(QtGui.QBrush(QtGui.QColor(r, g, b, a), QtCore.Qt.SolidPattern))

