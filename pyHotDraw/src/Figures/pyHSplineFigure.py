#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 25/03/2013

@author: paco
from: http://www.ibiblio.org/e-notes/Splines/bezier.html
'''
from visual import vector
from pyHotDraw.Geom.pyHRectangle import pyHRectangle
from pyHotDraw.Handles.pyHSplineHandle import pyHSplineHandle
from pyHAbstractFigure import pyHAbstractFigure

class pyHSplineFigure(pyHAbstractFigure):
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
        return pyHRectangle(minX-1,minY-1,maxX-minX+1,maxY-minY+1)
    def containPoint(self,q):
        for i in range(len(self.points)-1):
            p0=vector(self.points[i].getX(),self.points[i].getY())
            p1=vector(self.points[i+1].getX(),self.points[i+1].getY())
            pq=vector(q.getX(),q.getY())
            vs=p1-p0
            vLen=vs.mag
            vn=vs.norm()
            if vn.mag==0:
                continue
            vq=pq-p0
            d=vn.cross(vq).mag
            if abs(d)<=1:
                #project vq on vn
                l=vn.dot(vq)
                if l>=0:
                    prj=vn*l
                    #projection length must be shorter than segment lenght vn
                    prjLen=prj.mag
                    if prjLen>=0 and prjLen<=vLen:
                        return True
        return False
    def move(self,x,y):
        for p in self.points:
            p.setX(p.getX()+x)
            p.setY(p.getY()+y)
            
# This code is for cuadratic splines
#     def draw(self,g):
#         pyHAbstractFigure.draw(self,g)
#         if self.points:
#             l=len(self.points)
#             j=0
#             while j<l-2:
#                 p0=vector(self.points[j+0].getX(),self.points[j+0].getY())
#                 p1=vector(self.points[j+1].getX(),self.points[j+1].getY())
#                 p2=vector(self.points[j+2].getX(),self.points[j+2].getY())
#                 pi=p0
#                 for i in range(0,21):
#                     t=i/20.0
#                     p=p0*(1-t)**2+p1*2*(1-t)*t+p2*t**2
#                     g.drawLine(pi.x,pi.y,p.x,p.y)
#                     pi=p
#                 j+=2
#             p0=self.points[j]
#             for p1 in self.points[j+1:]:
#                 g.drawLine(p0.getX(),p0.getY(),p1.getX(),p1.getY())
#                 p0=p1

# This code is for cubic splines or Bezier curves
    def draw(self,g):
        pyHAbstractFigure.draw(self,g)
        if self.points:
            l=len(self.points)
            j=0
            while j<l-3:
                p0=vector(self.points[j+0].getX(),self.points[j+0].getY())
                p1=vector(self.points[j+1].getX(),self.points[j+1].getY())
                p2=vector(self.points[j+2].getX(),self.points[j+2].getY())
                p3=vector(self.points[j+3].getX(),self.points[j+3].getY())
                pi=p0
                for i in range(0,21):
                    t=i/20.0
                    p02=p0*(1-t)**2+p1*2*(1-t)*t+p2*t**2
                    p12=p1*(1-t)**2+p2*2*(1-t)*t+p3*t**2
                    p=(1-t)*p02+t*p12
                    g.drawLine(pi.x,pi.y,p.x,p.y)
                    pi=p
                j+=3
            p0=self.points[j]
            for p1 in self.points[j+1:]:
                g.drawLine(p0.getX(),p0.getY(),p1.getX(),p1.getY())
                p0=p1
        
    def getHandles(self):
        handles=[]
        for i,p in enumerate(self.points):
            handles.append(pyHSplineHandle(self,p,i))
        return handles
    #visitor method
    def visit(self,visitor):
        return visitor.visitSplineFigure(self)
