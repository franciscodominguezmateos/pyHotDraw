'''
Created on 25/03/2013

@author: paco
'''

import copy

class pyHCreationTool(object):
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
        self.createdFigure=copy.deepcopy(self.prototype)
        self.createdFigure.move(e.getX(),e.getY())
        self.view.getDrawing().addFigure(self.createdFigure)
        self.view.update()
    def onMouseUp(self,e):
        pass
    def onMouseMove(self,e):
        r=self.createdFigure.getDisplayBox()
        w=e.getX()-r.getX()
        h=e.getY()-r.getY()
        r.setWidth(w)
        r.setHeight(h)
        self.createdFigure.setDisplayBox(r)

    def onMouseGrab(self,e):
        print "onMouseGrab in pyHCreationTool"
        self.createdFigure.setDisplayBox()
    def onMouseDobleClick(self,e):
        pass
    def onMouseWheel(self,e):
        pass
    def onKeyPressed(self,e):
        pass