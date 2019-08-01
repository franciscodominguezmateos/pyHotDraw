'''
Created on 25/03/2013

@author: paco
'''

class pyHStandardEvent:
    LeftButton=0
    RightButton=1
    MiddleButton=2
    def __init__(self,x,y,button=0,key=0):
        self.x=x
        self.y=y
        self.button=button
        self.key=key
        pass
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getButton(self):
        return self.button
    def getKey(self):
        return self.key
