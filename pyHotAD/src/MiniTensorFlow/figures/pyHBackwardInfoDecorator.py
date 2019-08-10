#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.data.operations import truncate
from pyHotDraw.Figures.pyHDecoratorFigure import pyHDecoratorFigure
from numpy import matrix
from MathTextFigure import format_matrix
from format_values import format_value


class pyHBackwardInfoDecorator(pyHDecoratorFigure):

    def __init__(self, node, end='Y'):
        pyHDecoratorFigure.__init__(self, node)
        self.backwardExp = []
        self._createBackwardInfo()


    def addExpression(self, expression):
        l = self.decorated.get_function_letter()
        # exp = '∂Y / ∂l ='
        exp = (r'\dfrac{\partial \ \varepsilon}{\partial \ %s} = ' % l) + \
              str(expression)
        self.backwardExp.append(exp)

    def getBackwardExpresions(self):
        return self.backwardExp

    @staticmethod
    def _format_result(partial, output_partial):
        is_matrix = isinstance(partial, matrix) and partial.size > 1
        partial_value = format_matrix(
            partial) if is_matrix else format_value(partial)
        is_matrix = isinstance(output_partial, matrix) and output_partial.size > 1
        _output_partial_value = format_matrix(
            output_partial) if is_matrix else format_value(output_partial)

        return partial_value + ' \cdot ' + _output_partial_value




    def _createBackwardInfo(self):
        node = self.decorated
        node_letter = node.get_function_letter()
        parents = node.get_outputs_nodes()
        epsilon = r'\varepsilon'
        if not parents:
            self.addExpression(_partial_frac(node_letter, node_letter))
            #self.addExpression('1')

        else:
            # head = '∂ε / ∂l ='
            head = _partial_frac(epsilon, node_letter) + ' = '
            back_exp = [head] * 4
            separator = ' \ + \ '
            dot = ' \cdot '

            for p in parents:

                parent_letter = p.get_function_letter()
                target = _partial_frac(epsilon, parent_letter)

                #0: algebraic_expression
                algebraic_exp = _partial_frac(parent_letter, node_letter)
                back_exp[0] += target + dot + algebraic_exp + separator

                # 1: local_partial_expression
                parent_exp = p.get_expression(
                    *[i.get_function_letter() for i in p.get_inputs_nodes()]
                )
                partial_local_exp = _partial_frac(parent_exp, node_letter)
                back_exp[1]+= target + dot + partial_local_exp + separator

                #2: partial_local_derived
                partial_local_derived = str(p.get_partial_expressions().get(node))
                invert_order = p.invert_dot_to_calculate_partial().get(node)
                if invert_order:
                    back_exp[2]+= partial_local_derived + dot + target + separator
                else:
                    back_exp[2]+= target + dot + partial_local_derived + separator

                # 3: partial_local_value
                partial_local_value = format_value(p.get_partials().get(node))
                parent_partial = format_value(p.get_partial_global())
                if invert_order:
                    back_exp[3]+= partial_local_value + dot + parent_partial + separator
                else:
                    back_exp[3]+= parent_partial + dot + partial_local_value + separator


            self.backwardExp = [be[:-6] for be in back_exp]



def _partial_frac(numerator, denominator):
    return r' \dfrac{\partial \/ %s}{\partial \/ %s}' %\
           (numerator, denominator)



