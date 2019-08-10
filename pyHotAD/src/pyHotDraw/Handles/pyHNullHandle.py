#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: paco
'''
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
from pyHotDraw.Figures.pyHAttributes import *

class pyHNullHandle(object):
    '''
    classdocs
    '''


    def __init__(self,owner,point):
        '''
        Constructor
        '''
        self.rf=pyHRectangleFigure(point.getX()-1,point.getY()-1,20,20)
        self.rf.setAttribute('COLOR', pyHAttributeColor(170, 170, 170, 255))
        self.rf.setAttribute('FILL', pyHAttributeFillColor(220, 220, 220, 255))
        self.point=point
        self.owner=owner
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
        pass
    