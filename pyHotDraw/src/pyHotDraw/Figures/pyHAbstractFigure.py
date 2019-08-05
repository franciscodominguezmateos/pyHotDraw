'''
Created on 25/03/2013

@author: Francisco Dominguez
'''
import math
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Figures.pyHAttributes import pyHAttributeColor

class pyHAbstractFigure(object):
    def __init__(self):
        self.attributes={}
        self.changedFigureObservers=[]
        c=pyHAttributeColor(0,0,0)
        self.setColor(c)
        #this line gives maximun recursiondeep import error
        #self.toolBoxConnectors=pyHLocatorConnector.ToolBoxRectangleConnectors(self)
    def getAtribute(self,k):
        return self.attributes[k]
    def setAttribute(self,k,v):
        self.attributes[k]=v
    # example of overload on methodhs in python
    def setColor(self,c,g=None,b=None,a=255):
        if g==None and b==None:
            self.setAttribute("COLOR",c)
        else:
            r=c
            self.setAttribute("COLOR",pyHAttributeColor(r,g,b,a))
    def getDisplayBox(self):
        pass
    def setDisplayBox(self,r):
        pass
    def containPoint(self,p):
        return self.getDisplayBox().contains(p)
    def move(self,x,y):
        pass
    def draw(self,g):
        for v in self.attributes.values():
            v.draw(g)
            
#Abstract Handle methods
    def getHandles(self):
        handles=[]
        r=self.getDisplayBox()
        x=r.getX()
        y=r.getY()
        w=r.getWidth()
        h=r.getHeight()
        handles.append(pyHNullHandle(self,pyHPoint(x,y)))
        handles.append(pyHNullHandle(self,pyHPoint(x+w,y)))
        handles.append(pyHNullHandle(self,pyHPoint(x,y+h)))
        handles.append(pyHNullHandle(self,pyHPoint(x+w,y+h)))
        return handles
#Connector methods
    def getConnectors(self):
        return pyHLocatorConnector.ToolBoxDiamondConnectors(self)
    def findConnector(self,p):
        minD=1e90
        for c in self.getConnectors():
            r=c.getDisplayBox()
            pc=r.getCenterPoint() #central point of connector
            d=p.distance(pc)
            if d<minD:
                minD=d
                closestConnector=c
        return closestConnector
#Observer pattern methods
    def addChangedFigureObserver(self,fo):  
        self.changedFigureObservers.append(fo)
    def removeChangedFigureObserver(self,fo):
        self.changedFigureObservers.remove(fo)
    def notifyFigureChanged(self):
        for fo in self.changedFigureObservers:
            fo.figureChanged(self)        
          
from pyHotDraw.Locators.pyHRelativeLocator import pyHRelativeLocator
from pyHotDraw.Connectors.pyHLocatorConnector import pyHLocatorConnector
from pyHotDraw.Handles.pyHNullHandle import pyHNullHandle

















