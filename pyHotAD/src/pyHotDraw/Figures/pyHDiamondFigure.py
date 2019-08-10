#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 21/04/2015

@author: paco
'''
from pyHotDraw.Geom.pyHRectangle import pyHRectangle
from pyHAbstractFigure import pyHAbstractFigure

class pyHDiamondFigure(pyHAbstractFigure):
    '''
    classdocs
    '''
    def __init__(self,x0,y0,w,h):
        '''
        Constructor
        '''
        pyHAbstractFigure.__init__(self)
        self.x0=x0
        self.y0=y0
        self.w=w
        self.h=h
    def getDisplayBox(self):
        return pyHRectangle(self.x0,self.y0,self.w,self.h)
    def setDisplayBox(self,r):
        self.x0=r.getX()
        self.y0=r.getY()
        self.w =r.getWidth()
        self.h =r.getHeight()
        #send event to observers
        self.notifyFigureChanged()
    def move(self,dx,dy):
        self.x0+=dx
        self.y0+=dy
        #send event to observers
        self.notifyFigureChanged()
    def draw(self,g):
        pyHAbstractFigure.draw(self,g)
        g.drawLine(self.x0+self.w/2,self.y0         ,self.x0+self.w  ,self.y0+self.h/2)
        g.drawLine(self.x0+self.w  ,self.y0+self.h/2,self.x0+self.w/2,self.y0+self.h)
        g.drawLine(self.x0+self.w/2,self.y0+self.h  ,self.x0       ,self.y0+self.h/2)
        g.drawLine(self.x0         ,self.y0+self.h/2,self.x0+self.w/2,self.y0)
    #visitor method
    def visit(self,visitor):
        return visitor.visitEllipseFigure(self)