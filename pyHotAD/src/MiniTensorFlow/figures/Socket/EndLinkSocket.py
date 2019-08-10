#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.figures.Socket.Socket import Socket

class EndLinkSocket(Socket):
    """
    Este socket es una abstracción que representa una entrada a un nodo. En los
    nodos, por norma general, solo se permite un conector por cada socket
    entrada.
    """

    MAX_ACCEPTABLES_INPUTS = 1
    MAX_ACCEPTABLES_OUTPUTS = 0

    def __init__(self, owner):
        Socket.__init__(self,
                        owner,
                        self.MAX_ACCEPTABLES_INPUTS,
                        self.MAX_ACCEPTABLES_OUTPUTS)

    def is_free(self):
        max_acceptable_inputs = self.max_acceptables_inputs_links()
        acceptable_infinites = max_acceptable_inputs == -1
        acceptable_new = len(self.get_link()) < max_acceptable_inputs

        return acceptable_infinites or acceptable_new
