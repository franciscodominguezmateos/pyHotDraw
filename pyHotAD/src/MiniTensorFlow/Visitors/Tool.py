from pyHotDraw.Core.Exceptions import pyHFigureNotFound
from pyHotDraw.Figures.pyHAttributes import pyHAttributeWidth
from pyHotDraw.Geom.pyHPoint import pyHPoint


class Tool(object):
    '''
    classdocs
    '''

    def __init__(self, v, fig):
        '''
        Constructor
        '''
        self.view = v
        self.selectedNode = False
        self.fig = fig



    def getView(self):
        return self.view

    def onMouseDown(self, e):
        print('Tool')


    def onMouseUp(self, e):
        pass

    def onMouseMove(self, e):
        p = pyHPoint(e.getX(), e.getY())
        try:
            f = self.view.findFigure(p)
            if self.fig == f:
                self.fig.setAttribute('WIDTH', pyHAttributeWidth(4))
            else:
                self.fig.setAttribute('WIDTH', pyHAttributeWidth(2))
        except pyHFigureNotFound:
            self.fig.setAttribute('WIDTH', pyHAttributeWidth(2))

    def onMouseDobleClick(self, e):
        pass

    def onMouseWheel(self, e):
        pass

    def onKeyPressed(self, e):
        pass
