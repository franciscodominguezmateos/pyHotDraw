

from  MiniTensorFlow.data import operations as ops
from pyHotDraw.Figures.pyHAbstractFigure import pyHAbstractFigure
from pyHotDraw.Figures.pyHAttributes import pyHAttributeColor, pyHAttributeWidth
from pyHotDraw.Figures.pyHTextFigure import pyHTextFigure
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Geom.pyHRectangle import pyHRectangle
from pyHotDraw.Handles.pyHPolylineHandle import pyHPolylineHandle
import numpy as np
from figures.MathTextFigure import MathTextFigure


COLOR = {'RED':  pyHAttributeColor(255, 0, 0),
         'BLUE': pyHAttributeColor(0, 0, 255),
         'GRAY': pyHAttributeColor(127, 127, 127)}

class pyHADOutputNodeFigure(pyHAbstractFigure):

    def __init__(self, conector,l=120):
        pyHAbstractFigure.__init__(self)
        self.setColor(pyHAttributeColor(150, 150, 150, 255))
        self.setAttribute('WIDTH', pyHAttributeWidth(2))

        self.connectorStart = None
        self.points = [None]*2
        self.lenline = l

        self.forwardText = pyHTextFigure(0, 0, 0, 0, "")
        self.forwardText.setColor(COLOR.get('BLUE'))
        self.backwardText = pyHTextFigure(0, 0, 0, 0, "")
        self.backwardText.setColor(COLOR.get('RED'))

        self._error_figure = MathTextFigure(0,0,r'\varepsilon')
        self._error_figure.setColor(pyHAttributeColor(0, 0, 0, 0))
        self.setConnectorStart(conector)




    def getLastPoint(self):
        return self.points[-1]

    def getPoints(self):
        return self.points


    def getDisplayBox(self):
        maxX = 0
        maxY = 0
        minX = 1e90
        minY = 1e90
        for p in self.points:
            if p.getX() < minX:
                minX = p.getX()
            if p.getX() > maxX:
                maxX = p.getX()
            if p.getY() < minY:
                minY = p.getY()
            if p.getY() > maxY:
                maxY = p.getY()
        return pyHRectangle(minX, minY, maxX - minX, maxY - minY)

    def containPoint(self, q):
        for p in self.points:
            if p == q:
                return True
        return False

    def move(self, x, y):
        for p in self.points:
            p.setX(p.getX() + x)
            p.setY(p.getY() + y)


    # handles Method
    def getHandles(self):
        handles = []
        for p in self.points:
            handles.append(pyHPolylineHandle(self, p))
        return handles

    # Connector handle
    def setConnectorStart(self, connector):
        connector = connector[0] if isinstance(connector, list) else connector
        self.connectorStart = connector
        p0 = connector.findStart(self)
        self.points[0] = p0
        self.points[1] = pyHPoint(p0.getX() + self.lenline, p0.getY())

        connector.getOwner().addChangedFigureObserver(self)

    def getConnectorStart(self):
        return self.connectorStart

    # Observer pattern method, self is a Observer of connector owners

    def figureChanged(self, figure):
        ps = self.getConnectorStart().findStart(self)

        self.points[0].setX(ps.getX())
        self.points[0].setY(ps.getY())
        self.points[-1].setX(ps.getX() + self.lenline)
        self.points[-1].setY(ps.getY())

        self._print_forward_and_backward_values()

    @staticmethod
    def _is_scalar(value):
        if isinstance(value, np.matrix):
            if value.A.size == 1:
                return True, value.A[0][0]
            else:
                return False, value
        elif isinstance(value, (int, float)):
            return True, value
        else:
            return False, value

    def _print_forward_and_backward_values(self):
        """
        Dibuja el valor de las operaciones forward y backward en la conexión
        si el nodo lo permite, y el valor no es una matriz.
        :return:
        """
        start_node = self.getConnectorStart().getOwner()
        if start_node.get_node():
            if start_node.isForwardPrintable():
                forward_value = start_node.get_node().getValue()
                is_scalar, value = self._is_scalar(forward_value)
                if is_scalar:
                    self.forwardText.setText(
                        '{:.3f}'.format(value))
                else:
                    self.forwardText.setText('')

            if start_node.isBackwardPrintable():
                backward_value = start_node.get_node().partialGlobal
                is_scalar, value = self._is_scalar(backward_value)
                if is_scalar:
                    self.backwardText.setText(
                        '{:.3f}'.format(value))
                else:
                    self.backwardText.setText('')

    # visitor method
    def visit(self, visitor):
        pass



    def setForwardText(self, t):
        n = ops.truncate(float(t), 3)
        self.forwardText.setText(str(n))

    def setBackwardText(self, t):
        n = ops.truncate(float(t), 3)
        self.backwardText.setText(str(n))

    def getForwardText(self):
        return self.forwardText.getText()

    def getBackwardText(self):
        return self.backwardText.getText()

    def getColor(self):
        return self.getAttribute('COLOR')


    # Modify
    def draw(self, g):
        pyHAbstractFigure.draw(self, g)
        if self.points:
            x0 = self.points[0].getX()
            y0 = self.points[0].getY()
            x1 = self.points[0].getX() + self.lenline
            y1 = self.points[0].getY()

            g.drawLine(x0, y0, x1, y1)
            ops.printArrow(g, x0, x1, y0, y1)
            self._printValues(g, x0, y0)

            self._error_figure.set_position(x1+5, y1-45)
            self._error_figure.draw(g)


    def _printValues(self, g, x0, y0):
        pyHAbstractFigure.draw(self, g)
        n = self.getConnectorStart().getOwner()
        if n.isForwardPrintable():
            # print Forward Text
            self.forwardText.x0 = x0 + 10
            self.forwardText.y0 = y0 + 10
            self.forwardText.draw(g)
        if n.isBackwardPrintable():
            # print Backward Text
            self.backwardText.x0 = x0 + 10
            self.backwardText.y0 = y0 - 30
            self.backwardText.draw(g)




