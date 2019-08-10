#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.data.step import step
from MiniTensorFlow.data.operations import truncate, is_float
from MathTextFigure import MathTextFigure, format_matrix
from MathExpressionFigure import MathExpressionFigure, equal_expression
from numpy import matrix
from format_values import format_value

class AbstractForwardStep(step):

    def __init__(self, node, view):
        step.__init__(self, node, view)
        self._steps_list = [self.step0, self.step1, self.step2, self.step3]
        self.node.get_node().forward()


    def step0(self):
        """
        Vuelve opaco el nodo sobre el que se mostrará la información, así como sus
        nodos entrada (y sus respectivos conectores)
        """
        #self._makeFigureOpaque(self.node)
        self.makeNodeEnphasis(self.node)

        for input_conector in self.node.get_inputs_links():
            self.makeConnectorEnphasis(input_conector)
            self.makeNodeEnphasis(input_conector.get_start_node())

    def step1(self):
        """
        Muestra la operación algebraica a realizar
        """

        #self.info_figure.set_math_text(self.f + self.node.getForwardOps()[0])
        inputs_nodes = self.node.get_inputs_nodes()
        inputs_letters = [n.get_function_letter() for n in inputs_nodes]
        expression_figure = self.node.get_figure_expression(*inputs_letters)
        self.set_info_figure(expression_figure)

        self.moveFigureText()


    def step2(self):
        """
        Muestra la operación con sus valores
        :return:
        """
        inputs_nodes = self.node.get_inputs_nodes()
        inputs_values = [n.get_value() for n in inputs_nodes]
        expression_figure = self.node.get_figure_expression(*inputs_values)
        self.set_info_figure(expression_figure)
        self.moveFigureText()

    def step3(self):
        """
        Muestra el valor de la operación
        :return:
        """
        value = self.node.get_value()
        text = self.node.get_function_letter() + ' \ = \ ' + format_value(value)
        expression_figure = MathTextFigure(0, 0, text, use_latex=True)
        self.set_info_figure(expression_figure)
        self.moveFigureText()


    def moveFigureText(self):
        x = (2 * self.node.getX() + self.node.getWidth() - self.info_figure.w) / 2
        y = self.node.getY() + self.node.getHeight() + 20
        self.info_figure.move(x, y)





