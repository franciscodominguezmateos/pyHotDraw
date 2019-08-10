
from figures.Nodes.NodeFigure import NodeFigure
from pyHotDraw.Figures.pyHDecoratorFigure import pyHDecoratorFigure


class DecoratedNode(pyHDecoratorFigure):


    def getHandles(self):
        return self.getDecoratedFigure().getHandles()

    def draw(self, g):
        self.getDecoratedFigure().draw(g)

    def get_node(self):
        return self.getDecoratedFigure().get_node()

    def set_node(self, n):
        self.getDecoratedFigure().set_node(n)

    def get_function_letter(self):
        return self.getDecoratedFigure().get_function_letter()

    def get_inputs_links(self):
        return self.getDecoratedFigure().get_inputs_links()

    def remove_output_link(self, connector_fig):
        self.getDecoratedFigure().remove_output_link(connector_fig)

    def getColor(self):
        return self.getDecoratedFigure().getColor()

    def set_text(self, text, font_size=25):
        self.getDecoratedFigure().set_text(text, font_size)

    def setHeight(self, h):
        self.getDecoratedFigure().setHeight(h)

    def forward(self):
        self.getDecoratedFigure().forward()

    def get_expression(self, *values):
        pass

    def addChangedFigureObserver(self, fo):
        self.getDecoratedFigure().addChangedFigureObserver(fo)

    def getY(self):
        return self.getDecoratedFigure().getY()

    def create_node(self):
        pass

    def get_partial_expressions(self):
        pass

    def getConnectors(self):
        return self.getDecoratedFigure().getConnectors()

    def setAttribute(self, k, v):
        self.getDecoratedFigure().setAttribute(k, v)

    def getAttribute(self, k):
        return self.getDecoratedFigure().getAttribute(k)

    def isBackwardPrintable(self):
        return self.getDecoratedFigure().isBackwardPrintable()

    def remove_input_link(self, connector_fig):
        self.getDecoratedFigure().remove_input_link(connector_fig)

    def are_all_inputs_occupied(self):
        return self.getDecoratedFigure().are_all_inputs_occupied()

    def get_outputs_nodes(self):
        return self.getDecoratedFigure().get_outputs_nodes()

    def get_value(self):
        return self.getDecoratedFigure().get_value()

    def getHeight(self):
        return self.getDecoratedFigure().getHeight()

    def get_text(self):
        return self.getDecoratedFigure().get_text()

    def isForwardPrintable(self):
        return self.getDecoratedFigure().isForwardPrintable()

    def setFillColor(self, r, g, b, a=255):
        self.getDecoratedFigure().setFillColor(r, g, b, a)

    def get_inputs_sockets(self):
        return self.getDecoratedFigure().get_inputs_sockets()

    def backward(self):
        self.getDecoratedFigure().backward()

    def get_partials(self):
        return self.getDecoratedFigure().get_partials()

    def add_ouput_on_socket(self, link, socket):
        self.getDecoratedFigure().add_ouput_on_socket(link, socket)

    def setColor(self, c):
        self.getDecoratedFigure().setColor(c)

    def get_outputs_sockets(self):
        return self.getDecoratedFigure().get_outputs_sockets()


    def dimmensions(self):
        return self.getDecoratedFigure().dimmensions()

    def assign_function_letter(self, l):
        self.getDecoratedFigure().assign_function_letter(l)

    def notifyFigureChanged(self):
        self.getDecoratedFigure().notifyFigureChanged()

    def getX(self):
        return self.getDecoratedFigure().getX()

    def getLeftConnectors(self):
        return self.getDecoratedFigure().getLeftConnectors()

    def is_input(self):
        return self.getDecoratedFigure().is_input()

    def getDisplayBox(self):
        return self.getDecoratedFigure().getDisplayBox()

    def getWidth(self):
        return self.getDecoratedFigure().getWidth()


    def getRightConnectors(self):
        return self.getDecoratedFigure().getRightConnectors()

    def get_outputs_links(self):
        return self.getDecoratedFigure().get_outputs_links()


    def invert_dot_to_calculate_partial(self):
        return self.getDecoratedFigure().invert_dot_to_calculate_partial()

    def setForwardPrintable(self, b):
        self.getDecoratedFigure().setForwardPrintable(b)

    def getFillColor(self):
        return self.getDecoratedFigure().getFillColor()

    def get_figure_expression(self, *values):
        return self.getDecoratedFigure().get_figure_expression(*values)

    def get_partial_global(self):
        return self.getDecoratedFigure().get_partial_global()

    def setWidth(self, w):
        self.getDecoratedFigure().setWidth(w)

    def get_inputs_nodes(self):
        return self.getDecoratedFigure().get_inputs_nodes()

    def paint_socket(self, figure):
        self.getDecoratedFigure().paint_socket(figure)

    def get_operation(self):
        return self.getDecoratedFigure().get_operation()

    def show_sockets(self, b):
        self.getDecoratedFigure().show_sockets(b)

    def add_input_on_socket(self, link, socket):
        self.getDecoratedFigure().add_input_on_socket(link, socket)

    def containPoint(self, p):
        return self.getDecoratedFigure().containPoint(p)

    def setBackwardPrintable(self, b):
        self.getDecoratedFigure().setBackwardPrintable(b)

