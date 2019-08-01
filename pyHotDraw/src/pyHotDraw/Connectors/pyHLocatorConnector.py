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
    def __init__(self,owner,locator):
        '''
        Constructor
        '''
        pyHAbstractConnector.__init__(self, owner)
        self.locator=locator
        #pyHAbstractConnector.setDisplayBox(self, self.getDisplayBox())
    def locate(self,connectionFigure):
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
            x=math.cos(alpha)/2+0.5
            y=math.sin(alpha)/2+0.5
            connectors.append(pyHLocatorConnector(f,pyHRelativeLocator(x,y)))
        return connectors 
    @classmethod
    def ToolBoxDiamondConnectors(cls,f):
        connectors=[]
        connectors.append(pyHLocatorConnector(f,pyHRelativeLocator.north()))
        connectors.append(pyHLocatorConnector(f,pyHRelativeLocator.south()))
        connectors.append(pyHLocatorConnector(f,pyHRelativeLocator.east()))
        connectors.append(pyHLocatorConnector(f,pyHRelativeLocator.west()))
        return connectors
    @classmethod
    def ToolBoxRectangleConnectors(cls,f):
        connectors=[]
        connectors.append(pyHLocatorConnector(f,pyHRelativeLocator.northEast()))
        connectors.append(pyHLocatorConnector(f,pyHRelativeLocator.northWest()))
        connectors.append(pyHLocatorConnector(f,pyHRelativeLocator.southWest()))
        connectors.append(pyHLocatorConnector(f,pyHRelativeLocator.southEast()))
        return connectors