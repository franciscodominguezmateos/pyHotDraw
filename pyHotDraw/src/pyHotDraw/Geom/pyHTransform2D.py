class pyHTransform2D:
    def __init__(self,sx=1,sy=1,tx=0,ty=0):
        self.sx=sx
        self.sy=sy
        self.tx=tx
        self.ty=ty
    def transform(self,x,y):
        sx=self.sx
        sy=self.sy
        tx=self.tx
        ty=self.ty
        return x*sx+tx,y*sy+ty
    def itransform(self,x,y):
        sx=self.sx
        sy=self.sy
        tx=self.tx
        ty=self.ty
        return (x-tx)/sx,(y-ty)/sy
    def scale(self,x,y):
        return x*self.sx,y*self.sy
    def iscale(self,x,y):
        return x/self.sx,y/self.sy
    # Transformation composition, could be a product but I prefer an addition operator
    # transformation composition is not transitive
    def __add__(self,p):
        return pyHTransform2D(self.sx*p.sx,self.sy*p.sy,self.tx*p.sx+p.tx,self.ty*p.sy+p.ty)