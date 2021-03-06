#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 30/03/2013

@author: Francisco Dominguez
19-07-2019 try to make handles zoom independent
'''

class pyHAbstractHandle(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.view=None
        # in pixel
        self.width=4
        self.height=4
    def setView(self,v):
        self.view=v
    # TODO try to make handles zoom independent
    # this has to be called before draw method and would be userd to set with and height of rectangle or handle shape
    def getHandleSize(self):
        t=self.view.getTransform()
        return t.iscale(self.width,self.height)