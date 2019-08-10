#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 22/03/2016

@author: javi
'''
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
from pyHotDraw.Figures.pyHAttributes import pyHAttributeColor, pyHAttributeFillColor


class pyHBackwardHandle(object):
    '''
    classdocs
    '''

    def __init__(self, owner, point):
        '''
        Constructor
        '''
        self.handle_figure = pyHRectangleFigure(point.getX() - 1, point.getY() - 1, 20, 20)
        self.handle_figure.setAttribute('FILL', pyHAttributeFillColor(255, 51, 51, 255))
        self.handle_figure.setAttribute('COLOR', pyHAttributeColor(153, 0, 0, 255))

        self.point = point
        self.owner = owner

    # Figure methods
    def containPoint(self, p):
        return self.handle_figure.containPoint(p)

    def draw(self, g):
        self.handle_figure.draw(g)

    # Tool methods
    def onMouseDown(self, e):
        self.owner.showBackwardInfo(self.point.getX(), self.point.getY() - 20)

    def onMouseUp(self, e):
        pass

    def onMouseMove(self, e):
        pass
