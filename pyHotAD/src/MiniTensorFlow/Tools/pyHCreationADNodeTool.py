

import copy
from pyHotDraw.Figures.pyHDecoratorUndoRedo import pyHDecoratorUndoRedo

class pyHCreationADNodeTool(object):
    '''
    classdocs
    '''


    def __init__(self,v,figureToCreate):
        """
        Constructor
        """
        self.view=v
        self.prototype=figureToCreate
        self.createdFigure = None
        self.getView().clearSelectedFigures()
        self.getView().update()

    def getView(self):
        return self.view

    def onMouseDown(self,e):
        if e.isLeftClick():

            self.createdFigure = copy.deepcopy(self.prototype)
            self.createdFigure.move(e.getX() - (self.createdFigure.getWidth() / 2),
                                    e.getY() - (self.createdFigure.getHeight() / 2))
            self.view.save_actual_state()
            self.view.getDrawing().addFigure(self.createdFigure)
            self.view.update()

    def onMouseUp(self,e):
        pass

    def onMouseMove(self,e):
        pass

    def onMouseGrab(self,e):
        print ("onMouseGrab in pyHCreationTool")
        self.createdFigure.setDisplayBox()

    def onMouseDobleClick(self,e):
        pass
    def onMouseWheel(self,e):
        pass
    def onKeyPressed(self,e):
        print (e.getKey())