#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 25/03/2013

@author: Francisco Dominguez
'''
from pyHotDraw.Geom.pyHRectangle import pyHRectangle
from pyHotDraw.Handles.pyHPolylineHandle import pyHPolylineHandle
from pyHAbstractFigure import pyHAbstractFigure

class pyHConnectionFigure(pyHAbstractFigure):
    def __init__(self):
        pyHAbstractFigure.__init__(self)
        self.points=[]
    def addPoint(self,p):
        self.points.append(p)
    def getLastPoint(self):
        return self.points[-1]
    def getPoints(self):
        return self.points
    def getLenght(self):
        return len(self.points)
    def getDisplayBox(self):
        maxX=0
        maxY=0
        minX=1e90
        minY=1e90
        for p in self.points:
            if p.getX()<minX:
                minX=p.getX()
            if p.getX()>maxX:
                maxX=p.getX()
            if p.getY()<minY:
                minY=p.getY()
            if p.getY()>maxY:
                maxY=p.getY()
        return pyHRectangle(minX,minY,maxX-minX,maxY-minY)
    def containPoint(self,q):
        for p in self.points:
            if p==q:
                return True
        return False
    def move(self,x,y):
        for p in self.points:
            p.setX(p.getX()+x)
            p.setY(p.getY()+y)
    def draw(self,g):
        pyHAbstractFigure.draw(self,g)
        if self.points:
            p0=self.points[0]
            for p1 in self.points[1:]:
                g.drawLine(p0.getX(),p0.getY(),p1.getX(),p1.getY())
                p0=p1
#Handle Method
    def getHandles(self):
        handles=[]
        for p in self.points:
            handles.append(pyHPolylineHandle(self,p))
        return handles
#Connector handle
    def setConnectorStart(self,connector):
        self.connectorStart=connector
    def setConnectorEnd(self,connector):
        self.connectorEnd=connector
    def getConnectorEnd(self):
        return self.connectorEnd
    def getConnectorStart(self):
        return self.connectorStart
#Observer pattern method, self is a Observer of connector owners
    def figureChanged(self,figure):
        ps=self.getConnectorStart().findStart(self)
        pe=self.getConnectorEnd().findEnd(self)
        self.points[0].setX(ps.getX())
        self.points[0].setY(ps.getY())
        self.points[-1].setX(pe.getX())
        self.points[-1].setY(pe.getY())
    #visitor method
    def visit(self,visitor):
        return visitor.visitConnectionFigure(self)
   
        