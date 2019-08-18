#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 17/04/2015

@author: Francisco Dominguez
'''
import numpy as np
import cv2

class pyHImage():
    '''
    classdocs
    '''
    def __init__(self,fileName='../images/im2.png',scale=1):
        #This is platform specific we have to change it
        #data return a openCv or numpy image format
        civ=cv2.imread(fileName)
        if civ is None:
            print "Image not found: "+fileName 
            civ=cv2.imread('../images/im2.png')
        if scale!=1: # better performance
            nw=int(civ.shape[1]*scale)
            nh=int(civ.shape[0]*scale)
            civ=cv2.resize(civ,(nw,nh))
        self.data=civ
    # in GBR format
    def setData(self,npArray):
        self.data=npArray
    def setDataRGB(self,npArray):
        self.data=cv2.cvtColor(np.asarray(npArray,np.uint8), cv2.COLOR_RGB2BGR)
    def setDataGray(self,npArray):
        self.data=cv2.cvtColor(np.asarray(npArray,np.uint8), cv2.COLOR_GRAY2BGR)
        #self.data=npArray.copy()
    def getData(self):
        return self.data
    def getRGBData(self):
        return cv2.cvtColor(self.getData(), cv2.COLOR_BGR2RGB)
    def getWidth(self):
        return self.data.shape[1]
    def getHeight(self):
        return self.data.shape[0]
    def getAspectRatio(self):
        return float(self.getWidth())/float(self.getHeight())
    ''' Fitting figures to size keeping aspectratio '''
    ''' not sure where to put this code '''
#     def isPortrait(self):
#         return self.getWidth() < self.getHeight()
#     def getPortraitImageFigure(self,height=40):
#         ar=self.getAspectRatio()
#         imf=pyHImageFigure(0,0,height*ar,height,self)
#         return imf
#     def getLandscapeImageFigure(pyHImg,width=40):
#         ar=pyHImg.getAspectRatio()
#         imf=pyHImageFigure(0,0,width,width/ar,pyHImg)
#         return imf
#     def bestFitImageFigure(pyHImg,size=40):
#         if isPortrait(pyHImg):
#             return getPortraitImageFigure(pyHImg, size)
#         return getLandscapeImageFigure(pyHImg, size)


