#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyHotDraw.Figures.pyHRectangleRoundedFigure import pyHRectangleRoundedFigure, pyHRectangle
from pyHotDraw.Connectors.pyHLocatorConnector import pyHLocatorConnector


# Habria que editarlo porque hay inputs y ouputs, pero solo hay metodos de
# genéricos, es decir, add_link, cuando deberían de existir 'add_input_link' y
# add_output_link


class Socket(pyHRectangleRoundedFigure):
    def __init__(self,
                 owner,
                 max_inputs_links= -1,
                 max_outputs_links= -1):
        """
        Figura (con forma de Rectángulo redondeado) que representa visualemnte
        un conector/nexo(connector) de una figura nodo.

        Un socket actúa como una representación visual de los puntos donde se
        puede crear (o terminar) una conexión(Link) entr nodos. Estos puntos en
        pyHotDraw se conocen como connectores.
        El socket es dibujado sobre un nexo(connector) del nodo, estando este
        nexo en el centro de la figura.

        El propio nexo del nodo no es posible añadirlo como un parámentro debido
        a que se invoca en el momento de necesitarlo, es decir, no se
        almacena en memoria

        :param owner: Figura nodo sobre la cual se precisa dibujar sus sockets.
                     (instancia de ComplexNode)
        :param max_inputs_links: Número máximo de conectores que pueden acabar
                                en este socket.
                                Por defecto: infinitos (-1)
        :param max_outputs_links: Número máximo de conectores que pueden
                                comenzar en este socket.
                                Por defecto: infinitos (-1)
        """
        pyHRectangleRoundedFigure.__init__(self, 0, 0, 30, 30)
        self._OWNER = owner
        self._MAX_INPUTS_LINKS = int(max_inputs_links)
        self._MAX_OUTPUTS_LINKS = int(max_outputs_links)
        self._links = set()
        self._show = True

    def get_owner_node(self):
        return self._OWNER

    def add_link(self, link):
        """
        Añade un link (connection).
        :param link:
        :return: Existo de la operacion
        """
        if self.is_free():
            self._links.add(link)
            return True
        return False

    def remove_link(self, link):
        if link in self._links:
            self._links.remove(link)

    def get_link(self):
        return list(self._links)

    def is_free(self):
        # me da pereza implementarlo.
        return True

    def max_acceptables_inputs_links(self):
        return self._MAX_INPUTS_LINKS

    def max_acceptables_outputs_links(self):
        return self._MAX_OUTPUTS_LINKS

    def is_visible(self):
        return self._show

    def setPrintable(self, boolean):
        self._show = bool(boolean)

    def set_socket_position(self, connector):
        """
        Reposiciona el Socket. Esto es empleado dado que el Socket depende
        de la posicion de un nexo del nodo, es decir, una posición relativa
        a la figura nodo. Como la posición del nexo puede variar en función del
        tamaño de la figura, puede ser necesario reposicionar el ssocket.

        self.x0 = (point.getX() - (self.w / 2))
        self.y0 = (point.getY() - (self.h / 2))

        :param connector: conector sobre el cual hace el Socket de representación visual
        :return:
        """
        point = connector.locate()
        new_x = (point.getX() - (self.w / 2))
        new_y = (point.getY() - (self.h / 2))

        move_on_x = new_x - self.x0
        move_on_y = new_y - self.y0
        self.move(move_on_x, move_on_y)

    def draw(self, g):
        if self._show:
            pyHRectangleRoundedFigure.draw(self, g)

    def getConnectors(self):
        return pyHLocatorConnector.ToolBoxCenterLineFigureConnector(self)

    def get_central_connector(self):
        """
        Devuelve el nexo/conector (connector) localizado en el centro de la
        figura. Este conector coincide con el conector del nodo. (Los sockets
        representan, mediante una figura, un connector de su dueño)
        OJO: El punto del conector devuelto coincide con el del nodo, pero NO
        son el mismo. Es decir, el dueño del conector devuelto por este método
        es el socket, NO el nodo.
        :return:
        """
        return self.getConnectors()[1]

