#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.data.AbstractForwardStep import AbstractForwardStep


class ForwardEndNodeStep(AbstractForwardStep):
    def __init__(self, node, outLine, view):
        AbstractForwardStep.__init__(self, node, view)
        self.out_line_figure = outLine
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

        self.makeConnectorEnphasis(self.out_line_figure)
        self.view.update()


    def endStep(self):
        self.makeNodeOpaque(self.node)
        self.makeConnectorOpaque(self.out_line_figure)