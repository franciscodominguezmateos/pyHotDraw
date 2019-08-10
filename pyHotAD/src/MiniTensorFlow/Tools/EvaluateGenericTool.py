
from pyHotDraw.Core.Exceptions import pyHHandleNotFound,pyHFigureNotFound
from pyHotDraw.Geom.pyHPoint import pyHPoint
from MiniTensorFlow.Tools.AbstractTool import AbstractTool
from pyHotDraw.Tools.pyHViewTranslationTool import pyHViewTranslationTool
from figures.DecoratedNodes.ShowInfoNodeDecorator import ShowInfoNodeDecorator
from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure

class EvaluateGenericTool(AbstractTool):

    def __init__(self,v):
        AbstractTool.__init__(self, v)
        self.p = None
        self.delegateTool = pyHViewTranslationTool(self.view)
        self._start()

    def _start(self):
        self.getView().clearSelectedFigures()
        drawing = self.getView().getDrawing()
        for f in drawing.getFigures()[:]:
            if isinstance(f, NodeFigure):
                drawing.removeFigure(f)
                drawing.addFigure(ShowInfoNodeDecorator(f))



    def onMouseDown(self,e):
        p=pyHPoint(e.getX(),e.getY())
        try:
            h = self.view.findHandle(p)
            print(h)
            self.delegateTool = h
        except pyHHandleNotFound:
            try:
                f = self.view.findFigure(p)
                if self.getView().isThisFigureInSelectedFigures(f):
                    self.getView().unSelectFigure(f)
                else:
                    self.getView().selectFigure(f)
                    self.getView().getEditor().moveFront()

                self.delegateTool = AbstractTool(self.getView())
            except pyHFigureNotFound:
                #self.getView().clearSelectedFigures()
                self.getView().update()
                self.delegateTool = pyHViewTranslationTool(self.view)
        self.delegateTool.onMouseDown(e)

    def onMouseUp(self,e):
        self.delegateTool.onMouseUp(e)

    def onMouseMove(self,e):
        self.delegateTool.onMouseMove(e)

    def onMouseDobleClick(self,e):
        pass
    def onMouseWheel(self,e):
        pass
    def onKeyPressed(self,e):
        pass

    def exit(self, e=None):
        print('exit from tool')
        self.getView().clearSelectedFigures()
        drawing = self.getView().getDrawing()
        for f in drawing.getFigures()[:]:
            if isinstance(f, ShowInfoNodeDecorator):
                drawing.removeFigure(f)
                drawing.addFigure(f.getDecoratedFigure())
