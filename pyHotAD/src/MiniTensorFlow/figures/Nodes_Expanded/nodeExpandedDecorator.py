from MiniTensorFlow.figures.pyHADNodeConnectionFigure import pyHADNodeConnectionFigure

from MiniTensorFlow.figures.Nodes.NodeFigure import NodeFigure


class nodeExpandedDecorator(NodeFigure):

    def __init__(self, x, y, w, h):
        NodeFigure.__init__(self, x, y, w, h)
        self._internal_net = {'inputs': [],
                              'weight': [],
                              'net':    []}
        self.createInternalNet()
        self.assignNetPosition()

    def createInternalNet(self):
        """
        Genera la red que representa un nodo complejo para ser visualizada.
        :return:
        """
        pass

    def assignNetPosition(self):
        """
        Genera la red que representa un nodo complejo para ser visualizada.
        :return:
        """
        pass

    def setNodePosition(self, node, i, j):
        x, y, w, h = self.dimmensions()
        node.x0 = x + i*w
        node.y0 = y + j*h


    @classmethod
    def createConnection(cls, start_node, end_node, number_end_connector=0):
        connector_figure = pyHADNodeConnectionFigure()
        cStart = start_node.getRigthConnectors()
        eConnectors = end_node.getLeftConnectors()
        cEnd = eConnectors[number_end_connector] if isinstance(eConnectors, list) else eConnectors
        connector_figure.setConnectorStart(cStart)
        connector_figure.setConnectorEnd(cEnd)
        connector_figure.addPoint(cStart.findStart(connector_figure))
        connector_figure.addPoint(cEnd.findStart(connector_figure))


