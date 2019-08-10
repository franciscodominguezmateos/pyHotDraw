from MiniTensorFlow.figures.pyHHandleInfoDecorator import pyHHandleInfoDecorator

from pyHotDraw.Core.Exceptions import pyHHandleNotFound,pyHFigureNotFound
from pyHotDraw.Geom.pyHPoint import pyHPoint
from MiniTensorFlow.Tools.AbstractTool import AbstractTool

class pyHSelectionADTool(AbstractTool):
    """ Herramienta que permite:
        -
        -
        -
        -
    """
    def __init__(self,v):
        AbstractTool.__init__(self, v)
        self.delegateTool = AbstractTool(self.view)
        self.view.clearSelectedFigures()

    def onMouseDown(self,e):
        p=pyHPoint(e.getX(),e.getY())
        try:
            h=self.view.findHandle(p)
            # h.owner.removeExpresionsInfo()
            self.delegateTool= h

        except pyHHandleNotFound:
            try:
                f=self.view.findFigure(p)
                f = pyHHandleInfoDecorator(f, self.view)

                if not self.view.isThisFigureInSelectedFigures(f):
                    for fs in self.getView().getSelectionFigure().getFigures():
                        fs.removeFigure()
                    self.getView().clearSelectedFigures()
                    self.getView().selectFigure(f)
                    self.getView().getEditor().moveFront()
                    # pyHBackwardInfoDecorator(f).getBackwardExpresions()

                else: # desseleccionar Figura
                    self.getView().clearSelectedFigures()
                    #f.removeExpresionsInfo()

                self.getView().update()
                self.delegateTool=AbstractTool(self.view)

            except pyHFigureNotFound:
                self.delegateTool = AbstractTool(self.view)
        self.delegateTool.onMouseDown(e)

    def onMouseUp(self,e):
        pass

        self.delegateTool.onMouseUp(e)
    def onMouseMove(self,e):
        self.delegateTool.onMouseMove(e)
    def onMouseDobleClick(self,e):
        self.delegateTool.onMouseMove(e)

    def onMouseWheel(self,e):
        self.delegateTool.onMouseWheel(e)
    def onKeyPressed(self,e):
        pass

