#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 25/03/2013

@author: Francisco Dominguez
'''
from pyHotDraw.Geom.pyHRectangle import pyHRectangle
from pyHotDraw.Handles.pyHPolylineHandle import pyHPolylineHandle
from pyHPolylineFigure import pyHPolylineFigure

class pyHConnectionFigure(pyHPolylineFigure):
    def __init__(self):
        pyHPolylineFigure.__init__(self)
        self.points=[]
#Connector handle
    def setConnectorStart(self,connector):
        self.connectorStart=connector
    def setConnectorEnd(self,connector):
        self.connectorEnd=connector
    def getConnectorEnd(self):
        return self.connectorEnd
    def getConnectorStart(self):
        return self.connectorStart
    def connectFigures(self,fs,fe):
        rs=fs.getDisplayBox()
        re=fe.getDisplayBox()
        spc=rs.getCenterPoint()
        epc=re.getCenterPoint()
        self.connectorStart=fs.findConnector(epc)
        self.connectorEnd=fe.findConnector(spc)
        ps=self.getConnectorStart().findStart(self)
        pe=self.getConnectorEnd().findEnd(self)
        self.addPoint(ps)
        self.addPoint(pe)
        self.getConnectorStart().getOwner().addChangedFigureObserver(self)
        self.getConnectorEnd().getOwner().addChangedFigureObserver(self)
    def containPoint(self,q):
        return False
    def move(self,x,y):
        return
        pyHPolylineFigure.move(self,x,y)
        fs=self.getConnectorStart().getOwner()
        fe=self.getConnectorEnd().getOwner()   
        fs.move(x,y)
        fe.move(x,y)
    def getHandles(self):
        return []

        
#Observer pattern method, self is a Observer of connector owners
    def figureChanged(self,figure):
        fs=self.getConnectorStart().getOwner()
        fe=self.getConnectorEnd().getOwner()
        rs=fs.getDisplayBox()
        re=fe.getDisplayBox()
        spc=rs.getCenterPoint()
        epc=re.getCenterPoint()
        self.connectorStart=fs.findConnector(epc)
        self.connectorEnd=fe.findConnector(spc)
        
        ps=self.getConnectorStart().findStart(self)
        pe=self.getConnectorEnd().findEnd(self)
        self.points[0].setX(ps.getX())
        self.points[0].setY(ps.getY())
        self.points[-1].setX(pe.getX())
        self.points[-1].setY(pe.getY())
    #visitor method
    def visit(self,visitor):
        return visitor.visitConnectionFigure(self)
   
        