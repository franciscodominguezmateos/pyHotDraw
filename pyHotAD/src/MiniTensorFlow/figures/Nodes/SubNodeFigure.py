#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: javi
"""
from MiniTensorFlow.data.operations import is_float
from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from microtensorflow.Sub import Sub
from MathExpressionFigure import equal_expression
from MathTextFigure import MathTextFigure, format_matrix
import numpy as np
from format_values import *


class SubNodeFigure(NodeFigure):
    def __init__(self, x, y, w, h):
        NodeFigure.__init__(self, x, y, w, h, 2, '\mathrm{\mathsf{sub}}')


    def create_node(self):
        if self.are_all_inputs_occupied():
            nodes = self.get_inputs_nodes()
            n0 = nodes[0].get_node()
            n1 = nodes[1].get_node()
            self.set_node(Sub(n0, n1))


    def get_expression(self, v0, v1):
        i0 = format_value(v0)
        i1 = format_value(v1)
        if is_float(v1) and is_negative(v1):
            return '%s + %s' % (i0, 1*float(i1))
        return '%s - %s' % (i0, i1)

    def get_partial_expressions(self):
        inputs_nodes = self.get_inputs_nodes()
        i0 = inputs_nodes[0]
        i1 = inputs_nodes[1]

        return {i0: '1',
                i1: '(-1)'}

    def visit(self,visitor):
        return visitor.visit_sub_figure(self)