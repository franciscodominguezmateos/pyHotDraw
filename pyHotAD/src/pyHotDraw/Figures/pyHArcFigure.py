#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 26/03/2013

@author: paco
'''
from pyHotDraw.Geom.pyHArc import pyHArc
from pyHotDraw.Geom.pyHRectangle import pyHRectangle
from pyHAbstractFigure import pyHAbstractFigure

class pyHArcFigure(pyHAbstractFigure):
    '''
    classdocs
    '''
    def __init__(self,x0,y0,w,h,ans,ane):
        '''
        Constructor
        '''
        pyHAbstractFigure.__init__(self)
        self.arc=pyHArc(x0,y0,w,h,ans,ane)
    def getDisplayBox(self):
        return self.arc.getRectangle()
    def setDisplayBox(self,r):
        self.arc.setRectangle(r)
        #send event to observers
        self.notifyFigureChanged()
    def move(self,dx,dy):
        self.arc.getRectangle().move(dx,dy)
        #send event to observers
        self.notifyFigureChanged()
    def draw(self,g):
        pyHAbstractFigure.draw(self,g)
        x0=self.arc.getX()
        y0=self.arc.getY()
        w=self.arc.getWidth()
        h=self.arc.getHeight()
        ans=self.arc.getStartAngle()
        ane=self.arc.getEndAngle()
        g.drawArc(x0,y0,w,h,ans,ane)
    #visitor method
    def visit(self,visitor):
        return visitor.visitArcFigure(self)
