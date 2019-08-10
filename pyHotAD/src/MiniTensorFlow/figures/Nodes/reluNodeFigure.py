#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: javi
"""
from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from MiniTensorFlow.microtensorflow.ReLU import ReLU
from format_values import *


class reluNodeFigure(NodeFigure):
    def __init__(self, x, y, w, h):
        NodeFigure.__init__(self, x, y, w, h, 1, '\mathrm{\mathsf{ReLU}}')


    def create_node(self):
        if self.are_all_inputs_occupied():
            input_node = self.get_inputs_nodes()[0].get_node()
            self.set_node(ReLU(input_node))

    def get_expression(self, v):
        i = format_value(v)
        if is_matrix(v):
            return r' max(0, \/ n), \/ n $ is $ %s' % i
        return r' max(0, \/ %s)' % i

    def get_partial_expressions(self):
        inputs_node = self.get_inputs_nodes()
        i0 = inputs_node[0]

        return {i0 : ' max \prime (0, %s) ' % i0.get_function_letter()}



    def visit(self,visitor):
        return visitor.visit_relu_figure(self)