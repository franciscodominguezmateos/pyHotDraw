#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 1/03/2017

@author: javi
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *




class pyHADNodeInfoPanel(QWidget):
    MAX_HEIGHT = 200
    def __init__(self, parent=None, **kwargs):
        super(QWidget, self).__init__(parent)
        self.setGeometry(0, 0, parent.getWidth(), self.MAX_HEIGHT)
        self.setAutoFillBackground(True)


        # self.view = self.parent().getView()

        self.setContentsMargins(-10,-10,-10,-10)
        self.initUI()

    def initUI(self):

        self.setMinimumSize(1,30)
        self.setMaximumSize(1000000, self.MAX_HEIGHT)

        funcTextLabel = QLabel(self)
        funcTextLabel.set_text('Function evaluated: ')
        funcTextLabel.move(30,30)


        self.show()







