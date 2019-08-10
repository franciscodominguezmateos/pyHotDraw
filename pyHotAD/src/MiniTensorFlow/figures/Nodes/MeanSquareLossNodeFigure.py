from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
from MiniTensorFlow.microtensorflow.MeanSquareLoss import MeanSquareLoss
import numpy as np
from MiniTensorFlow.figures.MathTextFigure import MathTextFigure, format_matrix
from format_values import *

class MeanSquareLossNodeFigure(NodeFigure):
    def __init__(self, x, y, w, h):
        NodeFigure.__init__(self, x, y, w, h, 2, 'mse')

    def create_node(self):
        nodes = self.get_inputs_nodes()
        y = nodes[0].get_node()
        predictions = nodes[1].get_node()
        self.set_node(MeanSquareLoss(y, predictions))


    def get_expression(self, prediction, obteined):
        p = format_value(prediction)
        o = format_value(obteined)
        n_value = 'n'
        if is_matrix(o): n_value = o.shape[1]
        if is_float(o): n_value = 1

        n = format_value(n_value)
        if is_float(o) and is_negative(o):
            return r'\dfrac {( %s + %s ) ^2}{%s} ' % (p, -1*float(o), n)
        return r'\dfrac {\left( %s - %s \right) ^2}{%s} ' % (p, o, n)


    def get_partial_expressions(self):
        inputs_nodes = self.get_inputs_nodes()
        i0 = inputs_nodes[0]
        i1 = inputs_nodes[1]
        exp = r' \dfrac {2(%s - %s)}{n}'
        i0_exp = exp % (i0.get_function_letter(), i1.get_function_letter())
        i1_exp = exp % (i1.get_function_letter(), i0.get_function_letter())

        return {i0 : i0_exp,
                i1 : i1_exp}


    def visit(self,visitor):
        return visitor.visit_mean_square_loss_figure(self)