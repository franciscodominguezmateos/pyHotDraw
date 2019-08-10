#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: paco
'''
from PyQt5.QtCore import QRectF

class pyHRectangle(QRectF):
    def getX(self):
        return self.x()
    def getY(self):
        return self.y()
    def getWidth(self):
        return self.width()
    def getHeight(self):
        return self.height()
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

