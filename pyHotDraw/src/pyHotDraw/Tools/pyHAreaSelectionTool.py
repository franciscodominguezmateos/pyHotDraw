'''
Created on 25/03/2013

@author: paco
'''
from pyHotDraw.Figures.pyHRectangleFigure import pyHRectangleFigure

class pyHAreaSelectionTool(object):
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
        self.getView().clearSelectedFigures()
        self.r=pyHRectangleFigure(e.getX(),e.getY(),0,0)
        self.getView().getDrawing().addFigure(self.r)
    def onMouseUp(self,e):
        r=self.r.getDisplayBox()
        self.getView().getDrawing().removeFigure(self.r)
        self.getView().selectFiguresInRectangle(r)
        #self.getView().update()
    def onMouseMove(self,e):
        r=self.r.getDisplayBox()
        w=e.getX()-r.getX()
        h=e.getY()-r.getY()
        r.setWidth(w)
        r.setHeight(h)
        self.r.setDisplayBox(r)
    def onMouseDrag(self,e):
        print "mouse drag event in pyHAreaSelectionTool"
    def onMouseDobleClick(self,e):
        pass
    def onMouseWheel(self,e):
        pass
    def onKeyPressed(self,e):
        pass