from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from MiniTensorFlow.microtensorflow.SquareLoss import SquareLoss
import numpy as np
from MiniTensorFlow.figures.MathTextFigure import MathTextFigure, format_matrix
from format_values import *

class SquareLossNodeFigure(NodeFigure):
    def __init__(self, x, y, w, h):
        NodeFigure.__init__(self, x, y, w, h, 2, 'se')


    def create_node(self):
        nodes = self.get_inputs_nodes()
        y = nodes[0].get_node()
        predictions = nodes[1].get_node()
        self.set_node(SquareLoss(y, predictions))

    def get_expression(self, prediction, obteined):
        p = format_value(prediction)
        o = format_value(obteined)

        if is_float(o) and is_negative(o):
            return r' ( %s + %s ) ^2' % (p, -1*float(o))
        return r' \left( %s - %s \right) ^2 ' % (p, o)

    def get_partial_expressions(self):
        inputs_nodes = self.get_inputs_nodes()
        i0 = inputs_nodes[0]
        i1 = inputs_nodes[1]
        exp = r'\left(  2 \left( %s - %s \right) \right) '
        i0_exp = exp % (i0.get_function_letter(), i1.get_function_letter())
        i1_exp = exp % (i1.get_function_letter(), i0.get_function_letter())

        return {i0 : i0_exp,
                i1 : i1_exp}

    def visit(self,visitor):
        return visitor.visit_square_loss_figure(self)