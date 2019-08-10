#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 16/03/2016

@author: javi
'''
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
from pyHotDraw.Figures.pyHAttributes import pyHAttributeColor, pyHAttributeFillColor

class pyHForwardHandle(object):
    '''
    classdocs
    '''


    def __init__(self,owner,point):
        '''
        Constructor
        '''
        self.handle_figure = pyHRectangleFigure(point.getX() - 1, point.getY() - 1, 20, 20)
        self.handle_figure.setAttribute('COLOR', pyHAttributeColor(232, 61, 61, 255))
        self.handle_figure.setAttribute('FILL', pyHAttributeFillColor(141, 38, 38, 255))
        self.point=point
        self.owner=owner

    #Figure methods
    def containPoint(self,p):
        return self.handle_figure.containPoint(p)

    def draw(self,g):
        self.handle_figure.draw(g)



    #Tool methods
    def onMouseDown(self, e):
        #self.owner.showForwardExpresion(self.point.getX()+40,
        #                               self.point.getY()+40)
        self.owner.showForwardInfo(self.point.getX(), self.point.getY()+40)

    def onMouseUp(self,e):
        pass

    def onMouseMove(self,e):
        pass

    def onMouseDobleClick(self,e):
        pass

    def onMouseWheel(self,e):
        pass

    def onKeyPressed(self,e):
        pass