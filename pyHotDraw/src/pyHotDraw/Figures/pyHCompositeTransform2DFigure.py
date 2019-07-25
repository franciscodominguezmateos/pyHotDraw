'''
Created on 16 Jul 2019

@author: Francisco Dominguez
+ Added transformation2D
- TODO: getDisplayBox and move doesn't seem to work with 2Dtransformations
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
    # TODO
    def move(self,dx,dy):
        #pyHCompositeFigure.move(self,dx,dy)
        self.t=self.t+pyHTransform2D(1,1,dx,dy)
    # TODO   only one transformation not recursion as in draw 
    def getDisplayBox(self):
        r=pyHCompositeFigure.getDisplayBox(self)
        rx,ry=self.t.transform(r.getX(),r.getX())
        rw,rh=self.t.scale(r.getWidth(),r.getHeight())
        return pyHRectangle(rx,ry,rw,rh)
