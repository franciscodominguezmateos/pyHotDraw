#!/usr/bin/python
# -*- coding: utf-8 -*-

from MiniTensorFlow.figures.Socket.Socket import Socket

class StartLinkSocket(Socket):

    MAX_INPUTS_LINKS = 0
    MAX_OUTPUTS_LINKS = -1

    def __init__(self, owner):
        Socket.__init__(self,
                        owner,
                        self.MAX_INPUTS_LINKS,
                        self.MAX_OUTPUTS_LINKS)

    def is_free(self):
        max_acceptable_ouputs = self.max_acceptables_outputs_links()
        acceptable_infinites = max_acceptable_ouputs == -1
        acceptable_new = len(self.get_link()) < max_acceptable_ouputs

        return acceptable_infinites or acceptable_new
