'''
Created on 25/03/2013

@author: paco
'''

from pyHotDraw.Figures.pyHSplineFigure import pyHSplineFigure
from pyHotDraw.Geom.pyHPoint import pyHPoint

class pyHSplineCreationTool(object):
    '''
    classdocs
    '''
    def __init__(self,v):
        '''
        Constructor
        '''
        self.view=v
        self.f=pyHSplineFigure()
    def getView(self):
        return self.view
    def onMouseDown(self,e):
        p=pyHPoint(e.getX(),e.getY())
        self.f.addPoint(p)
        if(self.f.getLenght()==1):
#             p=pyHPoint(e.getX(),e.getY())
#             self.f.addPoint(p)
            self.view.getDrawing().addFigure(self.f)
    def onMouseUp(self,e):
        pass
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