#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 25/11/2013

@author: paco
'''
import math
from pyHRectangle import pyHRectangle
from pyHPoint import pyHPoint
class pyHArc:
    def __init__(self,x0,y0,w,h,ans,ane):
        self.r=pyHRectangle(x0,y0,w,h)
        self.ans=ans #start angle
        self.ane=ane #end angle
    def getRectangle(self):
        return self.r
    def getStartAngle(self):
        return self.ans
    def getPointFrontAngle(self,a):
        w=self.getWidth()
        h=self.getHeight()
        xc=self.getX()+w/2
        yc=self.getY()+h/2
        rx=w/2
        ry=h/2
        xe=rx*math.cos(a)
        ye=ry*math.sin(a)
        return pyHPoint(xc+xe,yc+ye)
    def getStartAnglePoint(self):
        return self.getPointFrontAngle(self.ans)
    def getEndAngle(self):
        return self.ane
    def getEndAnglePoint(self):
        return self.getPointFrontAngle(self.ane)
    def getX(self):
        # type: () -> object
        return self.r.getX()
    def getY(self):
        return self.r.getY()
    def getWidth(self):
        return self.r.getWidth()
    def getHeight(self):
        return self.r.getHeight()
    def setX(self,x):
        self.r.setX(x)
    def setY(self,y):
        self.r.setY(y)
    def setWidth(self,w):
        self.r.setWidth(w)
    def setHeight(self,h):
        self.r.setHeight(h)
    def setRectangle(self,r):
        self.r=r
    def setStartAngle(self,ans):
        self.ans=ans
    def setEndAngle(self,ane):
        self.ane=ane
