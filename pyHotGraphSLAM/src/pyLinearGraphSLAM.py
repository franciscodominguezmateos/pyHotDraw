'''
Created on 5 Aug 2019

@author: francisco
Inspired by Udacity
'''
from matrix import matrix

class pyLinearGraphSLAM(object):
    '''
    classdocs
    '''


    def __init__(self, dim=1,subDim=2):
        '''
        Constructor
        '''
        self.subDim=subDim
        self.Omega=matrix(dim,dim,subDim=2) 
        self.Xi   =matrix(dim,1)
    '''
    dataXi has to be a np.array with shape (subDim,1)
    '''
    def setSubmatrix(self,pn,pm,dataOmega,dataXi):
        n=self.subDim*int(pn)
        m=self.subDim*int(pm)
        for b in range(self.subDim):
            self.Omega.value[n+b][n+b] +=  dataOmega
            self.Omega.value[m+b][m+b] +=  dataOmega
            self.Omega.value[n+b][m+b] += -dataOmega
            self.Omega.value[m+b][n+b] += -dataOmega
            self.Xi.value[n+b][0]      += -dataXi[b]
            self.Xi.value[m+b][0]      +=  dataXi[b]