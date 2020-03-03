#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 3 Aug 2019

@author: Francisco Dominguez
'''
from pyHotDraw.Figures.pyHConnectionFigure import pyHConnectionFigure
from pyHotDraw.Handles.pyHPolylineHandle import pyHPolylineHandle

class pyHConnectionMeasureFigure(pyHConnectionFigure):
    '''
    classdocs
    '''
    def __init__(self,point):
        super(pyHConnectionMeasureFigure,self).__init__()
        self.p=point
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
        self.addPoint(self.p)
        self.addPoint(pe)
        self.getConnectorStart().getOwner().addChangedFigureObserver(self)
        self.getConnectorEnd().getOwner().addChangedFigureObserver(self)
    def draw(self,g):
        super(pyHConnectionFigure,self).draw(g)
        g.drawEllipse(self.p.getX()-1,self.p.getY()-1,2,2)


#    def move(self,x,y):
#        return
        