'''
Created on 25/03/2013

@author: paco
'''
from pyHotDraw.Core.pyHExceptions import pyHHandleNotFound,pyHFigureNotFound
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
    def getView(self):
        return self.view
    def onMouseDown(self,e):
        self.p=pyHPoint(e.getX(),e.getY())
    def onMouseUp(self,e):
        pass
    def onMouseMove(self,e):
        t=self.view.getTransform()
        dx=e.getX()-self.p.getX()
        dy=e.getY()-self.p.getY()
        # translation is in pixels
        dxp,dyp=t.scale(dx,dy)
        t.tx+=dxp
        t.ty+=dyp
    def onMouseDobleClick(self,e):
        v=self.getView()
        p=pyHPoint(e.getX(),e.getY())
        try:
            f=v.findFigure(p)
            r=f.getDisplayBox()
            v.setTransformFitToRectangle(r)
        except (pyHFigureNotFound):
            v.setTransformFitToDrawing()
    def onMouseWheel(self,e):
        pass
    def onKeyPressed(self,e):
        pass
