#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: javi
"""
from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from microtensorflow.Sigmoid import Sigmoid
from MiniTensorFlow.figures.MathTextFigure import MathTextFigure, format_matrix
from MathExpressionFigure import equal_expression
import numpy as np
from format_values import *


class sigmoidNodeFigure(NodeFigure):
    def __init__(self, x, y, w, h):
        NodeFigure.__init__(self, x, y, w, h, 1, '\mathrm{\mathsf{sig}}')

    def create_node(self):
        if self.are_all_inputs_occupied():
            input_node = self.get_inputs_nodes()[0].get_node()
            gate = Sigmoid(input_node)
            self.set_node(gate)

    def get_expression(self, v):
        i = format_value(v)
        if is_float(v):
            if is_negative(v):
                return r' \dfrac{1}{1 + e^{%s}}' % i
            else:
                return r' \dfrac{1}{1 + e^{-%s}}' % i
        if is_matrix(v):
            i_n = self.get_inputs_nodes()
            n = i_n[0].get_function_letter() if i_n else 'n'
            return r' \dfrac{1}{1 + e^{-%s}}, \/ %s $ is $ %s' % (n, n, i)

        return r' \dfrac{1}{1 + e^{-%s}}' % i


    def get_partial_expressions(self):
        inputs_node = self.get_inputs_nodes()
        i0 = inputs_node[0]
        l = self.get_function_letter()
        return {i0 : ' ({0}({1}) (1 - {0}({1}))) '.format(
            l, i0.get_function_letter())}


    def visit(self,visitor):
        return visitor.visit_sigmoid_figure(self)
