#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: Francisco Dominguez
'''
#from PyQt4.QtCore import QRectF
from pyHotDraw.Geom.pyHPoint import pyHPoint
from __builtin__ import False

class pyHRectangle(object): #QRectF):
    def __init__(self,x,y,w,h):
        self.setX(x)
        self.setY(y)
        self.setWidth(w)
        self.setHeight(h)
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWidth(self):
        return self.w
    def getHeight(self):
        return self.h
    def getOriginPoint(self):
        return pyHPoint(self.getX(),self.getY())
    def getCenterPoint(self):
        r=self
        return pyHPoint(r.getX()+r.getWidth()/2,r.getY()+r.getHeight()/2)
    def getEndPoint(self):
        r=self
        return pyHPoint(r.getX()+r.getWidth(),r.getY()+r.getHeight())
    def setX(self,x):
        self.x=float(x)
    def setY(self,y):
        self.y=float(y)
    def setWidth(self,w):
        self.w=float(w)
    def setHeight(self,h):
        self.h=float(h)
    def move(self,dx,dy):
        x0=self.getX()
        y0=self.getY()
        x0+=dx
        y0+=dy
        self.setX(x0)
        self.setY(y0)
    def contains(self,p):
        xe=self.getX()+self.getWidth()
        ye=self.getY()+self.getHeight()
        px=p.getX()
        py=p.getY()
        if px<self.getX() or px>xe: return False
        if py<self.getY() or py>ye: return False
        return True

