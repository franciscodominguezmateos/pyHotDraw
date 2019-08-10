#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.figures.pyHBackwardInfoDecorator import pyHBackwardInfoDecorator
from MiniTensorFlow.figures.MathTextFigure import MathTextFigure

from MiniTensorFlow.handles.pyHBackwardHandle import pyHBackwardHandle
from MiniTensorFlow.handles.pyHForwardHandle import pyHForwardHandle
from pyHotDraw.Figures.pyHAttributes import pyHAttributeFillColor
from pyHotDraw.Figures.pyHDecoratorFigure import pyHDecoratorFigure
from pyHotDraw.Geom.pyHPoint import pyHPoint


class pyHHandleInfoDecorator(pyHDecoratorFigure):

    def __init__(self, owner, view):
        pyHDecoratorFigure.__init__(self, owner)
        self.view = view

        self.forward_index = 0
        self.forward_exp = owner.forwardExp if owner.forwardExp else None
        if not owner.is_input():
            self.forward_exp = self.forward_exp[:-1]

        self.backward_index = 0
        self.backward_exp = pyHBackwardInfoDecorator(owner).getBackwardExpresions()

        self.info_figure = MathTextFigure(0, 0)
        self.info_figure.setFillColor(255,255,255,255)

    def addChangedFigureObserver(self, f):
        self.getDecoratedFigure().addChangedFigureObserver(f)

    def getHandles(self):
        r = self.getDecoratedFigure().getDisplayBox()
        x = r.getX()
        y = r.getY()
        w = r.getWidth()
        h = r.getHeight()

        h0 = pyHBackwardHandle(self, pyHPoint(x + w, y - 20))
        h0.handle_figure.setAttribute('FILL', pyHAttributeFillColor(255, 0, 0, 200))

        h1 = pyHForwardHandle(self, pyHPoint(x + w, y + h))
        h1.handle_figure.setAttribute('FILL', pyHAttributeFillColor(0, 0, 255, 200))

        handles = [h0, h1]

        return handles


    def removeFigure(self):
        self.view.getDrawing().removeFigure(self.info_figure)


    def showForwardInfo(self, x, y):
        if self.forward_index < len(self.forward_exp):
            self._drawForwardInfo(x, y)
            self.forward_index += 1

        else:
            self.forward_index = 0
            self.view.getDrawing().removeFigure(self.info_figure)
            self.info_figure = MathTextFigure(0, 0)
            self.info_figure.setFillColor(255, 255, 255, 255)

    def _drawForwardInfo(self, x, y):
        self.info_figure.set_math_text(self.forward_exp[self.forward_index])

        self.info_figure.x0 = x - self.decorated.getWidth()
        self.info_figure.y0 = y

        if self.forward_index is 0:
            self.view.getDrawing().addFigure(self.info_figure)

    def showBackwardInfo(self, x, y):
        if self.backward_index < len(self.backward_exp):
            self._drawBackwardInfo(x, y)
            self.backward_index += 1

        else:
            self.backward_index = 0
            self.view.getDrawing().removeFigure(self.info_figure)
            self.info_figure = MathTextFigure(0, 0)
            self.info_figure.setFillColor(255, 255, 255, 255)

    def _drawBackwardInfo(self, x, y):
        self.info_figure.set_math_text(self.backward_exp[self.backward_index])

        self.info_figure.x0 = x -10 - self.info_figure.w
        self.info_figure.y0 = y - self.decorated.getHeight()

        if self.backward_index is 0:
            self.view.getDrawing().addFigure(self.info_figure)








