

from MiniTensorFlow.figures.Nodes_Expanded.ComplexVNode import VNode
import numpy as np
from MiniTensorFlow.figures.MathTextFigure import MathTextFigure, format_matrix
from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from MiniTensorFlow.microtensorflow.Weight import Weights
from MiniTensorFlow.microtensorflow.FullyConnectedLinear import FullyConnectedLinear
from format_values import *

class FullyConnectFigure(VNode):
    def __init__(self, x, y, w, h):
        VNode.__init__(self, x, y, w, h, 1, 'fc')

        self.add_variable('weight')
        self.add_variable('bias')
        #self.num_outputs = 1
        self.add_variable('neurons')


    def create_node(self):
        input_node = self.get_inputs_nodes()[0].get_node()
        w = self.get_variable('weight')
        b = self.get_variable('bias')
        num_outs = self.get_variable('neurons').value.A[0][0]

        self.node = FullyConnectedLinear(input_node, num_outs, w, b)

    def forward(self):
        NodeFigure.forward(self)
        w = self.get_node()


    def get_expression(self, input_, weight='W', bias='b'):
        i = format_value(input_)
        if is_matrix(input_):
            w = format_value(self.get_variable('weight'))
            b = format_value(self.get_variable('bias'))
        else:
            w = format_value(weight)
            b = format_value(bias)

        if is_float(b) and is_negative(b):
            return r'%s \cdot %s - %s' % (w, i, -1*float(b))

        return r'%s \cdot %s + %s' % (w, i, b)

    def get_partial_expressions(self):
        inputs_nodes = self.get_inputs_nodes()
        i0 = inputs_nodes[0]
        return {i0 : ' W ^T '}

    def invert_dot_to_calculate_partial(self):
        invert = NodeFigure.invert_dot_to_calculate_partial(self)
        invert[self.get_inputs_nodes()[0]] = True
        return invert

    def visit(self,visitor):
        return visitor.visit_fully_connect_figure(self)


    def are_all_inputs_occupied(self):
        inputs_occupied = NodeFigure.are_all_inputs_occupied(self)
        variables_assigned = self.get_variable('neurons') is not None
        return inputs_occupied and variables_assigned