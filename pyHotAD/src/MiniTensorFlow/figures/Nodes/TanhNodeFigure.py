#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: javi
"""
from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from microtensorflow.Tanh import Tanh
from MiniTensorFlow.figures.MathTextFigure import MathTextFigure, format_matrix
from MathExpressionFigure import equal_expression
import numpy as np
from format_values import *

class TanhNodeFigure(NodeFigure):
    def __init__(self, x, y, w, h):
        NodeFigure.__init__(self, x, y, w, h, 1, '\mathrm{\mathsf{tanh}}')


    def create_node(self):
        if self.are_all_inputs_occupied():
            input_node = self.get_inputs_nodes()[0].get_node()
            gate = Tanh(input_node)
            self.set_node(gate)


    def get_expression(self, v):
        return r' tanh \left( %s \right)' % format_value(v)


    def get_partial_expressions(self):
        inputs_node = self.get_inputs_nodes()
        i0 = inputs_node[0]
        return {i0 : r' \left(1 -  tanh ^2 \left( %s \right)\right) ' %
                      i0.get_function_letter()}


    def visit(self, visitor):
        return visitor.visit_tanh_figure(self)
