#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

from  MiniTensorFlow.data import operations as ops
from pyHotDraw.Figures.pyHAttributes import *
from pyHotDraw.Figures.pyHConnectionFigure import pyHConnectionFigure
from pyHotDraw.Figures.pyHTextFigure import pyHTextFigure
from MiniTensorFlow.figures.MatrixFigure import MatrixFigure
from pyHotDraw.Geom.pyHPoint import pyHPoint
import numpy as np
from format_values import *



COLOR = {'RED':  pyHAttributeColor(255, 0, 0),
         'BLUE': pyHAttributeColor(0, 0, 255),
         'GRAY': pyHAttributeColor(127, 127, 127)}

class NodeLinkFigure(pyHConnectionFigure):
    """
    Figura empleada para conectar unos nodos con otros.
    """

    def __init__(self):
        pyHConnectionFigure.__init__(self)
        self._forward_info_figure = pyHTextFigure(0,0,0,0,"")
        self._backward_info_figure = pyHTextFigure(0,0,0,0,"")

        self.set_default_style()


    @staticmethod
    def _create_button_figure():
        from pyHEllipseFigure import pyHEllipseFigure
        button_figure = pyHEllipseFigure(0, 0, 50, 30)
        return button_figure


    def set_default_style(self):
        self.setColor(pyHAttributeColor(150, 150, 150, 255))
        self.setAttribute('WIDTH', pyHAttributeWidth(2))

        self._forward_info_figure.setColor(COLOR.get('BLUE'))
        self._forward_info_figure.setAttribute('FONT', pyHAttributeFontSize(12))

        self._backward_info_figure.setColor(COLOR.get('RED'))
        self._backward_info_figure.setAttribute('FONT', pyHAttributeFontSize(12))

    @staticmethod
    def _set_forward_color_style(figure):
        figure.setAttribute('COLOR', pyHAttributeColor(0, 76, 153))
        figure.setAttribute('FILL',  pyHAttributeFillColor(51, 153, 255))
        figure.setAttribute('WIDTH', pyHAttributeWidth(2))
        return figure


    @staticmethod
    def _set_backward_color_style(figure):
        figure.setAttribute('COLOR', pyHAttributeColor(168, 0, 0))
        figure.setAttribute('FILL',  pyHAttributeFillColor(204, 51, 51))
        figure.setAttribute('WIDTH', pyHAttributeWidth(2))
        return figure



    def set_start_socket(self, socket_figure):
        """
        Añade el nexo inicial de la figura conector, a partir del
        Socket de un nodo.

        Add the start connector of the link figure, from a node Socket.
        :param socket_figure: Socket de un nodo / node figure's Socket.
        """
        start_connector = socket_figure.get_central_connector()
        pyHConnectionFigure.setConnectorStart(self, start_connector)
        self._add_initial_points()


    def set_end_socket(self, socket_figure):
        end_connector = socket_figure.get_central_connector()
        pyHConnectionFigure.setConnectorEnd(self, end_connector)
        self._set_zigzag_form()

        start_socket = self.getConnectorStart().getOwner()
        end_socket = self.getConnectorEnd().getOwner()
        start_socket.addChangedFigureObserver(self)
        end_socket.addChangedFigureObserver(self)

        start_socket.add_link(self)
        end_socket.add_link(self)

    def figureChanged(self, figure):
        pyHConnectionFigure.figureChanged(self, figure)
        self._set_zigzag_form()
        self._print_forward_and_backward_values()
    """
    @staticmethod
    def _is_scalar(value):
        if isinstance(value, np.matrix):
            return value.size == 1
        return ops.is_float(value)

    @staticmethod
    def _to_scalar(value):
        if isinstance(value, np.matrix):
            return float(value.A[0][0])
        return float(value)
    """
    def _print_forward_and_backward_values(self):
        """
        Dibuja el valor de las operaciones forward y backward en la conexión
        si el nodo lo permite, y el valor no es una matriz.
        :return:
        """
        start_node = self.get_start_node()
        if start_node.get_node():
            if start_node.isForwardPrintable():
                forward_value = start_node.get_node().getValue()
                if is_float(forward_value):
                    value = format_number(forward_value)
                    self._forward_info_figure.setText(value)
                else:
                    self._forward_info_figure.setText('')

            if start_node.isBackwardPrintable():
                backward_value = start_node.get_node().partialGlobal
                if is_float(backward_value):
                    value = format_number(backward_value)
                    self._backward_info_figure.setText(value)
                else:
                    self._backward_info_figure.setText('')



    def setConnectorStart(self, connector):
        raise NotImplementedError('Usar setStartSocker(socket). Me da pereza'
                                  'implementar este')

    def setConnectorEnd(self, connector):
        raise NotImplementedError('Usar setEndSocker(socket). Me da pereza'
                                  'implementar este')

    def _add_initial_points(self):
        """
        Inicializa los puntos que forman el conector. Añade 2 puntos.
        El primero representa el comienzo del nodo.
        El segundo, igual al primero, es empleado para poder representar
        el connector.
        :return:
        """
        start_connector = self.getConnectorStart()
        p0 = start_connector.locate()
        p1 = start_connector.locate()
        self.points = [p0, p1]


    def get_start_node(self):
        return self.getConnectorStart().getOwner().get_owner_node()


    def get_end_node(self):
        return self.getConnectorEnd().getOwner().get_owner_node()


    def get_start_socket(self):
        return self.getConnectorStart().getOwner()


    def get_end_socket(self):
        return self.getConnectorEnd().getOwner()


    def removeLastPoint(self):
        self.points = self.points[:-1]


    def draw(self, g):
        pyHConnectionFigure.draw(self, g)
        self._print_arrow(g)
        self._printValues(g)


    def getColor(self):
        return self.getAttribute('COLOR')


    def getFillColor(self):
        return

    def setFillColor(self, *args):
        pass



    def containPoint(self, point):
        if not self.points: return False
        p0=self.points[0]
        for p1 in self.points[1:]:
            c1 = min(p0.x, p1.x) <= point.x <= max(p0.x, p1.x) or p0.x == p1.x
            c2 = min(p0.y, p1.y) <= point.y <= max(p0.y, p1.y) or p0.y == p1.y
            if c1 and c2:
                m, n = ops.crear_recta_a_partir_de_2_puntos(p0, p1)
                distance =  ops.distancia_punto_recta(m, n, point)
                if distance <= 30:
                    return True
            p0= p1
        return False

    def _printValues(self, g):
        start_point = self.getConnectorStart().locate()
        n = self.get_start_node()
        if n.isForwardPrintable():
            self._forward_info_figure.x0 = start_point.x + 20
            self._forward_info_figure.y0 = start_point.y + 10
            self._forward_info_figure.draw(g)
        if n.isBackwardPrintable():
            self._backward_info_figure.x0 = start_point.x + 20
            self._backward_info_figure.y0 = start_point.y - 30
            self._backward_info_figure.draw(g)

    @staticmethod
    def _printArrow(g, x1, x2, y1, y2):
        alpha = math.atan2(y2 - y1, x2 - x1)
        k = 30
        xa = x2 - k * math.cos(alpha + 0.35)
        ya = y2 - k * math.sin(alpha + 0.35)
        g.drawLine(xa, ya, x2, y2)
        xa = x2 - k * math.cos(alpha - 0.35)
        ya = y2 - k * math.sin(alpha - 0.35)
        g.drawLine(xa, ya, x2, y2)


    def _print_arrow(self, g, line_length=30):
        first_point = self.points[-2]
        end_point   = self.points[-1]
        angle_between_points = math.atan2(end_point.y - first_point.y,
                           end_point.x - first_point.x)

        x = end_point.x - line_length * math.cos(angle_between_points + 0.35)
        y = end_point.y - line_length * math.sin(angle_between_points + 0.35)
        g.drawLine(x, y, end_point.x, end_point.y)

        x = end_point.x - line_length * math.cos(angle_between_points - 0.35)
        y = end_point.y - line_length * math.sin(angle_between_points - 0.35)
        g.drawLine(x, y, end_point.x, end_point.y)


    def _set_zigzag_form(self):
        """
        Dota al conector de una figura de zigzag.
        :return:
        """
        start_point = self.getConnectorStart().locate()
        end_point = self.getConnectorEnd().locate()
        new_point_0 = pyHPoint(start_point.getX() + 100,
                          start_point.getY())
        new_point_1 = pyHPoint(end_point.getX() - 50,
                          end_point.getY())
        
        self.points = [start_point, new_point_0,
                       new_point_1, end_point]

