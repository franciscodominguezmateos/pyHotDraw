#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.data.step import step
from MiniTensorFlow.data.operations import truncate
from copy import deepcopy
from numpy import matrix
from format_values import *


class WeightUpdateStep(step):

    def __init__(self, node, alpha, view):
        step.__init__(self, node, view)
        self._alpha = alpha

        self._steps_list = [self.step0, self.step1, self.step2, self.step3, self.step4]
        # self.node.getNode().update(self._alpha)
        self.intro_eq = '{}^\prime = '.format(self.node.get_function_letter())

    def step0(self):
        """
        Vuelve opaco el nodo cuyo peso será actualizado
        """
        self.makeNodeEnphasis(self.node)
        for output_conector in self.node.get_outputs_links():
            self.makeConnectorEnphasis(output_conector)


    def step1(self):
        """
        Muestra la operación a realizar
        """
        node_text  = self.node.get_function_letter()
        self.assign_figure_text(self.intro_eq + node_text +
                                       r' - \alpha \cdot \dfrac{\partial \varepsilon}{\partial '
                                       + node_text + '}')
        self.moveFigureText()
        self.view.update()

    def step2(self):
        """
        Muestra los valores de la operación
        :return:
        """
        value = format_value(self.node.get_value())
        dvalue = format_value(self.node.get_partial_global())

        if is_float(dvalue) and is_negative(dvalue):
            text = '{} {} - {}  \cdot ({})'.format(self.intro_eq, value, self._alpha, dvalue)
        else:
            text = '{} {} - {}  \cdot {}'.format(self.intro_eq, value, self._alpha, dvalue)
        self.assign_figure_text(text)
        self.moveFigureText()

        self.view.update()

    def step3(self):
        """
        Muestra el valor de la operación
        :return:
        """
        """
        w = self.node.get_node().getValue()
        p = self.node.get_node().get_partial_value()
        value = self._gradient_descent(w, self._alpha, p)
        value = truncate(value, 2)
        """
        copia = deepcopy(self.node.get_node())
        copia.update(self._alpha)
        value = format_value(copia.getValue())
        self.info_figure.set_math_text('{} {}'.format(self.intro_eq, value))
        self.moveFigureText()

    def step4(self):
        """
        Elimina la figura de información y muestra el resultado de la operación 'backward' en su
        conector de salida.
        :return:
        """
        self.node.get_node().update(self._alpha)
        self.node.notifyFigureChanged()
        self.view.getDrawing().removeFigure(self.info_figure)


    def endStep(self):
        self.makeNodeOpaque(self.node)
        for out_conector in self.node.get_outputs_links():
            self.makeConnectorOpaque(out_conector)


    
    def moveFigureText(self):
        x = (2 * self.node.getX() + self.node.getWidth() - self.info_figure.w) / 2
        y = self.node.getY() + self.node.getHeight() + 20
        self.info_figure.x0 = x
        self.info_figure.y0 = y



