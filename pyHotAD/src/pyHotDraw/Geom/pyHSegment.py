from pyHLine import pyHLine
class Segment:
    def __init__(self,p0,p1):
        self.v0=p0
        self.v1=p1
        self.line=pyHLine(self.v0,self.v1)
    def __str__(self):
        return self.v0.__str__() + self.v1.__str__()
    def getOrigin(self):
        return self.v0
    def getEnd(self):
        return self.v1
    def getLength(self):
        return (self.v1-self.v0).mag
    def getLine(self):
        return self.line
    def contains(self,point):
        l=self.getLine()
        if(l.contains(point)):
            #check just the case point==v0
            if point.getX != self.v0.getX and point.getY != self.v0.getY:
                v=point-self.v0
                vn=v.norm()
                sn=self.getLine().getV().norm()
                #print "norma",vn,sn
                #print "mag",v.mag,self.getLength()
                #v must have the same direction as self.line.getV()
                #print "ddkd",abs(vn.x-sn.x)<0.0001
                if(abs(vn.getX-sn.getX)<0.0001 and abs(vn.getY-sn.getY)<0.0001):
                    b=v.mag<=self.getLength()
                    #print "bool2",b
                    return b
                else:
                    return False
            else:
                return True
    def canIntersect(self,s1):
        l0=self.getLine()
        l1=s1.getLine()
        if(l0.canIntersect(l1)):
            v=l0.intersect(l1)
            if(self.contains(v) and s1.contains(v)):
                return True
            else:
                return False
        else:
            return False
    def intersect(self,s1):
        l0=self.getLine()
        l1=s1.getLine()
        v=l0.intersect(l1)
        if(self.contains(v) and s1.contains(v)):
            return v
        else:
            raise PointNotIntersectSegments("Point Not in Intersected Segment "+v.__str__())
    def intersectCut(self,sNext):
        v=self.intersect(sNext)
        return (Segment(self.getOrigin(),v),Segment(v,sNext.getEnd()))

class PointNotIntersectSegments(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
