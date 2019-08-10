import math

from  MiniTensorFlow.data import operations as ops
from pyHotDraw.Figures.pyHAttributes import pyHAttributeColor, pyHAttributeWidth, pyHAttributeFontSize
from pyHotDraw.Figures.pyHConnectionFigure import pyHConnectionFigure
from pyHotDraw.Figures.pyHTextFigure import pyHTextFigure
from pyHotDraw.Geom.pyHPoint import pyHPoint

COLOR = {'RED':  pyHAttributeColor(255, 0, 0),
         'BLUE': pyHAttributeColor(0, 0, 255),
         'GRAY': pyHAttributeColor(127, 127, 127)}

class pyHADNodeConnectionFigure(pyHConnectionFigure):


    def __init__(self):
        pyHConnectionFigure.__init__(self)

        self.forwardText = pyHTextFigure(0,0,0,0,"")
        self.backwardText = pyHTextFigure(0,0,0,0,"")

        self.set_default_style()

    def set_default_style(self):
        self.setColor(pyHAttributeColor(150, 150, 150, 255))
        self.setAttribute('WIDTH', pyHAttributeWidth(2))

        self.forwardText.setColor(COLOR.get('BLUE'))
        self.forwardText.setAttribute('FONT', pyHAttributeFontSize(12))

        self.backwardText.setColor(COLOR.get('RED'))
        self.backwardText.setAttribute('FONT', pyHAttributeFontSize(12))





















    def figureChanged(self, figure):
        pyHConnectionFigure.figureChanged(self, figure)
        self._movePoints()
        fs = self.startNode()

        if fs.get_node() is not None:
            vf = fs.get_node().getValue()
            vb = fs.get_node().partialGlobal

            if fs.isForwardPrintable():
                self.setForwardText(str(vf))
            if fs.isBackwardPrintable():
                self.setBackwardText(str(vb))

    def setConnectorStart(self, connector):
        pyHConnectionFigure.setConnectorStart(self, connector)
        p = connector.findStart(self)
        self.points.insert(0, p)

        fs = self.getConnectorStart().getOwner()
        if fs.get_node() is not None:
            if fs.isForwardPrintable():
                self.setForwardText(str(fs.get_node().getValue()))

    def setConnectorEnd(self, connector):
        pyHConnectionFigure.setConnectorEnd(self, connector)
        p = connector.findEnd(self)
        self.addPoint(p)
        self._addZigzagForm()
        fs = self.getConnectorStart().getOwner()
        fe = self.getConnectorEnd().getOwner()
        fs.add_output(self)
        fe.add_input(self)

    def startNode(self):
        return self.getConnectorStart().getOwner()

    def endNode(self):
        return self.getConnectorEnd().getOwner()

    def setForwardText(self, t):
        n = ops.truncate(float(t), 2)
        self.forwardText.setText(str(n))

    def setBackwardText(self, t):
        n = ops.truncate(float(t), 2)
        self.backwardText.setText(str(n))

    def getForwardText(self):
        return self.forwardText.getText()

    def getBackwardText(self):
        return self.backwardText.getText()


    def removeLastPoint(self):
        self.points = self.points[:-1]

    # Modify
    def draw(self, g):
        pyHConnectionFigure.draw(self, g)

        p = self.points[0]
        p0  =self.points[-2]
        p1 = self.points[-1]
        self.printArrow(g, p0.getX(), p1.getX(), p0.getY(), p1.getY())
        self._printValues(g, p.getX(), p.getY())

    def _printValues(self, g, x0, y0):
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

    def getColor(self):
        return self.getAttribute('COLOR')

    def getFillColor(self):
        return

    def setFillColor(self, *args):
        pass




    def containPoint(self, point):
        if not self.points: return False

        p0=self.points[0]
        for p1 in self.points[1:]:
            c1 = min(p0.getX(), p1.getX()) <= point.getX() <= max(p0.getX(), p1.getX()) or p0.getX() == p1.getX()
            c2 = min(p0.getY(), p1.getY()) <= point.getY() <= max(p0.getY(), p1.getY()) or p0.getY() == p1.getY()
            if c1 and c2:
                m, n = ops.crear_recta_a_partir_de_2_puntos(p0, p1)
                distance =  ops.distancia_punto_recta(m, n, point)
                if distance <= 30:
                    return True
            p0= p1
        return False


    def printArrow(self, g, x1, x2, y1, y2):
        alpha = math.atan2(y2 - y1, x2 - x1)
        k = 30
        xa = x2 - k * math.cos(alpha + 0.35)
        ya = y2 - k * math.sin(alpha + 0.35)
        g.drawLine(xa, ya, x2, y2)
        xa = x2 - k * math.cos(alpha - 0.35)
        ya = y2 - k * math.sin(alpha - 0.35)
        g.drawLine(xa, ya, x2, y2)

    def _printLine(self, g, x0, x1, y0, y1):
        x = x0 + abs((x1 - x0) / 2)
        y = y0
        # Draw line
        g.drawLine(x0, y0, x, y)
        g.drawLine(x, y, x1, y1)

        return x1, y1

    def _printDoubleLine(self, g, x0, x3, y0, y3):
        x1 = x0 + 100
        y1 = y0
        x2 = x3 - 50
        y2 = y3
        # Draw line
        g.drawLine(x0, y0, x1, y1)
        g.drawLine(x1, y1, x2, y2)
        g.drawLine(x2, y2, x3, y3)

        return x2, y2


    def _movePoints(self):
        points = self.getPoints()
        pl = self.getLastPoint()
        points[1].setX(points[0].getX() + 100)
        points[1].setY(points[0].getY())
        points[2].setX(pl.getX() - 50)
        points[2].setY(pl.getY())


    def _addZigzagForm(self):
        points = self.getPoints()
        p0 = points[0]
        pl = points[-1]
        self.removeLastPoint()
        p_new1 = pyHPoint(p0.getX() + 100, p0.getY())
        p_new2 = pyHPoint(pl.getX() - 50, pl.getY())
        self.addPoint(p_new1)
        self.addPoint(p_new2)
        self.addPoint(pl)
