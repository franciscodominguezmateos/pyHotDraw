#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: javi
"""
from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from microtensorflow.Variable import Variable
from pyHotDraw.Figures.pyHAttributes import *


class VariableNodeFigure(NodeFigure):

    _IS_WEIGHT = True

    def __init__(self, x, y, w, h, text='w_0'):
        NodeFigure.__init__(self, x, y, w, h, 0, text)
        self.setForwardPrintable(True)


        self.setFillColor(189, 221, 187, 255)  # green
        self.figures[0].setColor(pyHAttributeColor(136, 159, 135, 255))
        self._paint()

    def isWeight(self):
        return self._IS_WEIGHT

    def setValue(self, v):
        self.set_node(Variable(v))

    def create_node(self):
        v = self.get_node().getValue()
        self.setValue(v)

    def get_expression(self):
        value = self.get_text()
        return value

    def visit(self,visitor):
        return visitor.visitWeightFigure(self)

    def _paint(self):
        for f in self.get_inputs_sockets():
            self.paint_socket(f)
        for f in self.get_outputs_sockets():
            self.paint_socket(f)