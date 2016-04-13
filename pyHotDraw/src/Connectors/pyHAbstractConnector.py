#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 04/04/2013

@author: paco
'''
from pyHotDraw.Figures.pyHDecoratorFigure import pyHDecoratorFigure
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
class pyHAbstractConnector(pyHDecoratorFigure):
    '''
    classdocs
    '''
    def __init__(self,owner):
        '''
        Constructor
        '''
        self.SIZE=5
        f=pyHRectangleFigure(0,0,self.SIZE,self.SIZE)
        pyHDecoratorFigure.__init__(self,f)
        self.owner=owner
    def getOwner(self):
        return self.owner
    def findStart(self,connectionFigure):
        pass
    def findEnd(self,connectionFigure):
        pass
