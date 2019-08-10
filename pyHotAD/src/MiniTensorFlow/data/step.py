#!/usr/bin/python
# -*- coding: utf-8 -*-


from MiniTensorFlow.figures.pyHColorNodeDecorator import pyHColorNodeDecorator
from MiniTensorFlow.figures.MathTextFigure import MathTextFigure
from pyHotDraw.Figures.pyHAttributes import pyHAttributeFillColor
from MiniTensorFlow.figures.pyHColorConnectorDecorator import pyHColorConnectorDecorator
from figures.MathTextFigure import format_matrix
from numpy import matrix

class step(object):


    def __init__(self, node, view):
        self.node = node
        self.view = view

        self.step = 0
        self._steps_list = []

        self.info_figure = None  #MathTextFigure(0, 0)
        #self.infoFigure.setFillColor(255, 255, 255, 255)


    def nextStep(self):
        """
        Show the next information.
        :return:
        """
        self._steps_list[self.step]()
        self.step += 1


    def hasNextStep(self):
        """
        :return: Informa si quedan pasos por realizar
        """
        return self.step < len(self._steps_list)


    def moveFigureText(self):
        """
        To implemet for the child class.
        Move the 'Information Figure' to right place.
        :return:
        """
        pass

    def endStep(self):
        pass

    def get_info_figure(self):
        return self.info_figure

    def set_info_figure(self, figure):
        drawing = self.view.getDrawing()
        if self.info_figure:
            drawing.removeFigure(self.info_figure)
        self.info_figure = figure
        figure.setAttribute('FILL', pyHAttributeFillColor(255, 255, 255, 255))
        drawing.addFigure(figure)
        self.view.update()

    def assign_figure_text(self, text, size=20):
        self.set_info_figure(MathTextFigure(0,0,text, size, True))


    @staticmethod
    def makeNodeSemitransparent(node):
        decorated_figure = pyHColorNodeDecorator(node)
        decorated_figure.makeSemitransparent()

    @staticmethod
    def makeNodeOpaque(node):
        decorated_figure = pyHColorNodeDecorator(node)
        decorated_figure.makeNormal()

    @staticmethod
    def makeNodeEnphasis(node):
        decorated_figure = pyHColorNodeDecorator(node)
        decorated_figure.makeEmphasis()

    @staticmethod
    def makeConnectorSemitransparent(connector):
        decorated_figure = pyHColorConnectorDecorator(connector)
        decorated_figure.makeSemitransparent()

    @staticmethod
    def makeConnectorOpaque(connector):
        decorated_figure = pyHColorConnectorDecorator(connector)
        decorated_figure.makeNormal()

    @staticmethod
    def makeConnectorEnphasis(connector):
        decorated_figure = pyHColorConnectorDecorator(connector)
        decorated_figure.makeEmphasis()
