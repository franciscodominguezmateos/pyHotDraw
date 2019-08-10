#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.figures.pyHBackwardInfoDecorator import pyHBackwardInfoDecorator

from MiniTensorFlow.data.step import step
from MiniTensorFlow.data.operations import truncate
from MathTextFigure import MathTextFigure, format_matrix
from MathExpressionFigure import MathExpressionFigure, equal_expression
from numpy import matrix
from format_values import format_value

class AbstractBackwardStep(step):

    def __init__(self, node, view):
        step.__init__(self, node, view)
        self._alg_ops_i = 0
        self._algebraics_operations = []
        #self.info_figure = MathTextFigure(0,0, use_latex=True)
        self.back_exp = pyHBackwardInfoDecorator(node)

        # create steps_list
        self._steps_list = [self.step0]
        for alg_op in self.back_exp.getBackwardExpresions():
            self._steps_list.append(self.step1)
            self._algebraics_operations.append(alg_op)

        self._steps_list += [self.step2, self.step3]

        self.node.get_node().backward()

    def step0(self):
        """
        To implemet for the child class.
        """
        raise NotImplementedError

    def step1(self):
        """
        Muestra la operación algebraica a realizar, y su desarrollo
        """
        text_info = self._algebraics_operations[self._alg_ops_i]
        self._alg_ops_i += 1
        #self.view.getDrawing().removeFigure(self.info_figure)
        self.assign_figure_text(text_info, 18)
        self.moveFigureText()
        self.view.update()

    def step2(self):
        """
        Muestra el valor de la operación
        :return:
        """
        """
        v = truncate(self.node.get_node().getPartialValue(), 2)
        self.back_exp.addExpression(v)
        self.info_figure.set_math_text(self.back_exp.getBackwardExpresions()[-1])
        self.moveFigureText()
        """

        value = format_value(self.node.get_partial_global())

        self.back_exp.addExpression(value)

        self.assign_figure_text(self.back_exp.getBackwardExpresions()[-1], 18)
        self.moveFigureText()


    def step3(self):
        """
        Elimina la figura de información y muestra el resultado de la operación 'backward' en su
        conector de salida.
        :return:
        """
        self.node.setBackwardPrintable(True)
        self.view.getDrawing().removeFigure(self.info_figure)

        for out_conector in self.node.get_outputs_links():
            self.makeNodeOpaque(out_conector.get_end_node())

        self.view.update()



    def moveFigureText(self):
        x = (2 * self.node.getX() + self.node.getWidth() - self.info_figure.w) / 2
        y = self.node.getY() + self.node.getHeight() + 20
        self.info_figure.x0 = x
        self.info_figure.y0 = y

