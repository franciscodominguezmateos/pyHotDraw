#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 3 Aug 2019

@author: Francisco Dominguez
'''
from pyHotDraw.Figures.pyHTextFigure import pyHTextFigure
from pyHotDraw.Figures.pyHAttributes import pyHAttributeWidth

class pyHLandMarkPredictionFigure(pyHTextFigure):
    '''
    classdocs
    '''
    def __init__(self,x0,y0,w,h,text="pyHotDraw",border=True):
        super(pyHLandMarkPredictionFigure,self).__init__(x0,y0,w,h,text,border)
    def move(self,x,y):
        return