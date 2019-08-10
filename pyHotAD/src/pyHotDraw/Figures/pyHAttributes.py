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

    def values(self):
        return self.r, self.g, self.b, self.a

    def draw(self,g):
        g.setColor(self.r,self.g,self.b,self.a)

class pyHAttributeFillColor(object):
    '''
    classdocs
    '''

    def __init__(self, r, g, b, a=255):
        '''
        Constructor
        '''
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def values(self):
        return self.r, self.g, self.b, self.a

    def draw(self, g):
        g.setFillColor(self.r, self.g, self.b, self.a)




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

""" FONT METHODS"""
class pyAttributeFont(object):

    def __init__(self, family, size, bold, italic):
        pass

class pyHAttributeFontSize(object):
    """
    Tamaño de la fuente usada en las figuras texto
    """

    def __init__(self, size):
        self.size = float(size)

    def draw(self, g):
        g.setFontSize(self.size)


class pyHAttributeFontBold(object):
    """
    Hacer negrita la fuente usada en las figuras texto
    """

    def __init__(self):
        pass

    def draw(self, g):
        g.setFontBold()