#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 27/03/2013

@author: paco
'''

class pyHAttributeColor(object):
    '''
    classdocs
    '''
    def __init__(self,r,g,b,a=255):
        '''
        Constructor
        '''
        self.r=r
        self.g=g
        self.b=b
        self.a=a
    def draw(self,g):
        g.setColor(self.r,self.g,self.b,self.a)
        
class pyHAttributeWidth(object):
    '''
    classdocs
    '''
    def __init__(self,w):
        '''
        Constructor
        '''
        self.w=w
    def draw(self,g):
        g.setWidth(self.w)
class pyHAttributeDotLine(object):
    '''
    classdocs
    '''
    def __init__(self):
        pass
    def draw(self,g):
        g.setDotLine()
class pyHAttributeSolidLine(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def draw(self,g):
        g.SolidLine()
        