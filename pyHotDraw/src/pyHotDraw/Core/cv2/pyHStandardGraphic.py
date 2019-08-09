#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 09/08/2019

@author: Francisco Dominguez
'''
import cv2

class pyHStandardGraphic:
    def __init__(self,v,img):
        self.img=img
        self.color=(0,0,0)
        self.pen_width=1
        self.v=v
    def getTransformation(self):
        return self.v.getTransform()
    def setTransformation(self,t):
        self.v.setTransform()
    def drawLine(self,x0,y0,x1,y1):
        h=self.v.height()
        x0,y0=self.getTransformation().transform(x0,y0)
        x1,y1=self.getTransformation().transform(x1,y1)
        x0=int(x0)
        y0=int(y0)
        x1=int(x1)
        y1=int(y1)
        cv2.line(self.img,(x0,h-y0),(x1,h-y1),self.color,self.pen_width)
    def drawRect(self,x0,y0,rx,ry):
        h=self.v.height()
        x0,y0=self.getTransformation().transform(x0,y0)
        rx,ry=self.getTransformation().scale(rx,ry)
        ix0=int(x0)
        iy0=int(y0)
        irx=int(rx)
        iry=int(ry)
        cv2.rectangle(self.img,(ix0,h-iy0),(ix0+irx,h-iy0-iry),self.color,self.pen_width)
    def drawRoundedRect(self,x0,y0,rx,ry):
        self.drawRect(x0, y0, rx, ry)
    def drawEllipse(self,x0,y0,rx,ry):
        h=self.v.height()
        x0,y0=self.getTransformation().transform(x0,y0)
        rx,ry=self.getTransformation().scale(rx,ry)
        x0=x0+rx/2
        y0=y0+ry/2
        ix0=int(x0)
        iy0=int(y0)
        irx=int(rx/2)
        iry=int(ry/2)
        cv2.ellipse(self.img,(x0,h-y0),(irx,iry),0,0,360,self.color,self.pen_width)
    def drawArc(self,x0,y0,rx,ry,ans,ane):
        h=self.v.height()
        x0,y0=self.getTransformation().transform(x0,y0)
        rx,ry=self.getTransformation().scale(rx,ry)
        x0=x0+rx/2
        y0=y0+ry/2
        ix0=int(x0)
        iy0=int(y0)
        irx=int(rx/2)
        iry=int(ry/2)
        cv2.ellipse(self.img,(x0,h-y0),(irx,iry),0,ans,ane,self.color,self.pen_width)
    def drawPoint(self,x0, y0):
        h=self.v.height()
        x0,y0=self.t.transform(x0,y0)
        x0=int(x0)
        y0=int(h-y0)
        self.img[y0,x0]=self.color
    def drawText(self,x,y,rx,ry,text):
        h=self.v.height()
        x0,y0=self.getTransformation().transform(x,y)
        rx,ry=self.getTransformation().scale(rx,ry)
        #TODO: scale font
        ix0=int(x0)
        iy0=int(y0)
        irx=int(rx)
        iry=int(ry)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.img,text,(ix0,h-iy0), font, 0.5,self.color,self.pen_width,cv2.LINE_AA)
        #self.qPainter.drawRect(x0,h-y0,m.width(text),-m.height())
    def drawImage(self,x,y,rx,ry,hImg):
        h=self.v.height()
        x0,y0=self.getTransformation().transform(x,y)
        rx,ry=self.getTransformation().scale(rx,ry)
        # check size of self.img it can't paint ourside of it
        ix0=int(x0)
        iy0=int(h-y0)
        irx=int(rx)
        iry=int(ry)
        img=cv2.resize(hImg.getData(),(irx,iry))
        #img.copyTo(self.img.rowRange(ix0,irx ).colRange(h-iy0, iry));
        self.img[iy0-iry:iy0,ix0:ix0+irx]=img
    # image format is in bgr!!!!!!!!!!!
    def setColor(self,r,g,b,a=255):
        self.color=(b,g,r)
    def setWidth(self,w):
        self.pen_width=w
    def setSolidLine(self):
        pass
    def setDotLine(self):
        pass
