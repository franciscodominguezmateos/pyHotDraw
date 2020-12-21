#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 31/03/2013

@author: paco
'''
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure
from pyHotDraw.Figures.pyHEllipseFigure import pyHEllipseFigure
from pyHotDraw.Handles.pyHAbstractHandle import pyHAbstractHandle
from pyHotDraw.Figures.pyHConnectionFigure import pyHConnectionFigure

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
        self.lmmf=pyHNodeLandMarkMeasureFigure(self.anchorPoint.getX()-1,self.anchorPoint.getY()-1,2,2,"?")
        self.view.getDrawing().addFigure(self.lmmf)
    def onMouseUp(self,e):
        ex=e.getX()
        ey=e.getY()
        d=self.view.getDrawing()
        d.removeFigure(self.lmmf)
        lmf=self.view.findFigure(pyHPoint(ex,ey))
        if(isinstance(lmf,pyHNodeLandMarkFigure)):
                d.addFigure(self.lmmf)
                cf=pyHConnectionFigure()
                cf.setColor(0,0,255,100)
                cf.connectFigures(self.owner,self.lmmf)
                d.addFigure(cf)
                cf.connectFigures(self.lmmf, lmf )
                cf.setColor(100,0,0,100)
                self.lmmf.setText(lmf.getText())
                d.addFigure(cf)
        if(isinstance(lmf,pyHNodePoseFigure)):
                d.addFigure(self.lmmf)
                cf=pyHConnectionFigure()
                cf.setColor(0,0,255,100)
                cf.connectFigures(self.owner,self.lmmf)
                d.addFigure(cf)
                cf.connectFigures(self.lmmf, lmf )
                cf.setColor(100,0,0,100)
                self.lmmf.setText(lmf.getText())
                d.addFigure(cf)
    def onMouseMove(self,e):
        print "mouseMove ppyHNullHandle"
        p=pyHPoint(e.getX(),e.getY())
        dx=e.getX()-self.anchorPoint.getX()
        dy=e.getY()-self.anchorPoint.getY()
        self.lmmf.move(dx,dy)
        self.anchorPoint=p
    