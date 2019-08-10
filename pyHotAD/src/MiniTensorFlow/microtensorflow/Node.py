"""
Created on Jun 17, 2017

@author: Francisco Dominguez
"""
import numpy as np


class Node:
    def __init__(self):
        self.input = []
        self.partialFunctions = []
        self.output = []
        self.partialsLocal = {}
        self.partialsGlobal = {}
        self.partials = {}
        self.operation = None
        self.differetial = None
        self.value = 0
        self.partialGlobal = 1

    def getValue(self):
        return self.value

    def forward(self):
        return self.value

    def backward(self):
        self.setPartialsGlobal()
        self.setPartialGlobal()
        self.setPartialsLocal()
        self.setPartials()

    def setPartialsGlobal(self):
        for o in self.output:
            self.partialsGlobal[o] = o.getPartial(self)

    def setPartialGlobal(self):
        if len(self.partialsGlobal) == 0:
            self.partialGlobal = 1
            return
        t = 0
        for k in self.partialsGlobal:
            t += self.partialsGlobal[k]
        self.partialGlobal = t

    # This method should be redefined
    def setPartialsLocal(self):
        for i, n in enumerate(self.input):
            f = self.partialFunctions[i]
            self.partialsLocal[i] = f(n.value)

    def setPartials(self):
        for n in self.input:
            self.partials[n] = self.partialsLocal[n] * self.partialGlobal

    def getPartial(self, i):
        return self.partials[i]

    def get_partial_value(self):
        return self.partialGlobal

    def getPartialLocal(self, i):
        return self.partialsLocal[i]