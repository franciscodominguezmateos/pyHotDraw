'''
Created on 25/03/2013

@author: paco
'''
from pyHotDraw.Figures.pyHCompositeFigure import pyHCompositeFigure

class pyHDrawing(pyHCompositeFigure):
    '''
    classdocs
    '''


    def __init__(self,v):
        '''
        Constructor
        '''
        pyHCompositeFigure.__init__(self)
        self.view=v
        self.changedDrawingObservers=[]
    def addFigure(self,f):
        f.addChangedFigureObserver(self)
        self.figures.append(f)
    #Figure Observer method
    def figureChanged(self,f):
        self.notifyDrawingChanged()
    #Observed pattern methods
    def addChangedDrawingObserver(self,fo):  
        self.changedDrawingObservers.append(fo)
    def notifyDrawingChanged(self):
        for fo in self.changedDrawingObservers:
            fo.drawingChanged(self)    