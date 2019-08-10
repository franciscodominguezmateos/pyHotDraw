'''
Created on 25/03/2013

@author: paco
'''
from pyHotDraw.Images.pyHImage import pyHImage
from pyHotDraw.Figures.pyHImageFigure import pyHImageFigure

class pyHCreationImageTool(object):
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
        i=pyHImage('../images/im2.png')
        f=pyHImageFigure(e.getX(),e.getY(),i.getWidth(),i.getHeight(),i)
        self.view.getDrawing().addFigure(f)
        self.view.update()
    def onMouseUp(self,e):
        pass
    def onMouseMove(self,e):
        pass

    def onMouseGrab(self,e):
        print ("onMouseGrab in pyHCreationTool")
        self.createdFigure.setDisplayBox()
    def onMouseDobleClick(self,e):
        pass
    def onMouseWheel(self,e):
        pass
    def onKeyPressed(self,e):
        pass