'''
Created on 25 Jul 2019

@author: Francisco Dominguez
This is like a drawing but you can put in any place of the main drawing and scale it too
- move and getDisplayBox are not recursive but draw is
'''
from pyHAbstractFigure import pyHAbstractFigure
from pyHotDraw.Geom.pyHTransform2D import pyHTransform2D
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Geom.pyHRectangle import pyHRectangle
from pyHRectangleFigure import pyHRectangleFigure
from pyHCompositeFigure import pyHCompositeFigure

class pyHCompositeTransform2DFigure(pyHCompositeFigure):
    def __init__(self,t=pyHTransform2D()):
        pyHCompositeFigure.__init__(self)
        self.t=t
    def getTransform2D(self):
        return self.t
    def setTransform2D(self,t):
        self.t=t
    def draw(self,g):
        # save trasnformation
        oldt=g.getTransformation()
        # compose transformations
        newt=self.t+oldt
        g.setTransformation(newt)
        for f in self.figures:
            f.draw(g)
        # restore transformation
        g.setTransformation(oldt)
    def move(self,dx,dy):
        self.t=self.t+pyHTransform2D(1,1,dx,dy) 
    def getDisplayBox(self):
        r=pyHCompositeFigure.getDisplayBox(self)
        rx,ry=self.t.transform(r.getX(),r.getY())
        rw,rh=self.t.scale(r.getWidth(),r.getHeight())
        return pyHRectangle(rx,ry,rw,rh)
