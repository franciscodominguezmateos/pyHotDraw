#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: paco
'''
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
from pyHotDraw.Handles.pyHAbstractHandle import pyHAbstractHandle

class pyHPolylineHandle(pyHAbstractHandle):
    '''
    classdocs
    '''


    def __init__(self,owner,point):
        '''
        Constructor
        '''
        pyHAbstractHandle.__init__(self)
        self.point=point
        w=self.width
        h=self.height
        self.rf=pyHRectangleFigure(self.point.getX()-w/2,self.point.getY()-h/2,w,h)
    def setView(self,v):
        pyHAbstractHandle.setView(self, v)
        h,w=self.getHandleSize()
        self.rf=pyHRectangleFigure(self.point.getX()-w/2,self.point.getY()-h/2,w,h)
#Figure methods
    def containPoint(self,p):
        b=self.rf.containPoint(p)
        return b
    def draw(self,g):
        h,w=self.getHandleSize()
        self.rf=pyHRectangleFigure(self.point.getX()-w/2,self.point.getY()-h/2,w,h)
        self.rf.draw(g)
#Tool methods
    def onMouseDown(self,e):
        pass
    def onMouseUp(self,e):
        pass
    def onMouseMove(self,e):
        print "mouseMove pyHPolylineHandle"
        self.point.setX(e.getX())
        self.point.setY(e.getY())
    