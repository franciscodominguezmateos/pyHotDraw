#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: paco
'''
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
from pyHotDraw.Figures.pyHEllipseFigure import pyHEllipseFigure
class pyHSplineHandle(object):
    '''
    classdocs
    '''
    def __init__(self,owner,point,i):
        '''
        Constructor
        '''
        pos=i % 3
        if i==0 or i==3:
            #curve points
            self.rf=pyHRectangleFigure(point.getX()-1,point.getY()-1,2,2)
        else:
            #control points
            self.rf=pyHEllipseFigure(point.getX()-1,point.getY()-1,2,2)
        self.owner=owner
        self.point=point
        self.i=i #index of point
#Figure methods
    def containPoint(self,p):
        return self.rf.containPoint(p)
    def draw(self,g):
        i=self.i
        pos=i % 3
        self.rf.draw(g)
        if pos==1:
            ps=self.owner.getPoints()[i-1]
            pd=self.point
            g.drawLine(ps.getX(),ps.getY(),pd.getX(),pd.getY())
        if pos==2 and i+1<len(self.owner.getPoints()):
            ps=self.owner.getPoints()[i+1]
            pd=self.point
            g.drawLine(ps.getX(),ps.getY(),pd.getX(),pd.getY())
#Tool methods
    def onMouseDown(self,e):
        pass
    def onMouseUp(self,e):
        pass
    def onMouseMove(self,e):
        print "mouseMove pyHSplineHandle"
        self.point.setX(e.getX())
        self.point.setY(e.getY())
    