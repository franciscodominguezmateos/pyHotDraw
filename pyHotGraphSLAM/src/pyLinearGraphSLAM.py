'''
Created on 5 Aug 2019

@author: francisco
Inspired by Udacity
'''
from matrix import matrix
from platform import node

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
        self.Omega.zero(dim, dim)
        self.Omega.value[0][0] = 1.0
        self.Omega.value[1][1] = 1.0
        self.Xi   =matrix(dim,1)
        self.Xi.zero(dim, 1)
        # initial pose now (50,50)-> subdim=2
        self.Xi.value[0][0] = 100 / 2.0
        self.Xi.value[1][0] = 100 / 2.0
        self.pose2PoseEdges=[]
        self.pose2MeasurementEdges=[]
    '''
    dataXi has to be a np.array with shape (subDim,1)
    '''
    def getNPoses(self):
        return 0
    def getNMeasurements(self):
        return 0
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
            
    def setPose2PoseEdge(self,ps,pe,values,noise=1):
        N=self.getNPoses()
        if ps>=N:
            raise Exception("Pose source must be a existing node")
        if pe==N:
            #inserting new node
            #grow matrices
            pass
        if pe>N:
            raise Exception("Pose end must exists or be N+1 in order to insert new node")            
        self.setSubmatrix(ps,pe,1.0/noise,values/noise)
        self.pose2PoseEdges.append((ps,pe,values,noise))
        
    def setPose2MeasurementEdge(self,ps,pe,values,noise=1):
        N=self.getNPoses()
        L=self.getNMeasurements()
        if ps>=N:
            raise Exception("Pose source must be an existing node")
        if pe==L:
            #inserting new node
            #grow matrices
            pass
        if pe>L:
            raise Exception("Meaurement end must exists or be N+1 in order to insert new node")            
        self.setSubmatrix(ps,N+pe,1.0/noise,values/noise)
        self.pose2MeasurementEdges.append((ps,pe,values,noise))

    def solve(self):
        # compute best estimate
        mu = self.Omega.inverse() * self.Xi
        return mu
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        