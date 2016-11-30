'''
Created on 25/03/2013

@author: paco
'''

class pyHAbstractTool(object):
    '''
    classdocs
    '''
    def __init__(self,v):
        '''
        Constructor
        '''
        self.view=v
    def getView(self):
        return self.view
    def onMouseDown(self,e):
        pass
    def onMouseUp(self,e):
        self.view.update()
    def onMouseMove(self,e):
        pass
    def onMouseDobleClick(self,e):
        pass
    def onMouseWheel(self,e):
        pass
    def onKeyPressed(self,e):
        pass