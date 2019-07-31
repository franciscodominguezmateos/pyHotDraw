#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 25/03/2013

@author: Francisco Dominguez
'''
from pyHotDraw.Core.pyHDrawing import pyHDrawing
from pyHotDraw.Core.Exceptions import pyHHandleNotFound,pyHFigureNotFound
from pyHotDraw.Geom.pyHTransform2D import pyHTransform2D
from pyHotDraw.Figures.pyHCompositeFigure import pyHCompositeFigure

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step
def dirange(start, stop, step):
    r = start
    while r > stop:
        yield r
        r += step

class pyHAbstractView(object):
    def __init__(self,e):   
        self.editor=e
        self.clearSelectedFigures()
        self.setDrawing(pyHDrawing(self))
        self.transform=pyHTransform2D(1.0,1.0)
    def getTransform(self):
        return self.transform
    def setTransform(self,t):
        self.transform=t
    def setTransformFitToDrawing(self):
        r=self.getDrawing().getDisplayBox()
        self.setTransformFitToRectangle(r)
    def setTransformFitToRectangle(self,r):
        v=self
        t=v.getTransform()
        w=r.getWidth()
        h=r.getHeight()
        cx=r.getX()+w/2
        cy=r.getY()+h/2
        print "cxcy",cx,cy
        t.sx=v.width()/w
        t.sy=v.height()/h
        #just keep aspect ratio
        if t.sx<t.sy:
            t.sy=t.sx
        else:
            t.sx=t.sy
        t.tx=v.width()/2-cx*t.sx
        t.ty=v.height()/2-cy*t.sy
    def getEditor(self):
        return self.editor
    def setEditor(self,e):
        self.editor=e
    def setDrawing(self,d):
        d.addChangedDrawingObserver(self)
        self.drawing=d
    def getDrawing(self):
        return self.drawing
    #Drawing Observer method
    def drawingChanged(self,d):
        self.update()
    #to be provided for children classes
    def width(self):
        pass
    #to be provided for children classes
    def height(self):
        pass
    def drawGrid(self,g):
        g.setDotLine()
        g.setColor(220,220,230)
        t=self.getTransform()
        xs,ys=t.itransform(0,0)
        #print "xsys",xs,ys
        xe,ye=t.itransform(self.width(),self.height())
        #xe,ye=t.itransform(200,200)
        xg=t.sx
        yg=t.sy
        if xg>3 and yg>3:
            for x in drange(0,xe,1):
                g.drawLine(x,ys,x,ye)
            for y in drange(0,ye,1):
                g.drawLine(xs,y,xe,y)
            for x in dirange(0,xs,-1):
                g.drawLine(x,ys,x,ye)
            for y in dirange(0,ys,-1):
                g.drawLine(xs,y,xe,y)
        xi=xg*10
        yi=xg*10
        g.setColor(200,200,210)
        if xi>5 and yi>5:
            for x in drange(0,xe,10):
                g.drawLine(x,ys,x,ye)
            for y in drange(0,ye,10):
                g.drawLine(xs,y,xe,y)
            for x in dirange(0,xs,-10):
                g.drawLine(x,ys,x,ye)
            for y in dirange(0,ys,-10):
                g.drawLine(xs,y,xe,y)
        xi=xg*100
        yi=xg*100
        g.setColor(180,180,190)
        if xi>3 and yi>3:
            for x in drange(0,xe,100):
                g.drawLine(x,ys,x,ye)
            for y in drange(0,ye,100):
                g.drawLine(xs,y,xe,y)
            for x in dirange(0,xs,-100):
                g.drawLine(x,ys,x,ye)
            for y in dirange(0,ys,-100):
                g.drawLine(xs,y,xe,y)
        xi=xg*1000
        yi=xg*1000
        if xi>3 and yi>3:
            g.setColor(125,200,125)
            for x in drange(0,xe,1000):
                g.drawLine(x,ys,x,ye)
            for x in dirange(0,xs,-1000):
                g.drawLine(x,ys,x,ye)
            g.setColor(125,125,200)
            for y in drange(0,ye,1000):
                g.drawLine(xs,y,xe,y)
            for y in dirange(0,ys,-1000):
                g.drawLine(xs,y,xe,y)
        g.setColor(0,0,128)
        g.drawLine(xs,0,xe,0)
        g.setColor(0,128,0)
        g.drawLine(0,ys,0,ye)
        g.setColor(0,0,0)
    def draw(self,g):
        self.drawGrid(g)
        self.drawing.draw(g) 
        for f in self.getSelectedFigures():
            for h in f.getHandles():
                h.setView(self)
                h.draw(g)   
#Selection methods
    def clearSelectedFigures(self):
        self.selectedFigures=pyHCompositeFigure()
    def getSelectedFigures(self):
        return self.selectedFigures.getFigures()
    def getSelectionFigure(self):
        return self.selectedFigures
    def selectFigure(self,figure):
        self.selectedFigures.addFigure(figure)
    def unSelectFigure(self,figure):
        self.selectedFigures.removeFigure(figure)
    def selectFiguresInRectangle(self,r):
        for f in self.getDrawing().getFigures():
            rdb=f.getDisplayBox()
            if r.contains(rdb):
                self.selectFigure(f)
        print "Seleccionadas ",len(self.getSelectedFigures())
    def isThisFigureInSelectedFigures(self,f):
        for fs in self.getSelectedFigures():
            if fs==f:
                return True
        return False
    def findHandle(self,p):
        for f in self.getSelectedFigures():
            hs=f.getHandles()
            for h in hs:
                if h.containPoint(p):
                    h.setView(self)
                    return h
        raise pyHHandleNotFound("Handle not found at point %d,%d" % (p.getX(),p.getY()))
    def findFigure(self,p):
        for f in reversed(self.getDrawing().getFigures()):
            if f.containPoint(p):
                return f
        raise pyHFigureNotFound("Figure not found at point %d,%d"% (p.getX(),p.getY()))
    def findFigureReversed(self,p):
        for f in self.getDrawing().getFigures():
            if f.containPoint(p):
                return f
        raise pyHFigureNotFound("Figure not found at point %d,%d Reversed"% (p.getX(),p.getY()))
        
#Platform specific mouse and key manipulation see any pyHStandardView.py


        