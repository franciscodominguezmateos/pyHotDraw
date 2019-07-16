'''
Created on 25/03/2013

@author: Francisco Dominguez
'''
from pyHAbstractFigure import pyHAbstractFigure
from pyHotDraw.Geom.pyHRectangle import pyHRectangle

class pyHCompositeFigure(pyHAbstractFigure):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pyHAbstractFigure.__init__(self)
        self.figures=[]
    def clearFigures(self):
        self.figures=[]
    def addFigure(self,f):
        self.figures.append(f)
    def removeFigure(self,f):
        self.figures.remove(f)
    def getLength(self):
        return len(self.figures)
    def getFigures(self):
        return self.figures
    def draw(self,g):
        for f in self.figures:
            f.draw(g)
    def move(self,x,y):
        for f in self.getFigures():
            f.move(x,y)
    def getDisplayBox(self):
        minX=10e100
        minY=10e100
        maxX=0
        maxY=0
        for f in self.getFigures():
            r=f.getDisplayBox()
            x0=r.getX()
            y0=r.getY()
            x1=x0+r.getWidth()
            y1=y0+r.getHeight()
            if x0<minX:
                minX=x0
            if y0<minY:
                minY=y0
            if x1>maxX:
                maxX=x1
            if y1>maxY:
                maxY=y1
        return pyHRectangle(minX,minY,maxX-minX,maxY-minY)
    #visitor methods
    def visit(self,visitor):
        return visitor.visitCompositeFigure(self)

