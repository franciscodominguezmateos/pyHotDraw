'''
Created on 01/08/2019

@author: Francisco Dominguez
- Drop figures on drawing
- If there is a figure on mouseDown then move the figure
'''

import copy
from pyHotDraw.Core.pyHExceptions import pyHFigureNotFound
from pyHotDraw.Geom.pyHPoint import pyHPoint

class pyHCreationDropTool(object):
    '''
    classdocs
    '''
    def __init__(self,v,figureToCreate):
        '''
        Constructor
        '''
        self.view=v
        self.prototype=figureToCreate
    def getView(self):
        return self.view
    def onMouseDown(self,e):
        p=pyHPoint(e.getX(),e.getY())
        try:
            f=self.view.findFigure(p)
            self.createdFigure=f
        except (pyHFigureNotFound):
            self.createdFigure=copy.deepcopy(self.prototype)
            r=self.createdFigure.getDisplayBox()
            self.createdFigure.move(e.getX()-r.getWidth()/2,e.getY()-r.getHeight()/2)
            self.view.getDrawing().addFigure(self.createdFigure)
            self.view.update()
    def onMouseUp(self,e):
        pass
    def onMouseMove(self,e):
        r=self.createdFigure.getDisplayBox()
        dx=e.getX()-r.getX()-r.getWidth()/2
        dy=e.getY()-r.getY()-r.getHeight()/2
        self.createdFigure.move(dx,dy)

    def onMouseGrab(self,e):
        print "onMouseGrab in pyHCreationTool"
        self.createdFigure.setDisplayBox()
    def onMouseDobleClick(self,e):
        pass
    def onMouseWheel(self,e):
        pass
    def onKeyPressed(self,e):
        pass