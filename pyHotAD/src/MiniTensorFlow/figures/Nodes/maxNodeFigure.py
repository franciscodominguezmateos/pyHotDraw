#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 27/02/2017

@author: javi
"""
from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from microtensorflow.Maximum import Maximum
from MiniTensorFlow.figures.MathTextFigure import MathTextFigure, format_matrix
from MathExpressionFigure import equal_expression
import numpy as np
from format_values import *


class maxNodeFigure(NodeFigure):
    def __init__(self, x, y, w, h):
        NodeFigure.__init__(self, x, y, w, h, 2, '\mathrm{\mathsf{max}}')


    def create_node(self):
        if self.are_all_inputs_occupied():
            nodes = self.get_inputs_nodes()
            n0 = nodes[0].get_node()
            n1 = nodes[1].get_node()
            self.set_node(Maximum(n0, n1))

    def get_expression(self, v0, v1):
        i0 = format_value(v0)
        i1 = format_value(v1)
        return r'\mathit{max} \left( %s, \/ %s \right)' % (i0, i1)

    def get_partial_expressions(self):
        inputs_nodes = self.get_inputs_nodes()
        i0 = inputs_nodes[0]
        i1 = inputs_nodes[1]
        i0_exp = ' %s ' % i0.get_function_letter()
        i1_exp = ' %s ' % i1.get_function_letter()

        return {i0 : i1_exp,
                i1 : i0_exp}

    def visit(self,visitor):
        return visitor.visit_max_figure(self)