#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 25/03/2013

@author: paco
'''
from pyHotDraw.Geom.pyHRectangle import pyHRectangle
from pyHotDraw.Handles.pyHPolylineHandle import pyHPolylineHandle
from pyHAbstractFigure import pyHAbstractFigure

class pyHPolylineFigure(pyHAbstractFigure):
    def __init__(self):
        pyHAbstractFigure.__init__(self)
        self.points=[]
        # maxDist is distance from pq to segment
        self.maxDist=2       
    def clearPoints(self):
        self.points=[]
    def addPoint(self,p):
        self.points.append(p)
    def getFirstPoint(self):
        return self.points[0]
    def getLastPoint(self):
        return self.points[-1]
    def getPoints(self):
        return self.points
    def reversePoints(self):
        pts=self.getPoints()
        pts.reverse()
        self.clearPoints()
        for p in pts:
            self.addPoint(p)
        return self.getPoints()
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
        return pyHRectangle(minX-1,minY-1,maxX-minX+1,maxY-minY+1)
    def containPoint(self,q):
        for p in self.points:
            if p.distance(q)<self.maxDist:
                print p.distance(q)
                return True
        for i in range(len(self.points)-1):
            p0=self.points[i]
            p1=self.points[i+1]
            pq=q
            vs=p1-p0
            vLen=vs.mag()
            vn=vs.norm()
            if vn.mag()==0:
                continue
            vq=pq-p0
            d=abs(vn.cross(vq))#.mag()
            if abs(d)<=self.maxDist:
                #project vq on vn
                l=vn.dot(vq)
                if l>=0:
                    prj=vn*l
                    #projection length must be shorter than segment lenght vn
                    prjLen=prj.mag()
                    if prjLen>=0 and prjLen<=vLen:
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
    def getHandles(self):
        handles=[]
        for p in self.points:
            handles.append(pyHPolylineHandle(self,p))
        return handles
    #visitor method
    def visit(self,visitor):
        return visitor.visitPolylineFigure(self)
