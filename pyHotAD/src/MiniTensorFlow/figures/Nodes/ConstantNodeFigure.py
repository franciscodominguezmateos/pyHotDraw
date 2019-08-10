#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: javi
"""
from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from microtensorflow.Variable import Variable
from pyHotDraw.Figures.pyHAttributes import *


class ConstantNodeFigure(NodeFigure):
    _IS_WEIGHT = False

    def __init__(self, x, y, w, h, text='x_0'):
        NodeFigure.__init__(self, x, y, w, h, 0, text)
        self.setForwardPrintable(True)

        self.setFillColor(220, 220, 220, 255)  # green
        self.figures[0].setColor(pyHAttributeColor(170, 170, 170, 255))
        self._paint()

    def isWeight(self):
        return self._IS_WEIGHT

    def setValue(self, v):
        self.set_node(Variable(v))

    def create_node(self):
        v = self.get_node().getValue()
        self.setValue(v)

    def get_expression(self):
        return self.get_text()


    def visit(self, visitor):
        return visitor.visit_input_figure(self)

    def _paint(self):
        for f in self.get_inputs_sockets():
            self.paint_socket(f)
        for f in self.get_outputs_sockets():
            self.paint_socket(f)

