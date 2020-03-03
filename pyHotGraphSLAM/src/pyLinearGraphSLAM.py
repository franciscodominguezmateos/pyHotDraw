'''
Created on 5 Aug 2019

@author: Francisco Dominguez
Inspired by Udacity
'''
from matrix import matrix
from platform import node
from geometry_msgs.msg._PoseStamped import PoseStamped

class pyLinearGraphSLAM(object):
    '''
    classdocs
    '''
    def __init__(self,subDim=2, pose=(50,50), noise=1.0):
        '''
        Constructor
        '''
        #Number of Pose
        self.N=1
        #Number of landmarks
        self.L=0
        #subDim are dimensions of the problem for 2D pose subDim is only 2
        self.subDim=subDim
        dim=self.getDim()
        self.dim=dim
        self.Omega=matrix() 
        self.Omega.zero(dim, dim)
        for i in range(subDim):
            self.Omega.value[i][i] = 1.0
        self.Xi   =matrix()
        self.Xi.zero(dim, 1)
        # initial pose now (50,50)-> subdim=2
        for i in range(subDim):
            self.Xi.value[i][0] = pose[i] / noise
        self.pose2PoseEdges=[]
        self.pose2MeasurementEdges=[]
    ''' Dimension of matrix is (N+L)*subDim '''
    def getDim(self):
        return (self.N+self.L)*self.subDim
    '''
    dataXi has to be a np.array with shape (subDim,1)
    '''
    def getNPoses(self):
        return self.N
    def getNLandMarks(self):
        return self.L
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
    def allocPose(self):
        subDim=self.subDim
        ND=self.getNPoses()*subDim
        LD=self.getNLandMarks()*subDim
        newDim=self.getDim()+subDim
        l0=range(ND)
        l1=[ND+subDim+i for i in range(LD)]
        ranges=l0+l1
        self.Omega=self.Omega.expand(newDim,newDim,ranges)
        self.Xi=self.Xi.expand(newDim,1,ranges,[0])
        self.N+=1
        self.dim+=self.getDim()
    def allocMeasurement(self):
        subDim=self.subDim
        ND=self.getNPoses()*subDim
        newDim=self.getDim()+subDim
        ranges=range(self.getDim())
        self.Omega=self.Omega.expand(newDim,newDim,ranges)
        self.Xi=self.Xi.expand(newDim,1,ranges,[0])
        self.L+=1
        self.dim+=self.getDim()
    def setPose2PoseEdge(self,ps,pe,values,noise=1):
        N=self.getNPoses()
        if ps>=N:
            raise Exception("Pose source must be a existing node")
        if pe==N:
            #inserting new node
            #grow matrices
            self.allocPose()
        if pe>N:
            raise Exception("Pose end must exists or be N+1 in order to insert new node")            
        self.setSubmatrix(ps,pe,1.0/noise,values/noise)
        self.pose2PoseEdges.append((ps,pe,values,noise))
    ''' Meaurement end must exists or be N+1 in order to insert new node'''    
    def setPose2MeasurementEdge(self,ps,pe,values,noise=1):
        N=self.getNPoses()
        L=self.getNLandMarks()
        if ps>=N:
            raise Exception("Pose source must be an existing node")
        if pe==L:
            #inserting new node
            #grow matrices
            self.allocMeasurement()
        if pe>L:
            raise Exception("Meaurement end must exists or be L+1 in order to insert new node")            
        self.setSubmatrix(ps,N+pe,1.0/noise,values/noise)
        self.pose2MeasurementEdges.append((ps,pe,values,noise))

    def solve(self):
        # compute best estimate
        self.mu = self.Omega.inverse() * self.Xi
        return self.mu

if __name__ == '__main__':
    g=pyLinearGraphSLAM()
    g.allocPose()
    g.allocMeasurement()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        