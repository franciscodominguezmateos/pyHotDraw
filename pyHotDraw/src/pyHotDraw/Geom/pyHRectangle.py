#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: paco
'''
from PyQt4.QtCore import QRectF
from pyHotDraw.Geom.pyHPoint import pyHPoint

class pyHRectangle(QRectF):
    def getX(self):
        return self.x()
    def getY(self):
        return self.y()
    def getWidth(self):
        return self.width()
    def getHeight(self):
        return self.height()
    def getCenterPoint(self):
        r=self
        return pyHPoint(r.getX()+r.getWidth()/2,r.getY()+r.getHeight()/2)
    def setX(self,x):
        QRectF.setX(self,x)
    def setY(self,y):
        QRectF.setY(self,y)
    def setWidth(self,w):
        QRectF.setWidth(self,w)
    def setHeight(self,h):
        QRectF.setHeight(self,h)
    def move(self,dx,dy):
        x0=self.getX()
        y0=self.getY()
        x0+=dx
        y0+=dy
        self.setX(x0)
        self.setY(y0)

