#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: paco
'''
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
class pyHPolylineHandle(object):
    '''
    classdocs
    '''


    def __init__(self,owner,point):
        '''
        Constructor
        '''
        self.rf=pyHRectangleFigure(point.getX()-1,point.getY()-1,2,2)
        self.point=point
#Figure methods
    def containPoint(self,p):
        return self.rf.containPoint(p)
    def draw(self,g):
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
    