#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 30/03/2013

@author: paco
'''
from pyHotDraw.Geom.pyHPoint import pyHPoint
class pyHRelativeLocator(object):
    '''
    classdocs
    '''
    def __init__(self,rx,ry):
        '''
        Constructor
        '''
        self.rx=rx
        self.ry=ry
    def locate(self,figure):
        r=figure.getDisplayBox()
        return pyHPoint(r.getX()+r.getWidth()*self.rx,r.getY()+r.getHeight()*self.ry)
    @classmethod
    def east(cls):
        return pyHRelativeLocator(1,0.5)
    @classmethod
    def west(cls):
        return pyHRelativeLocator(0,0.5)
    @classmethod
    def north(cls):
        return pyHRelativeLocator(0.5,0)
    @classmethod
    def northEast(cls):
        return pyHRelativeLocator(1,0)
    @classmethod
    def northWest(cls):
        return pyHRelativeLocator(0,0)
    @classmethod
    def south(cls):
        return pyHRelativeLocator(0.5,1)
    @classmethod
    def southEast(cls):
        return pyHRelativeLocator(1,1)
    @classmethod
    def southWest(cls):
        return pyHRelativeLocator(0,1)
    @classmethod
    def center(cls):
        return pyHRelativeLocator(0.5,0.5)
    