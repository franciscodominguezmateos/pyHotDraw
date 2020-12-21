#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: paco
'''
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Core.pyHExceptions import pyHFigureNotFound
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
from pyHotDraw.Figures.pyHEllipseFigure import pyHEllipseFigure
from pyHotDraw.Handles.pyHAbstractHandle import pyHAbstractHandle
from pyHotDraw.Figures.pyHConnectionFigure import pyHConnectionFigure
from pyHotDraw.Figures.pyHPolylineFigure import pyHPolylineFigure

from Figures.pyHNodeLandMarkMeasureFigure import pyHNodeLandMarkMeasureFigure
from Figures.pyHNodeLandMarkFigure import pyHNodeLandMarkFigure
from Figures.pyHNodePoseFigure import pyHNodePoseFigure

class pyHCreateLandMarkMeasureHandle(pyHAbstractHandle):
    '''
    classdocs
    '''


    def __init__(self,owner,point):
        '''
        Constructor
        '''
        pyHAbstractHandle.__init__(self)
        self.point=point
        self.owner=owner
        w=self.width
        h=self.height
        self.rf=pyHRectangleFigure(self.point.getX()-w/2,self.point.getY()-h/2,w,h)
    def setView(self,v):
        pyHAbstractHandle.setView(self, v)
        h,w=self.getHandleSize()
        self.rf=pyHRectangleFigure(self.point.getX()-w/2,self.point.getY()-h/2,w,h)
#Figure methods
    def containPoint(self,p):
        return self.rf.containPoint(p)
    def draw(self,g):
        h,w=self.getHandleSize()
        self.rf=pyHRectangleFigure(self.point.getX()-w/2,self.point.getY()-h/2,w,h)
        self.rf.draw(g)
#Tool methods
    def onMouseDown(self,e):
        self.anchorPoint=pyHPoint(e.getX(),e.getY())
        self.f=pyHPolylineFigure()
        p=pyHPoint(e.getX(),e.getY())
        self.f.addPoint(p)
        p=pyHPoint(e.getX(),e.getY())
        self.f.addPoint(p)
        self.view.getDrawing().addFigure(self.f)
    def onMouseUp(self,e):
        ex=e.getX()
        ey=e.getY()
        d=self.view.getDrawing()
        d.removeFigure(self.f)
        try:                
            nf=self.view.findFigure(pyHPoint(ex,ey))
            if isinstance(nf,pyHNodeLandMarkFigure):
                cnf=nf.getDisplayBox().getCenterPoint()
                cow=self.owner.getDisplayBox().getCenterPoint()
                pf=cnf*0.5+cow*0.5
                lmmf=pyHNodeLandMarkMeasureFigure(pf.getX()-1,pf.getY()-1,2,2,"?")
                d.addFigure(lmmf)
                cf=pyHConnectionFigure()
                cf.setColor(0,0,255,100)
                cf.connectFigures(self.owner,lmmf)
                d.addFigure(cf)
                cf=pyHConnectionFigure()
                cf.setColor(100,0,0,100)
                cf.connectFigures(lmmf, nf )
                d.addFigure(cf)
                lmmf.setText(nf.getText())
                d.addFigure(cf)
            if isinstance(nf,pyHNodePoseFigure):
                cnf=nf.getDisplayBox().getCenterPoint()
                cow=self.owner.getDisplayBox().getCenterPoint()
                pf=cnf*0.5+cow*0.5
                npf=pyHNodePoseFigure(pf.getX()-1,pf.getY()-1,2,2,"?")
                d.addFigure(npf)
                cf=pyHConnectionFigure()
                cf.setColor(0,0,255,100)
                cf.connectFigures(self.owner,npf)
                d.addFigure(cf)
                cf=pyHConnectionFigure()
                cf.setColor(100,0,0,100)
                cf.connectFigures(npf, nf )
                d.addFigure(cf)
                npf.setText(nf.getText())
                d.addFigure(cf)
        except pyHFigureNotFound:
            print "No figure found"
    def onMouseMove(self,e):
        ex=e.getX()
        ey=e.getY()
        d=self.view.getDrawing()
        d.removeFigure(self.f)
        try:
            nf=self.view.findFigure(pyHPoint(ex,ey))
            if isinstance(nf,pyHNodeLandMarkFigure):
                self.f.setColor(0,0,255)
            else: 
                if isinstance(nf,pyHNodePoseFigure):
                    self.f.setColor(0,255,0)
        except pyHFigureNotFound:
            self.f.setColor(0,0,0)
        if(self.f.getLenght()>0):
            p=self.f.getLastPoint()
            p.setX(e.getX())
            p.setY(e.getY())
        d.addFigure(self.f)
