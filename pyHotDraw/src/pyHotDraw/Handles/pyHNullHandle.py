#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: paco
'''
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
class pyHNullHandle(object):
    '''
    classdocs
    '''


    def __init__(self,owner,point):
        '''
        Constructor
        '''
        self.rf=pyHRectangleFigure(point.getX()-1,point.getY()-1,2,2)
        self.point=point
        self.owner=owner
#Figure methods
    def containPoint(self,p):
        return self.rf.containPoint(p)
    def draw(self,g):
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
    