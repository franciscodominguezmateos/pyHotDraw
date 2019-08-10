from MiniTensorFlow.data.nodeInfo import nodeInfo
from MiniTensorFlow.figures.MathTextFigure import MathTextFigure

from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from pyHotDraw.Core.Exceptions import pyHFigureNotFound
from pyHotDraw.Geom.pyHPoint import pyHPoint


class pyHInfoNodeTool(object):
    '''
    classdocs
    '''

    def __init__(self, v, n_fn):
        '''
        Constructor
        '''
        self.view = v
        self.selectedNode = False
        self.n_fn = n_fn
        self.nodeInfo = None
        self.mtfigure = None



    def getView(self):
        return self.view

    def resetNodeColor(self):
        self.selectedNode = False
        for fig in self.view.getDrawing().getFigures():
            if isinstance(fig, NodeFigure):
                fig.resetColor()

    def addMathFigure(self, f):
        if self.mtfigure is not None and f is not self.mtfigure:
            self.view.getDrawing().removeFigure(self.mtfigure)
            self.mtfigure= None
        try:
            self.nodeInfo = nodeInfo(f, self.n_fn)
            h = f.getHandles()[3]
            p = h.point
            self.mtfigure = MathTextFigure(p.getX(), p.getY())
            self.mtfigure.set_math_text(self.nodeInfo.getForwardExpresion())
            self.view.getDrawing().addFigure(self.mtfigure)
        except:
            pass


    def onMouseDown(self, e):
        p = pyHPoint(e.getX(), e.getY())
        try:
            f = self.view.findFigure(p)
            self.selectedNode = True

            self.addMathFigure(f)

            for figure in self.view.getDrawing().getFigures():
                if isinstance(figure, basicNodeFigure):
                    if figure not in self.nodeInfo.getForwardNodes():
                        figure.setTransparent()
                    else:
                        figure.resetColor()

            self.view.update()

        except pyHFigureNotFound:
            pass


    def onMouseUp(self, e):
        pass

    def onMouseMove(self, e):
        pass

    def onMouseDobleClick(self, e):
        pass

    def onMouseWheel(self, e):
        pass

    def onKeyPressed(self, e):
        if self.mtfigure is not None:
            self.view.getDrawing().removeFigure(self.mtfigure)
            self.mtfigure= None
        self.resetNodeColor()
