#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.figures.Socket.SocketList import SocketList
from MiniTensorFlow.figures.Socket.StartLinkSocket import StartLinkSocket
from MiniTensorFlow.figures.Socket.EndLinkSocket import EndLinkSocket
from MiniTensorFlow.figures.pyHFindConnectorDecorator import pyHFindConnectorDecorator
from MiniTensorFlow.figures.MathTextFigure import MathTextFigure
from MiniTensorFlow.handles.pyHBackwardHandle import pyHBackwardHandle
from MiniTensorFlow.handles.pyHForwardHandle import pyHForwardHandle
from pyHotDraw.Connectors.pyHLocatorConnector import pyHLocatorConnector
from pyHotDraw.Figures.pyHAttributes import *
from pyHotDraw.Figures.pyHCompositeFigure import pyHCompositeFigure
from pyHotDraw.Figures.pyHEllipseFigure import pyHEllipseFigure
from pyHotDraw.Geom.pyHPoint import pyHPoint
from pyHotDraw.Handles.pyHNullHandle import pyHNullHandle
from format_values import is_matrix

class NodeFigure(pyHCompositeFigure):
    def __init__(self, x, y, w, h, num_inputs,
                 operation='op', func_letter='f'):
        pyHCompositeFigure.__init__(self)
        self._create_node_figure(x, y, w, h)

        self.node = None
        self.function_letter = func_letter
        self.operation = operation
        self.MAX_INPUTS_NODES = num_inputs
        self.inputs_sockets = self._create_inputs_sockets()
        self.outputs_sockets = self._create_start_sockets()

        self._isForwardValuePrintable = False
        self._isBackwardValuePrintable = False

        self.set_text(self.get_operation())

    def create_node(self):
        """
        Metodo encargado de crear el nodo/gate que representa la figura.
        :return:
        """
        raise NotImplementedError

    def get_expression(self, *values):
        """
        Devuelve la expresión matemática, en formato de cadena, que representa
        la figura, haciendo uso de las variables pasadas como argumentos.
        Por ejemplo, en un nodo suma (que necesita dos entradas para ser evaluado):
            >> sumNode.getExpression(a, b)
               'a + b'
        :param values: strings que representan cada una de las variables necesarias
                       para realizar la operación que representa el nodo.
        :return: string
        """
        raise NotImplementedError


    def get_partial_expressions(self):
        raise NotImplementedError


    def invert_dot_to_calculate_partial(self):
        return {p: False for p in self.get_inputs_nodes()}

    def get_partials(self):
        f = self.get_node()
        return {i: f.getPartialLocal(i.get_node())
                for i in self.get_inputs_nodes()}

    def get_figure_expression(self, *values):
        expression = self.function_letter + ' \/ = \/ ' + self.get_expression(*values)
        use_latex = any(is_matrix(v) for v in values)
        return MathTextFigure(0, 0, expression, use_latex=use_latex)

    def get_value(self):
        return self.node.getValue()

    def get_partial_global(self):
        return self.node.get_partial_value()

    def forward(self):
        self.node.forward()

    def backward(self):
        self.node.backward()

    def get_operation(self):
        return self.operation


    def _create_node_figure(self, x, y, w, h):
        f = pyHEllipseFigure(x, y, w, h)
        f.setAttribute('FILL', pyHAttributeFillColor(187, 198, 221, 255))  # blue
        f.setAttribute('WIDTH', pyHAttributeWidth(3))
        f.setColor(pyHAttributeColor(127, 135, 151, 255))  # dark blue

        f_text = MathTextFigure(x, y)
        f_text.setColor(pyHAttributeColor(255, 0, 0, 0))
        f_text.setFillColor(0, 0, 0, 0)

        self.addFigure(f)
        self.addFigure(f_text)

    def set_node(self, n):
        self.node = n
        self.notifyFigureChanged()

    def get_node(self):
        """
        Devuelve el nodo representado por la figura.
        :return:
        """
        return self.node

    def is_input(self):
        return self.MAX_INPUTS_NODES == 0


    def get_inputs_sockets(self):
        return self.inputs_sockets.sockets()

    def get_outputs_sockets(self):
        return self.outputs_sockets.sockets()

    def show_sockets(self, b):
        show = bool(b)
        socket_list = self.get_inputs_sockets() + self.get_outputs_sockets()
        for socket in socket_list:
            socket.setPrintable(show)

    def _create_inputs_sockets(self):
        """
        Crea los sockets que actuarán como entradas al nodo.
        """
        socket_list = SocketList()
        for connector in self.getLeftConnectors():
            input_socket = EndLinkSocket(self)
            input_socket.set_socket_position(connector)
            self.paint_socket(input_socket)
            socket_list.addFigure(input_socket)
        self.addFigure(socket_list)
        return socket_list

    def _create_start_sockets(self):
        """
        Crea los sockets que actuarán como punto de creación de un
        link, es decir, de salida del nodo.
        """
        socket_list = SocketList()
        for connector in self.getRightConnectors():
            output_socket = StartLinkSocket(self)
            output_socket.set_socket_position(connector)
            self.paint_socket(output_socket)
            socket_list.addFigure(output_socket)
        self.addFigure(socket_list)
        return socket_list



    def paint_socket(self, figure):
        fill = self.figures[0].getAttribute('FILL')
        color = self.figures[0].getAttribute('COLOR')
        figure.setAttribute('WIDTH', pyHAttributeWidth(2))
        figure.setAttribute('COLOR', color)
        figure.setAttribute('FILL', fill)


    # OVERRIDES BASIC NODE METHODS
    def are_all_inputs_occupied(self):
        """
        Conprueba si todas las entradas del nodo tienen asociado un nodo.
        En el caso de que alguna entrada esté sin conectar, devuelve falso.
        :return:
        """
        for s in self.get_inputs_sockets():
            if s.is_free():
                return False
        return True

    def get_inputs_links(self):
        links= []
        for socket in self.get_inputs_sockets():
            links += [l for l in socket.get_link()]
        return links

    def get_outputs_links(self):
        links = []
        for socket in self.get_outputs_sockets():
            links += [c for c in socket.get_link()]
        return links

    def get_inputs_nodes(self):
        """
        Devuelve una lista con los nodos (figuras) entrada
        :return:
        """
        l = []
        for s in self.get_inputs_sockets():
            l += [c.get_start_node() for c in s.get_link()]
        return l

    def get_outputs_nodes(self):
        """
        Devuelve una lista con los nodos (figuras) salida
        :return:
        """
        l = []
        for s in self.get_outputs_sockets():
            l += [c.get_end_node() for c in s.get_link()]
        return l

    def remove_input_link(self, connector_fig):
        decorator = pyHFindConnectorDecorator(self)
        s = decorator.findInputSocket(connector_fig.getLastPoint())
        s.remove_link(connector_fig)

    def remove_output_link(self, connector_fig):
        decorator = pyHFindConnectorDecorator(self)
        s = decorator.findOutputSocket(connector_fig.getPoints()[0])
        s.remove_link(connector_fig)


    def getLeftConnectors(self):
        connectorList = self.getConnectors()
        if self.MAX_INPUTS_NODES == 1: return [connectorList[8]]
        elif self.MAX_INPUTS_NODES == 2: return [connectorList[7], connectorList[9]]
        return []

    def getRightConnectors(self):
        connector_list = self.getConnectors()
        return [connector_list[0]]

    def set_text(self, text, font_size=25):
        text_figure = self.getFigures()[1]
        text_figure.set_math_text(text, font_size)

    def get_text(self):
        return self.getFigures()[1].get_text()

    def setWidth(self, w):
        circle = self.getFigures()[0]
        circle.w = w
        text = self.getFigures()[1]
        text.x0 += (w / 2) - 7.5
        self.notifyFigureChanged()

    def setHeight(self, h):
        circle = self.getFigures()[0]
        circle.h = h
        text = self.getFigures()[1]
        text.y0 += (h / 2) - 5
        self.notifyFigureChanged()

    def setFillColor(self, r, g, b, a=255):
        self.figures[0].setAttribute('FILL', pyHAttributeFillColor(r, g, b, a))

    def getFillColor(self):
        c = self.figures[0].getAttribute('FILL')
        return (c.r, c.g, c.b, c.a) if c else None

    def getColor(self):
        return self.figures[0].getAttribute('COLOR')

    def isForwardPrintable(self):
        return self._isForwardValuePrintable

    def setForwardPrintable(self, b):
        self._isForwardValuePrintable = bool(b)
        self.notifyFigureChanged()

    def isBackwardPrintable(self):
        return self._isBackwardValuePrintable

    def setBackwardPrintable(self, b):
        self._isBackwardValuePrintable = bool(b)
        self.notifyFigureChanged()

    def assign_function_letter(self, l):
        self.function_letter = str(l)

    def get_function_letter(self):
        return self.function_letter

    # OVERRIDE FIGURE METHODS
    def getConnectors(self):
        return pyHLocatorConnector.ToolBoxCircleConnectors(self, n=16)

    def containPoint(self, p):
        figures = self.get_inputs_sockets() + self.get_outputs_sockets() + self.getFigures()
        for f in figures:
            if f.containPoint(p):
                return True
        return False

    def getDisplayBox(self):
        return self.getFigures()[0].getDisplayBox()

    #remove...
    def draw(self, g):
        self.inputs_sockets.setPositions(self.getLeftConnectors())
        self.outputs_sockets.setPositions(self.getRightConnectors())

        circle_figure = self.getFigures()[0]
        text_figure = self.getFigures()[1]

        if text_figure.w >= circle_figure.w:
            circle_figure.w = text_figure.w + 10

        text_figure.x0 = circle_figure.x0 + ((circle_figure.w - text_figure.w) / 2)
        text_figure.y0 = circle_figure.y0 + ((circle_figure.h - text_figure.h) / 2)

        circle_figure.draw(g)
        text_figure.draw(g)

        self.notifyFigureChanged()

        for f in self.getFigures()[2:]:
            f.draw(g)

        # show connectors
        """
        lc = pyHLocatorConnector.ToolBoxCircleConnectors(self, n=16)
        for l in lc:
            p = l.locate(self)
            r= pyHRectangleFigure(p.getX(), p.getY(), 5, 5)
            r.draw(g)
        """


    def getHandles(self):
        r = self.getDisplayBox()
        x = r.getX()
        y = r.getY()
        w = r.getWidth()
        h = r.getHeight()

        h0 = pyHNullHandle(self, pyHPoint(x + w, y - 20))
        h1 = pyHNullHandle(self, pyHPoint(x + w, y + h))
        h2 = pyHNullHandle(self, pyHPoint(x-20, y - 20))
        h3 = pyHNullHandle(self, pyHPoint(x-20, y + h))

        return [h0, h1, h2, h3]



    def add_input_on_socket(self, link, socket):
        if socket in self.get_inputs_sockets():
            socket.add_link(link)


    def add_ouput_on_socket(self, link, socket):
        if socket in self.get_outputs_sockets():
            socket.add_link(link)



    def addChangedFigureObserver(self, fo):
        for f in self.getFigures():
            f.addChangedFigureObserver(fo)

    def notifyFigureChanged(self):
        for f in self.getFigures():
            f.notifyFigureChanged()

    def setColor(self, c):
        self.figures[0].setColor(c)
        color = c.values()
        self.figures[1].setTextColor(*color)

    def setAttribute(self,k,v):
        self.getFigures()[0].setAttribute(k, v)

    def getAttribute(self, k):
        return self.getFigures()[0].getAttribute(k)

    def _get_representation_figure(self):
        return self.getFigures()[0]

    def _get_text_figure(self):
        return self.getFigures()[1]



    def getX(self):
        return self.figures[0].x0

    def getY(self):
        return self.figures[0].y0

    def getWidth(self):
        return self.figures[0].w

    def getHeight(self):
        return self.figures[0].h

    def dimmensions(self):
        f = self.figures[0]
        return f.x0, f.y0, f.w, f.h

    def __repr__(self):
        return 'Nodo {}'.format(self.operation)
