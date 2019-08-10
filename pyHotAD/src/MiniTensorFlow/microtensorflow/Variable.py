"""
Created on Jun 17, 2017

@author: Francisco Dominguez
"""

import numpy as np
from MiniTensorFlow.microtensorflow.Node import Node

class Variable(Node):

    def __init__(self, s):
        Node.__init__(self)
        self.value = np.matrix(s)
        self.input.append(self)


    def setPartialsLocal(self):
        self.partialsLocal[self] = 1  # np.ones_like(self.value)


    def setValue(self, v):
        self.value = v


    def update(self, alpha):
        partial = self.getPartial(self)
        iValue = -partial  # We want the opposite direction of the gradient
        new_value = self.value + alpha*iValue
        self.value = new_value
        #self.value += alpha * iValue
        """
        Numpy error in python3:
        self.value += alpha * iValue
        TypeError: Cannot cast ufunc add output from dtype('float64') to
                    dtype('int64') with casting rule 'same_kind'
        """

    @staticmethod
    def is_acceptable_arg(arg):
        try:
            np.matrix(arg)
            return True
        except ValueError:
            return False

