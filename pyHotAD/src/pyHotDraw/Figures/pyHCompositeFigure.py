'''
Created on 25/03/2013

@author: paco
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
        self.figures=[]
    def clearFigures(self):
        self.figures=[]
    def addFigure(self,f):
        self.figures.append(f)
    """editado para que compruebe si existe la figura"""
    def removeFigure(self,f):
        if f in self.figures:
            self.figures.remove(f)
    def getLenght(self):
        len(self.figures)
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


    def addChangedFigureObserver(self, fo):
        for f in self.getFigures():
            f.addChangedFigureObserver(fo)

    def notifyFigureChanged(self):
        for f in self.getFigures():
            f.notifyFigureChanged()

    #visitor methods
    def visit(self,visitor):
        return visitor.visitCompositeFigure(self)


