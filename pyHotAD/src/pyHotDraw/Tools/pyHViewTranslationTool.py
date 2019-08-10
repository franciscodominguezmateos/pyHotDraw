'''
Created on 25/03/2013

@author: paco
'''
from pyHotDraw.Core.Exceptions import pyHHandleNotFound,pyHFigureNotFound
from pyHotDraw.Geom.pyHPoint import pyHPoint

class pyHViewTranslationTool(object):
    '''
    classdocs
    '''
    def __init__(self,v):
        '''
        Constructor
        '''
        self.view=v
        self.p = None

    def getView(self):
        return self.view

    def onMouseDown(self,e):
        self.p=pyHPoint(e.getX(),e.getY())

    def onMouseUp(self,e):
        self.p = None

    def onMouseMove(self,e):
        if self.p:
            t=self.view.getTransform()
            t.tx+=e.getX()-self.p.getX()
            t.ty+=e.getY()-self.p.getY()





    def onMouseDobleClick(self,e):
        pass
    def onMouseWheel(self,e):
        pass
    def onKeyPressed(self,e):
        pass
