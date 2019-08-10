#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 04/04/2013

@author: paco
'''
import math
from pyHotDraw.Geom.pyHRectangle import pyHRectangle
from pyHotDraw.Connectors.pyHAbstractConnector import pyHAbstractConnector
from pyHotDraw.Locators.pyHRelativeLocator import pyHRelativeLocator

class pyHLocatorConnector(pyHAbstractConnector):
    '''
    classdocs
    '''
    def __init__(self, owner, locator):
        '''
        Constructor
        '''
        pyHAbstractConnector.__init__(self, owner)
        self.locator=locator
        #pyHAbstractConnector.setDisplayBox(self, self.getDisplayBox())
    def locate(self, connectionFigure=None):
        return self.locator.locate(self.owner)
    def getDisplayBox(self):
        p=self.locate(self.owner)
        x=p.getX()-self.SIZE/2
        y=p.getY()-self.SIZE/2
        w=self.SIZE
        h=self.SIZE
        return pyHRectangle(x,y,w,h)
    def findStart(self,connectionFigure):
        return self.locate(connectionFigure)
    def findEnd(self,connectionFigure):
        return self.locate(connectionFigure)
    #TOOLBOXes
    #Build a set of n relative locator around a circle
    @classmethod
    def ToolBoxCircleConnectors(cls,f,n=32):
        connectors=[]
        for i in range(n):
            alpha=2*math.pi/n*i
            x=math.cos(alpha)
            y=math.sin(alpha)
            x_norm = (x+1) / 2
            y_norm = (y+1) / 2
            connectors.append(pyHLocatorConnector(f,pyHRelativeLocator(x_norm,y_norm)))
        return connectors 
    @classmethod
    def ToolBoxDiamondConnectors(cls,f):
        return [pyHLocatorConnector(f, pyHRelativeLocator.north()),
                pyHLocatorConnector(f, pyHRelativeLocator.south()),
                pyHLocatorConnector(f, pyHRelativeLocator.east()),
                pyHLocatorConnector(f, pyHRelativeLocator.west())]

    @classmethod
    def ToolBoxRectangleConnectors(cls,f):
        return [pyHLocatorConnector(f, pyHRelativeLocator.northEast()),
                pyHLocatorConnector(f, pyHRelativeLocator.northWest()),
                pyHLocatorConnector(f, pyHRelativeLocator.southWest()),
                pyHLocatorConnector(f, pyHRelativeLocator.southEast())]


    @classmethod
    def ToolBoxCenterLineFigureConnector(cls, f):
        return [pyHLocatorConnector(f, pyHRelativeLocator.west()),
                pyHLocatorConnector(f, pyHRelativeLocator.center()),
                pyHLocatorConnector(f, pyHRelativeLocator.east())]