#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyHotDraw.Figures.pyHDecoratorFigure import pyHDecoratorFigure


class pyHFindConnectorDecorator(pyHDecoratorFigure):
    """ Clase para realizar operaciones sobre sus figuras de
        conexion de conectores de los nodos complejos.
    """


    def __init__(self, node):
        pyHDecoratorFigure.__init__(self, node)

    def isNode(self):
        from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure
        return isinstance(self.getDecoratedFigure(), NodeFigure)
    # inputs
    def findInputConnectorFree(self, p):
        ir = self.findInputSocket(p)
        if not ir or not ir.is_free(): return
        return self.getInputConnector(ir)

    def findInputSocket(self, p):
        """
        Comprueba si el ratón se encuentra sobre una de las
        figuras que representan un punto de entrada al nodo. Si
        existe lo devuelve.
        :param p:
        :return:
        """
        for f in self.getDecoratedFigure().get_inputs_sockets():
            if f.containPoint(p):
                return f

    def getInputSocket(self, connector):
        """
        :param connector: Punto de conexión (no figura pyHNodeConnector)
        :return:
        """
        node_sockets = self.getDecoratedFigure().get_inputs_sockets()
        return self._findSocket(connector, node_sockets)

    def getInputConnector(self, socket):
        node_connectors = self.getDecoratedFigure().getLeftConnectors()
        return self._findConnector(socket, node_connectors)


    # outputs
    def findOutputConnectorFree(self, p):
        outr = self.findOutputSocket(p)
        if not outr or not outr.is_free(): return
        return self.getOutputConnector(outr)

    def findOutputSocket(self, p):
        return self.findRepresentationOutput(p)

    def getOutputSocket(self, connector):
        node_sockets = self.getDecoratedFigure().get_outputs_sockets()
        return self._findSocket(connector, node_sockets)

    def getOutputConnector(self, socket):
        node_connectors = self.getDecoratedFigure().getRightConnectors()
        return self._findConnector(socket, node_connectors)


    def _findConnector(self, figure, connectors_list):
        for connector in connectors_list:
            p_aux = connector.locate(self.getDecoratedFigure())
            if p_aux.getX() == figure.x0 and p_aux.getY() == figure.y0:
                return connector

    def _findSocket(self, connector, socket_list):
        for socket in socket_list:
            p_aux = connector.locate(self.getDecoratedFigure())
            if p_aux.getX() == socket.x0 and p_aux.getY() == socket.y0:
                return socket


    def findRepresentationInput(self, p):
        """
        Comprueba si el ratón se encuentra sobre una de las
        figuras que representan un punto de entrada al nodo. Si
        existe lo devuelve.
        :param p:
        :return:
        """

        for f in self.getDecoratedFigure().get_inputs_sockets():
            if f.containPoint(p):
                return f

    def findRepresentationOutput(self, p):
        """
        Comprueba si el ratón se encuentra sobre una de las
        figuras que representan un punto de salida del nodo. Si
        existe lo devuelve.
        :param p:
        :return:
        """
        for f in self.getDecoratedFigure().get_outputs_sockets():
            if f.containPoint(p):
                return f



    # ---------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------

    def findInputConnector(self, p):
        """

        :param p:
        :return:
        """
        figure_input = self.findRepresentationInput(p)
        if not figure_input: return
        node_connectors = self.getDecoratedFigure().getLeftConnectors()
        return self._findConnector(figure_input, node_connectors)

    def findOutputConnector(self, p):
        """

        :param p:
        :return:
        """

        circle = self.findRepresentationOutput(p)
        if not circle: return
        figure_connectors = self.getDecoratedFigure().getRightConnectors()
        return self._findConnector(circle, figure_connectors)








    def isInputConnectorFree(self, connector):
        """
        Comprueba si existe una figura conector que acabe en el conector
        pasado como parámetro.
        :param connector:
        :return:
        """

        for c in self.getDecoratedFigure().get_inputs_links():
            ce = c.getConnectorEnd()
            connector_point = connector.locate(self.getDecoratedFigure())
            ce_point = ce.locate(self.getDecoratedFigure())
            if connector_point == ce_point:
                return False
        return True


    # necesario?
    def isOutputConnectorFree(self, connector):
        """
        Comprueba si existe una figura conector que empiece desde
        el conector pasado como parámetro.
        :param connector:
        :return:
        """
        for c in self.getDecoratedFigure().get_outputs_links():
            cs = c.getConnectorStart()
            connector_point = connector.locate(self.getDecoratedFigure())
            cs_point = cs.locate(self.getDecoratedFigure())
            if connector_point == cs_point:
                return False
        return True




