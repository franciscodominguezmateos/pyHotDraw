#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 3 Aug 2019

@author: Francisco Dominguez
'''
from pyHotDraw.Figures.pyHTextFigure import pyHTextFigure

class pyHNodeLandMarkMeasureFigure(pyHTextFigure):
    '''
    classdocs
    '''
    def __init__(self,x0,y0,w,h,text="pyHotDraw",border=True):
        super(pyHNodeLandMarkMeasureFigure,self).__init__(x0,y0,w,h,text,border)
        self.setColor(100,100,0)
        self.setFillColor(255, 255, 230,100)
#    def move(self,x,y):
#        return
        