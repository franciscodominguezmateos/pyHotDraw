'''
Created on 16 Jul 2019

@author: Francisco Dominguez
'''
from pyHAbstractFigure import pyHAbstractFigure
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHRectangleFigure import pyHRectangleFigure
from pyHCompositeFigure import pyHCompositeFigure

class pyHGridFigure(pyHCompositeFigure):
    def __init__(self,x=0,y=0,rows=10,cols=20,cellWidth=40,cellHeight=None):
        pyHCompositeFigure.__init__(self)
        self.rows=rows
        self.cols=cols
        self.cellWidth =cellWidth
        if cellHeight==None:
            cellHeight=cellWidth
        self.cellHeight=cellHeight
        self.width =cols*cellWidth
        self.height=rows*cellHeight
        self.rf=pyHRectangleFigure(x,y,self.width,self.height)
        #draw cells updown or buttonup
        self.updown=True
        
    # this method change f location in order to be inserted in the grid
    def addFigure(self,f):
        l=self.getLength()
        nextCol=l % self.cols
        nextRow=l // self.cols
        if self.updown:
            gridPos=pyHPoint(nextCol*self.cellWidth,self.height-self.cellHeight-nextRow*self.cellHeight)
        else:
            gridPos=pyHPoint(nextCol*self.cellWidth,nextRow*self.cellHeight)
        sr=self.rf.getDisplayBox()
        drawPos=sr.getOriginPoint()+gridPos
        fr=f.getDisplayBox()
        offsetPos=drawPos-fr.getOriginPoint()
        f.move(offsetPos.getX(),offsetPos.getY())
        pyHCompositeFigure.addFigure(self,f)
    # return figure in pos i row and j colum
    def getFigure(self,i,j):
        if i>=self.rows or j>=self.cols or i<0 or j<0:
            return None
        return self.getFigure(i*self.cols+j)
    def draw(self,g):
        self.rf.draw(g)
        pyHCompositeFigure.draw(self,g)
    def move(self,dx,dy):
        self.rf.move(dx,dy)
        pyHCompositeFigure.move(self,dx,dy)     
    def getDisplayBox(self):
        return self.rf.getDisplayBox()
