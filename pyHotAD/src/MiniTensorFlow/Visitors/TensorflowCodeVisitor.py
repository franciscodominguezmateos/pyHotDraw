
# -*- coding: utf-8 -*-
"""
Visita todas las figuras para generar un codigo de pyBackPropNet

@autor: Javi
"""
import numpy as np
from format_values import *


class TensorflowCodeVisitor:
    FORBIDDEN_CHARS = '\{}()[],- ^~$%=ºª¿?+-* '

    def __init__(self):
        self.inputs = set()
        self.graph = {}  # k: node, v: var name assigned for tf


    def visitCompositeFigure(self,cf):
        for f in cf.getFigures():
            visited_figure = f.visit(self)
            if visited_figure:
                pass

    def visitDecoratorFigure(self,df):
        pass


    def visit_input_figure(self, i_node):
        node_name = self.remove_forbidden_chars(i_node.get_text())
        var_name = self.format_input_name(node_name)
        self.graph[i_node] = var_name
        return var_name, \
               'tf.placeholder(tf.float32, {0}_value.shape, name= \'{0}\')'.\
                   format(var_name)

    def visitWeightFigure(self, w_node):
        node_name = self.remove_forbidden_chars(w_node.get_text())
        var_name = self.format_input_name(node_name)
        self.graph[w_node] = var_name
        value = w_node.get_node().getValue()
        return var_name, 'tf.Variable({}, dtype=tf.float32, name= \'{}\')'.format(self._format(value), var_name)


    def visitSumFigure(self, s_node):
        node_name = s_node.get_function_letter()
        var_name = self.remove_forbidden_chars(node_name)
        self.graph[s_node] = var_name
        inputs = s_node.get_inputs_nodes()
        i0 = self.graph.get(inputs[0])
        i1 = self.graph.get(inputs[1])
        return var_name, r"tf.add({}, {}, name='{}')".format(i0, i1, var_name)

    def visitMulFigure(self, m_node):
        node_name = m_node.get_function_letter()
        var_name = self.remove_forbidden_chars(node_name)
        self.graph[m_node] = var_name
        inputs = m_node.get_inputs_nodes()
        i0 = self.graph.get(inputs[0])
        i1 = self.graph.get(inputs[1])
        return var_name, \
               r"create_mul({}, {}, name='{}')".format(i0, i1, var_name)

    def visit_sigmoid_figure(self, s_node):
        node_name = s_node.get_function_letter()
        var_name = self.remove_forbidden_chars(node_name)
        self.graph[s_node] = var_name
        inputs = s_node.get_inputs_nodes()
        i0 = self.graph.get(inputs[0])
        return var_name, r"tf.sigmoid({}, name='{}')".format(i0, var_name)


    def visit_fully_connect_figure(self, fc_node):
        node_name = fc_node.get_function_letter()
        var_name = self.remove_forbidden_chars(node_name)
        self.graph[fc_node] = var_name
        inputs = fc_node.get_inputs_nodes()
        i0 = self.graph.get(inputs[0])
        n_outs = int(fc_node.get_variable('neurons').getValue())
        return var_name, \
               r"tf.contrib.layers.fully_connected({}, {}, activation_fn=None)"\
                   .format(i0, n_outs)

    def visit_mean_square_loss_figure(self, msl_node):
        node_name = msl_node.get_function_letter()
        var_name = self.remove_forbidden_chars(node_name)
        self.graph[msl_node] = var_name
        inputs = msl_node.get_inputs_nodes()
        y = self.graph.get(inputs[0])
        p = self.graph.get(inputs[1])
        return var_name, \
               r"tf.losses.mean_squared_error({}, {})".format(y, p)

    def visitNodeConnector(self, nc):
        pass


    # tanh
    def visit_tanh_figure(self, s_node):
        node_name = s_node.get_function_letter()
        var_name = self.remove_forbidden_chars(node_name)
        self.graph[s_node] = var_name
        inputs = s_node.get_inputs_nodes()
        i0 = self.graph.get(inputs[0])
        return var_name, r"tf.tanh({}, name='{}')".format(i0, var_name)

    # ReLU
    def visit_relu_figure(self, s_node):
        node_name = s_node.get_function_letter()
        var_name = self.remove_forbidden_chars(node_name)
        self.graph[s_node] = var_name
        inputs = s_node.get_inputs_nodes()
        i0 = self.graph.get(inputs[0])
        return var_name, r"tf.nn.relu({}, name='{}')".format(i0, var_name)

    # square error
    def visit_square_loss_figure(self, msl_node):
        node_name = msl_node.get_function_letter()
        var_name = self.remove_forbidden_chars(node_name)
        self.graph[msl_node] = var_name
        inputs = msl_node.get_inputs_nodes()
        y = self.graph.get(inputs[0])
        p = self.graph.get(inputs[1])
        return var_name, \
               r"tf.losses.tf.square({}, {})".format(y, p)

    # max
    def visit_max_figure(self, s_node):
        node_name = s_node.get_function_letter()
        var_name = self.remove_forbidden_chars(node_name)
        self.graph[s_node] = var_name
        inputs = s_node.get_inputs_nodes()
        i0 = self.graph.get(inputs[0])
        i1 = self.graph.get(inputs[1])
        return var_name, r"tf.maximum({}, {}, name='{}')".format(i0, i1, var_name)

    # sub
    def visit_sub_figure(self, s_node):
        node_name = s_node.get_function_letter()
        var_name = self.remove_forbidden_chars(node_name)
        self.graph[s_node] = var_name
        inputs = s_node.get_inputs_nodes()
        i0 = self.graph.get(inputs[0])
        i1 = self.graph.get(inputs[1])
        return var_name, r"tf.subtract({}, {}, name='{}')".format(i0, i1, var_name)






    def format_input_name(self, var_name):
        var_name = self.remove_forbidden_chars(var_name)
        if not var_name in self.inputs:
            self.inputs.add(var_name)
        else:
            i = 0
            while '{}_{}'.format(var_name, i) in self.inputs:
                i += 1
            var_name = '{}_{}'.format(var_name, i)
            self.inputs.add(var_name)
        return var_name

    def remove_forbidden_chars(self, string):
        """
        Elimina los caracteres que no pueden ser usados en python a la hora de
        crear una variable.
        :param string:
        :return:
        """
        return string.translate({ord(c): None for c in self.FORBIDDEN_CHARS})

    def _format(self, v):
        if is_float(v):
            return float(v)
        elif is_matrix(v):
            return 'np.' + repr(v)
        return v