#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 18/04/2015

@author: paco
'''
import numpy as np
import cv2
from PySide import QtGui

class OpenCVQImage(QtGui.QImage):
    def __init__(self, opencvBgrImg):
        opencvRgbImg=cv2.cvtColor(opencvBgrImg, cv2.COLOR_BGR2RGB)
        _imgData = opencvRgbImg.tostring()
        height, width, channels = opencvRgbImg.shape
        super(OpenCVQImage, self).__init__(_imgData, width,height, QtGui.QImage.Format_RGB888)
    def convertQImageToMat(self):
        '''  Converts a QImage into an opencv MAT format  '''
        incomingImage = self.convertToFormat(QtGui.QImage.Format.Format_RGB32)
        width = incomingImage.width()
        height = incomingImage.height()
        ptr = incomingImage.constBits()
        arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
        return arr