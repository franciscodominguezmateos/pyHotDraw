#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: paco
'''
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
from pyHotDraw.Figures.pyHEllipseFigure import pyHEllipseFigure
from pyHotDraw.Handles.pyHAbstractHandle import pyHAbstractHandle

class pyHCreateLandMarkMeasureHandle(pyHAbstractHandle):
    '''
    classdocs
    '''


    def __init__(self,owner,point):
        '''
        Constructor
        '''
        pyHAbstractHandle.__init__(self)
        self.point=point
        self.owner=owner
        w=self.width
        h=self.height
        self.rf=pyHRectangleFigure(self.point.getX()-w/2,self.point.getY()-h/2,w,h)
    def setView(self,v):
        pyHAbstractHandle.setView(self, v)
        h,w=self.getHandleSize()
        self.rf=pyHRectangleFigure(self.point.getX()-w/2,self.point.getY()-h/2,w,h)
#Figure methods
    def containPoint(self,p):
        return self.rf.containPoint(p)
    def draw(self,g):
        h,w=self.getHandleSize()
        self.rf=pyHEllipseFigure(self.point.getX()-w/2,self.point.getY()-h/2,w,h)
        self.rf.draw(g)
#Tool methods
    def onMouseDown(self,e):
        self.anchorPoint=pyHPoint(e.getX(),e.getY())
    def onMouseUp(self,e):
        pass
    def onMouseMove(self,e):
        print "mouseMove ppyHNullHandle"
        p=pyHPoint(e.getX(),e.getY())
        dx=e.getX()-self.anchorPoint.getX()
        dy=e.getY()-self.anchorPoint.getY()
        self.owner.move(dx,dy)
        self.anchorPoint=p
    