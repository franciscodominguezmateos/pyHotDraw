from visual import vector
import numpy as np
from  LineExceptions import *
"""
From Parametric Equation to General Equation
x=v.x*t+p.x -> t=(x-p.x)/v.x
y=v.y*t+p.y -> t=(y-p.y)/v.y
  (x-p.x)*v.y=(y-p.y)*v.x
x*v.y-p.x*v.y=y*v.x-p.y*v.x
x*v.y-y*v.x-p.x*v.y+p.y*v.x=0
v.y*x-v.x*y-p.x*v.y+p.y*v.x=0
 a *x+ b *y+      c        =0
a=v.y   b=-v.x  c=-p.x*v.y+p.y*v.x
"""
class pyHLine:
    def __init__(self,p0,p1):
        self.p=p0
        self.v=vector(p1-p0).norm()
    def getV(self):
        return self.v
    def getP(self):
        return self.p
    def canIntersect(self,l1):
        v=self.getV().cross(l1.getV())
        if(v.mag==0):
            return False
        else:
            return True
    def getGeneralEquation(self):
        v=self.getV()
        p=self.getP()
        a= v.y
        b=-v.x
        c=-p.x*v.y+p.y*v.x
        return (a,b,c)
    def getParametricEquation(self):
        return (self.p,self.v)
    def distance(self,point):
        (a,b,c)=self.getGeneralEquation()
        return abs(a*point.x+b*point.y+c)/vector(a,b).mag
    def contains(self,point):
        return self.distance(point)<0.001
    def intersect(self,lin1):
        if(self.canIntersect(lin1)):
            (a0,b0,c0)= self.getGeneralEquation()
            (a1,b1,c1)= lin1.getGeneralEquation()
            a=np.array([[a0,b0],[a1,b1]])
            b=np.array([-c0,-c1])
            x=np.linalg.solve(a,b)
            return vector(x)
        else:
            raise NoIntersectLines("No Intersect Lines") 
            
class NoIntersectLines(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
       return repr(self.value)