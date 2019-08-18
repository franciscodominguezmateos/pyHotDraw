'''
Created on 18 August 2019

@author: Francisco Dominguez
Draw a 2D scatter plot of x and y data
- move and getDisplayBox are not recursive but draw is
'''
from pyHotDraw.Geom.pyHTransform2D import pyHTransform2D
from pyHCompositeTransform2DFigure import pyHCompositeTransform2DFigure
from pyHotDraw.Figures.pyHTextFigure import pyHTextFigure
from pyHotDraw.Geom.pyHRectangle import pyHRectangle

class pyHScatterPlot(pyHCompositeTransform2DFigure):
    def __init__(self,xdata,ydata,labels=None,figures=None):
        pyHCompositeTransform2DFigure.__init__(self)
        self.maxX=1e-20
        self.maxY=1e-20
        self.minX=1e+20
        self.minY=1e+20
        for x,y in zip(xdata,ydata):
            self.updateMaxMin(x,y)
            f=pyHTextFigure(x-0.5,y-0.5,1,1," * ",border=False)
            self.addFigure(f)
        self.r=self.getRecFromMinMax()
    def updateMaxMin(self,x,y):
        if x>self.maxX: self.maxX=x
        if x<self.minX: self.minX=x
        if y>self.maxY: self.maxY=y
        if y<self.minY: self.minY=y
    def getRecFromMinMax(self):
        w=self.maxX-self.minX
        h=self.maxY-self.minY
        iw=w*0.1
        ih=h*0.1
        return pyHRectangle(self.minX-iw/2.0,self.minY-ih/2.0,w+iw,h+ih)
    def drawAxis(self,g):
        g.setColor(255,0,0,200)
        g.drawLine(self.minX*1.1,0,self.maxX*1.1,0)
        g.setColor(0,255,0,200)
        g.drawLine(0,self.minY*1.1,0,self.maxY*1.1)
    def draw(self,g):
        #pyHCompositeTransform2DFigure.draw(self,g)
        # save trasnformation
        oldt=g.getTransformation()
        # compose transformations
        newt=self.t+oldt
        g.setTransformation(newt)
        g.setFillColor(255,255,255,100)
        g.drawRect(self.r.getX(),self.r.getY(),self.r.getWidth(),self.r.getHeight()) 
        self.drawAxis(g)       
        for f in self.figures:
            f.draw(g)
        # restore transformation
        g.setTransformation(oldt)
    def move(self,dx,dy):
        self.t=self.t+pyHTransform2D(1,1,dx,dy) 
    def getDisplayBox(self):
        r=self.r
        rx,ry=self.t.transform(r.getX(),r.getY())
        rw,rh=self.t.scale(r.getWidth(),r.getHeight())
        return pyHRectangle(rx,ry,rw,rh)
