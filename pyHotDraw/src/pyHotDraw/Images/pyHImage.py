#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 17/04/2015

@author: paco
'''
import numpy as np
import cv2
from PyQt4.QtGui import QImage
class pyHImage():
    '''
    classdocs
    '''
    def __init__(self,fileName='../images/im2.png'):
        #This is platform specific we have to change it
        #data return a openCv or numpy image format
        civ=cv2.imread(fileName)
        self.data=civ
    def setData(self,npArray):
        self.data=npArray
        #self.data=npArray.copy()
    def getData(self):
        return self.data
    def getWidth(self):
        return self.data.shape[1]
    def getHeight(self):
        return self.data.shape[0]
    def convertQImageToMat(self,qImg):
        '''  Converts a QImage into an opencv MAT format  '''
        incomingImage = qImg.convertToFormat(QImage.Format.Format_RGB32)
        width  = incomingImage.width()
        height = incomingImage.height()
        ptr = incomingImage.constBits()
        arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
        return arr        
    def convertMatToQImage(self,w=320,h=240):
        opencvBgrImg=cv2.resize(self.data,(int(w),int(h)))
        opencvRgbImg=cv2.cvtColor(opencvBgrImg, cv2.COLOR_BGR2RGB)
        d=opencvRgbImg.shape[2]
        w=opencvRgbImg.shape[1]
        h=opencvRgbImg.shape[0]
        #qImg=QImage(opencvRgbImg.tostring(),opencvRgbImg.shape[1],opencvRgbImg.shape[0],QImage.Format.Format_RGB888)
        qImg=QImage(opencvRgbImg.data,w,h,w*3,QImage.Format_RGB888)
        return qImg
