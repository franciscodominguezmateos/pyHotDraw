'''
Created on 25/03/2013

@author: paco
'''

from pyHotDraw.Figures.pyHPolylineFigure import pyHPolylineFigure
from pyHotDraw.Geom.pyHPoint import pyHPoint

class pyHLineCreationTool(object):
    '''
    classdocs
    '''
    def __init__(self,v):
        '''
        Constructor
        '''
        self.view=v
    def getView(self):
        return self.view
    def onMouseDown(self,e):
        self.f=pyHPolylineFigure()
        p=pyHPoint(e.getX(),e.getY())
        self.f.addPoint(p)
        p=pyHPoint(e.getX(),e.getY())
        self.f.addPoint(p)
        self.view.getDrawing().addFigure(self.f)
    def onMouseUp(self,e):
        if self.f.getFirstPoint()==self.f.getLastPoint():
            self.view.getDrawing().removeFigure(self.f)
    def onMouseMove(self,e):
        if(self.f.getLenght()>0):
            p=self.f.getLastPoint()
            p.setX(e.getX())
            p.setY(e.getY())

    def onMouseDobleClick(self,e):
        pass
    def onMouseWheel(self,e):
        pass
    def onKeyPressed(self,e):
        pass