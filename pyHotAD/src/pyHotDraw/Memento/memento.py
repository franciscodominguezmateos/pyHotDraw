#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Memento dessign pattern.
 http://www.blackwasp.co.uk/gofpatterns.aspx
 http://www.blackwasp.co.uk/Memento.aspx
"""

import copy

class memento(object):
    """
    The Memento class is used to hold the information from an Originator's state.
    The amount of information held is controlled by the Originator. The Memento
    can provide protection against change to the stored state by including a very
    limited interface with no means of modifying the values it holds.
    """

    def __init__(self, state, deep=False):
        self._state = copy.deepcopy(state) if bool(deep) else copy.copy(state)

    def getState(self):
        return self._state


class originator(object):
    """
    This is the class whose state is to be stored. The Originator includes a method,
    named "CreateMemento", that is used to generate a Memento object containing a
    snapshot of the Originator's current state. It also includes the "SetMemento"
    method, which restores the Originator to a previously stored state
    """

    _state = None

    def setMemento(self, m):
        self._state = m.getState()

    def createMemento(self):
        return memento(self._state)

class caretaker(object):
    """
    The Caretaker class is used to hold a Memento object for later use. The Caretaker
    provides storage only; it should neither examine nor modify the contents of the
    Memento object. In the UML diagram and the examples in this article the Caretaker
    holds a single Memento object. It can be modified to hold a collection of Mementos
    to support multi-level undo and redo functionality.
    """
    pass



def createUndo(figure_list):
    return memento(figure_list)