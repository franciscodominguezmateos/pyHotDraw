#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 3 Aug 2019

@author: Francisco Dominguez
'''
from pyHotDraw.Figures.pyHTextFigure import pyHTextFigure
from pyHotDraw.Figures.pyHEllipseFigure import pyHEllipseFigure

class pyHNodePosePredictionFigure(pyHTextFigure):
    '''
    classdocs
    '''
    def __init__(self,x0,y0,w,h,text="pyHotDraw",border=True):
        super(pyHNodePosePredictionFigure,self).__init__(x0,y0,w,h,text,border)
        self.e=pyHEllipseFigure(x0,y0,w,h)
        #self.e.setColor(0,100,0)
        #self.e.setFillColor(50, 255, 50, 100)
        #self.e.setWidth(3)
    def draw(self,g):
        super(pyHNodePosePredictionFigure,self).draw(g)
        self.e.draw(g)
    #def move(self,x,y):
    #    super(pyHMotionNodeFigure,self).move(x,y)
    #    self.e.move(x,y)
    def getConnectors(self):
        return self.e.getConnectors()
    def move(self,x,y):
        return