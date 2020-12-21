#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 21 Aug 2020

@author: Francisco Dominguez
'''
import pyHotDraw
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Figures.pyHTextFigure import pyHTextFigure
from pyHotDraw.Figures.pyHEllipseFigure import pyHEllipseFigure

class pyHNodePoseFigure(pyHTextFigure):
    '''
    classdocs
    '''
    def __init__(self,x0,y0,w,h,text="pyHotDraw",border=False):
        super(pyHNodePoseFigure,self).__init__(x0,y0,w,h,text,border)
        self.e=pyHEllipseFigure(x0,y0,w,h)
        self.e.setColor(0,100,0)
        self.e.setFillColor(50, 255, 50, 100)
        self.e.setWidth(3)
    def draw(self,g):
        super(pyHNodePoseFigure,self).draw(g)
        self.e.draw(g)
    def move(self,x,y):
        super(pyHNodePoseFigure,self).move(x,y)
        self.e.move(x,y)
    def getConnectors(self):
        return self.e.getConnectors()
    def getHandles(self):
        #handles=super(pyHNodePoseFigure,self).getHandles()
        handles=[]
        r=self.getDisplayBox()
        x=r.getX()
        y=r.getY()
        w=r.getWidth()
        h=r.getHeight()
        handles.append(pyHCreateLandMarkMeasureHandle(self,pyHPoint(x,y+h/2)))
        return handles

from Handles.pyHCreateLandMarkMeasureHandle import pyHCreateLandMarkMeasureHandle
