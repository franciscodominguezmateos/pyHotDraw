#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.data.AbstractBackwardStep import AbstractBackwardStep


class BackwardStep(AbstractBackwardStep):
    def __init__(self, node, view):
        AbstractBackwardStep.__init__(self, node, view)


    def step0(self):
        """
        Vuelve opacos el nodo sobre el que se mostrará la información, así como sus
        nodos salida (y sus respectivos conectores)
        """
        self.makeNodeEnphasis(self.node)
        for output_conector in self.node.get_outputs_links():
            self.makeConnectorEnphasis(output_conector)
            self.makeNodeEnphasis(output_conector.get_end_node())


    def endStep(self):
        self.makeNodeOpaque(self.node)
        for out_conector in self.node.get_outputs_links():
            self.makeConnectorOpaque(out_conector)