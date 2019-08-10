'''
Created on 25/03/2013

@author: paco
'''

import copy
from pyHotDraw.Core.Exceptions import pyHFigureNotFound
from pyHotDraw.Geom.pyHPoint import pyHPoint

class pyHConnectionImageFilterTool(object):
    '''
    classdocs
    '''
    def __init__(self,v,figureToCreate):
        '''
        Constructor
        '''
        self.view=v
        self.prototype=figureToCreate
    def getView(self):
        return self.view
    def onMouseDown(self,e):
        print ("mouseDown pyHConnectionImageFilterTool")
        self.figureClicked=False
        p=pyHPoint(e.getX(),e.getY())
        try:
            f=self.view.findFigure(p)
            cStart=f.findConnector(p)
            print (dir(f))
            self.figureClicked=True
            self.createdFigure=copy.deepcopy(self.prototype)
            self.createdFigure.setConnectorStart(cStart)
            self.view.getDrawing().addFigure(self.createdFigure)
            #two points in order to do feedback with the second one
            p0=cStart.findStart(self.createdFigure)
            p1=cStart.findStart(self.createdFigure)
            self.createdFigure.addPoint(p0)
            self.createdFigure.addPoint(p1)
        except (pyHFigureNotFound):
                print ("No figure clicked")
    def onMouseUp(self,e):
        print ("mouseUp pyHConnectionImageFilterTool")
        p=pyHPoint(e.getX(),e.getY())
        try:
            f=self.view.findFigureReversed(p)
            if f==self.createdFigure:
                raise pyHFigureNotFound("Figure is the connection Figure")
            cEnd=f.findConnector(p)    
            self.createdFigure.setConnectorEnd(cEnd)
            pl=cEnd.findEnd(self.createdFigure)
            lp=self.createdFigure.getLastPoint()
            lp.setX(pl.getX())
            lp.setY(pl.getY())
            self.createdFigure.getConnectorStart().getOwner().addChangedFigureObserver(self.createdFigure)
            self.createdFigure.getConnectorEnd().getOwner().addChangedFigureObserver(self.createdFigure)
            self.figureClicked=False
        except (pyHFigureNotFound):
                print ("No figure found on mouseUP position in pyHConnectionImageFilterTool")
                self.view.getDrawing().removeFigure(self.createdFigure)

    def onMouseMove(self,e):
        print ("mouseMove pyHConnectionTool")
        if(self.figureClicked and self.createdFigure.getLenght()>0):
            p=self.createdFigure.getLastPoint()
            p.setX(e.getX())
            p.setY(e.getY())

    def onMouseGrab(self,e):
        print ("onMouseGrab in pyHCreationTool")
        self.createdFigure.setDisplayBox()
    def onMouseDobleClick(self,e):
        pass
    def onMouseWheel(self,e):
        pass
    def onKeyPressed(self,e):
        pass