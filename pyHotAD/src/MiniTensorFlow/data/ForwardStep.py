#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.data.AbstractForwardStep import AbstractForwardStep

class ForwardStep(AbstractForwardStep):

    def __init__(self, node, view):
        AbstractForwardStep.__init__(self, node, view)
        self._steps_list.append(self.step4)


    def step4(self):
        """
        Elimina la figura de información y muestra el resultado de la operación 'forward' en su
        conector de salida.
        :return:
        """
        self.node.setForwardPrintable(True)
        self.view.getDrawing().removeFigure(self.info_figure)

        for input_conector in self.node.get_inputs_links():
            self.makeConnectorOpaque(input_conector)
            self.makeNodeOpaque(input_conector.get_start_node())

        for out_contector in self.node.get_outputs_links():
            self.makeConnectorEnphasis(out_contector)

        self.view.update()

    def endStep(self):
        self.makeNodeOpaque(self.node)
        for out_conector in self.node.get_outputs_links():
            self.makeConnectorOpaque(out_conector)


