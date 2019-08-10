#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy

from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure

from MiniTensorFlow.figures.pyHFindConnectorDecorator import pyHFindConnectorDecorator
from pyHotDraw.Core.Exceptions import pyHFigureNotFound
from pyHotDraw.Figures.pyHAttributes import *
from pyHotDraw.Geom.pyHPoint import pyHPoint
from MiniTensorFlow.Tools.AbstractTool import AbstractTool

EMPHASIS_FACTOR = 1.40

class NodesLinkCreatorTool(AbstractTool):
    """
    classdocs
    """
    def __init__(self,v,figureToCreate):
        """
        Constructor
        """
        AbstractTool.__init__(self, v)
        self.prototype = figureToCreate
        self.figureClicked = False
        self.created_link = None
        self.conexion_socket = None
        self.getView().clearSelectedFigures()
        self.state = self.view.actual_state()


    def onMouseDown(self,e):
        if e.isLeftClick():
            self.figureClicked = False
            click_point = pyHPoint(e.getX(), e.getY())

            start_socket = self._search_output_socket_on_point(click_point)
            if start_socket and start_socket.is_free():
                self.figureClicked = True
                self.created_link = copy.deepcopy(self.prototype)
                self.created_link.set_start_socket(start_socket)
                self._add_figure_to_drawing(self.created_link)

    def onMouseUp(self, e):
        click_point = pyHPoint(e.getX(), e.getY())
        input_socket = self._search_input_socket_on_point(click_point)
        if input_socket and input_socket.is_free():
            if not self._same_owner_as_link_start(input_socket):
                self.created_link.set_end_socket(input_socket)
                self.figureClicked = False
                self.created_link = None
                self.view.save_state(self.state)
                self._deemphasize_socket(EMPHASIS_FACTOR)
                self.state = self.view.actual_state()
            else:
                self._onMouseUpError()
        else:
            self._onMouseUpError()

    def onMouseMove(self,e):
        click_point = pyHPoint(e.getX(), e.getY())

        found_socket = self._find_socket_to_emphasize(click_point)
        if found_socket and not self.conexion_socket:
            self._emphasize_socket(found_socket, EMPHASIS_FACTOR)
        elif not found_socket and self.conexion_socket:
            self._deemphasize_socket(EMPHASIS_FACTOR)

        if self.created_link:
            self._update_link(click_point)

    def onMouseGrab(self,e):
        pass

    def onMouseDobleClick(self,e):
        pass

    def onMouseWheel(self,e):
        pass

    def onKeyPressed(self,e):
        pass

    def _update_link(self, point):
        """
        Actualiza el último punto del conector a la posición del ratón
        :param point: posición actual del ratón
        :return:
        """
        if self.created_link.getLenght() > 0:
            last_point_of_link = self.created_link.getLastPoint()
            last_point_of_link.setX(point.getX())
            last_point_of_link.setY(point.getY())



    def _add_figure_to_drawing(self, figure):
        """
        Añade una figura al dibujo.
        :param figure: figura a añdir al dibujo
        :return:
        """
        self.view.getDrawing().addFigure(figure)

    def _remove_figure_to_drawing(self, figure):
        """
        Elimina una figura del dibujo.
        :return: elimina una figura del dibujo
        """
        self.view.getDrawing().removeFigure(figure)

    def _onMouseUpError(self, errorText = 'On mouse up error'):
        self._remove_figure_to_drawing(self.created_link)
        self.created_link = None
        self.figureClicked = False
        self.getView().update()
        print(errorText)


    def _search_input_socket_on_point(self, point):
        """
        Busca la existencia de un socket entrada de una figura nodo dado un
        punto. Si existe un socket en ese punto, la función devuelve el socket
        encontrando. En caso de no encontrar ninguno, devuelve None.
        :param point: punto (x, y)
        :return: socket encontrado; en caso contrario 'None'.
        """
        node = self._find_node_on_this_point(point)
        if node:
            for socket in node.get_inputs_sockets():
                if socket.containPoint(point):
                    return socket

    def _search_output_socket_on_point(self, point):
        """
        Busca la existencia de un socket salida de una figura nodo dado un
        punto. Si existe un socket en ese punto, la función devuelve el socket
        encontrando. En caso de no encontrar ninguno, devuelve None.
        :param point: punto (x, y)
        :return: socket encontrado; en caso contrario 'None'.
        """
        node = self._find_node_on_this_point(point)
        if node:
            for socket in node.get_outputs_sockets():
                if socket.containPoint(point):
                    return socket

    def _find_node_on_this_point(self, point):
        figures_in_drawing = self.getView().getDrawing().getFigures()
        for figure in figures_in_drawing:
            if isinstance(figure, NodeFigure) \
                    and figure.containPoint(point):
                return figure


    def _same_owner_as_link_start(self, end_socket):
        """
        Comprueba si el socket del comienzo del conector y el futuro socket
        final pertenecen a la misma figura nodo.
        :param end_socket:
        :return:
        """
        if self.created_link.get_start_node() == end_socket.get_owner_node():
            print('Same Figure')
            return True



    def _find_socket_to_emphasize(self, point):
        """
        Comprueba si el ratón se encuentra sobre una figura que representa un
        punto de unión (Socket, ya sea de comienzo o final).
        Si existe una figura conector, buscará puntos de entrada a los nodos,
        evitando los del mismo nodo origen y aquellos que no estén libres.
        Si no existe una figura conector, resaltará los puntos sobre los cuales
        es posible empezar un conector.
        Cada vez que el puntero se encuentra sobre uno de estos puntos de unión
        los resalta, haciéndolos más visibles, facilitando su detección, su
        disponibilidad, y la realización exitosa de un conector.

        :param point: punto donde se pulsó el ratón
        :return:
        """

        if self.created_link:
            return self._find_input_socket_to_emphasize(point)
        else:
            return self._find_output_socket_to_emphasize(point)


    def _find_output_socket_to_emphasize(self, mouse_point):
        return self._search_output_socket_on_point(mouse_point)


    def _find_input_socket_to_emphasize(self, mouse_point):
        found_input_socket = self._search_input_socket_on_point(mouse_point)
        if found_input_socket and found_input_socket.is_free():
            if not self._same_owner_as_link_start(found_input_socket):
                return found_input_socket



    def _emphasize_socket(self, socket, size):
        self.conexion_socket = socket
        w = self.conexion_socket.w
        h = self.conexion_socket.h
        w_new = w * size
        h_new = h * size
        self.conexion_socket.w = w_new
        self.conexion_socket.h = h_new
        self.conexion_socket.move(-(w_new - w) / 2, -(h_new - h) / 2)
        self.conexion_socket.setAttribute('WIDTH', pyHAttributeWidth(3))

    def _deemphasize_socket(self, size):
        w = self.conexion_socket.w
        h = self.conexion_socket.h
        w_new = w / size
        h_new = h / size
        self.conexion_socket.w = w_new
        self.conexion_socket.h = h_new
        self.conexion_socket.move((w - w_new) / 2, (h - h_new) / 2)
        self.conexion_socket.setAttribute('WIDTH', pyHAttributeWidth(2))
        self.conexion_socket = None

