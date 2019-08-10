'''
Created on 25/03/2013

@author: paco
'''
from pyHotDraw.Geom.pyHPoint import pyHPoint

class pyHFigureMoveTool(object):
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
        self.anchorPoint=pyHPoint(e.getX(),e.getY())
    def onMouseUp(self,e):
        pass
    def onMouseMove(self,e):
        print ("mouseMove ppyHFigureMovetool")
        p=pyHPoint(e.getX(),e.getY())
        dx=e.getX()-self.anchorPoint.getX()
        dy=e.getY()-self.anchorPoint.getY()
        for f in self.getView().getSelectedFigures():
            f.move(dx,dy)
        self.anchorPoint=p
    def onMouseDrag(self,e):
        print ("mouse drag event in pyHAreaSelectionTool")
    def onMouseDobleClick(self,e):
        pass
    def onMouseWheel(self,e):
        pass
    def onKeyPressed(self,e):
        pass