'''
Created on 25/03/2013

@author: paco
'''

class pyHStandardEvent:
    def __init__(self,x,y,button=0,key=0):
        self.x=x
        self.y=y
        self.button=0
        self.key=0
        pass
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getButton(self):
        return self.button
    def getKey(self):
        return self.key
