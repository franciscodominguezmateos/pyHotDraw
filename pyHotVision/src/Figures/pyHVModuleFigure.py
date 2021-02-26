'''
Created on 14 Nov 2020

@author: Francisco Dominguez
First try to put some kind of process node
'''
from pyHotDraw.Figures.pyHImageFigure import pyHImageFilterFigure

class pyHVModuleFigure(pyHImageFilterFigure):
    '''
    Kind of process nodes,.. but,,.. still thinking about it,...
    '''
    def __init__(self,x0,y0,w,h,text="ModuleFilter"):
        #super(pyHImageFilterFigure,self).__init__(x0,y0,w,h)
        super(pyHImageFilterFigure,self).__init__(x0,y0,w,h,text)
    def launchModule(self,phImg):
        pass
    def imageChanged(self,phImg):
        self.imageSink=self.launchModule(phImg)
        self.notifyImageChanged()


        