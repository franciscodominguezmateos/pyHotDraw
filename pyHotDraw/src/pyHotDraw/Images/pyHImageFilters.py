#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 25/04/2015

@author: Francisco Dominguez
+03/02/2016
'''
import numpy as np
from math import sqrt
import cv2

class Undistor():
    def __init__(self,mtx,dist):
        self.mtx=mtx
        self.dist=dist
    def process(self,imgcv):
        ret= cv2.undistort(imgcv, self.mtx, self.dist, None, self.mtx)
        return ret
class GrayFilter():
    def process(self,imgcv):
        gray = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
        ret=cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return ret
class Bilateral():
    def process(self,imgcv):
        ret= cv2.bilateralFilter(imgcv,9,75,75)
        return ret
class Blur():
    def process(self,imgcv):
        ret= cv2.blur(imgcv,(5,5))
        return ret
class Gaussian():
    def process(self,imgcv):
        ret= cv2.GaussianBlur(imgcv,(9,9),0)
        return ret
class Median():
    def process(self,imgcv):
        ret= cv2.medianBlur(imgcv,5)
        return ret
class SobelX():
    def process(self,imgcv):
        gray = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
        ret=cv2.Sobel(gray,cv2.CV_8U,1,0,ksize=3)
        ret=cv2.cvtColor(ret,cv2.COLOR_GRAY2BGR)
        return ret
class SobelY():
    def process(self,imgcv):
        gray = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
        ret=cv2.Sobel(gray,cv2.CV_8U,0,1,ksize=3)
        ret=cv2.cvtColor(ret,cv2.COLOR_GRAY2BGR)
        return ret
class ScharrX():
    def process(self,imgcv):
        gray = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
        ret=cv2.Scharr(gray,cv2.CV_8U,1,0)
        ret=cv2.cvtColor(ret,cv2.COLOR_GRAY2BGR)
        return ret
class ScharrY():
    def process(self,imgcv):
        gray = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
        ret=cv2.Scharr(gray,cv2.CV_8U,0,1)
        ret=cv2.cvtColor(ret,cv2.COLOR_GRAY2BGR)
        return ret
class Laplacian():
    def process(self,imgcv):
        gray = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
        sobelx64f=cv2.Laplacian(gray,cv2.CV_64F)
        abs_sobel64f = np.absolute(sobelx64f)
        sobel_8u = np.uint8(abs_sobel64f)
        ret=cv2.cvtColor(sobel_8u,cv2.COLOR_GRAY2BGR)
        return ret
class FastFeatureDetector():
    def __init__(self):
        self.fast=cv2.FastFeatureDetector_create()
    def process(self,imgcv):
        gray = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
        self.kp = self.fast.detect(gray, None)
        ret = cv2.drawKeypoints(gray, self.kp, None, color = (0, 255, 0), )
        return ret
    def getPoints(self):
        return self.kp
class FeatureDetector():
    #detector_format = ["","Grid","Pyramid"]
    # "Dense" and "SimpleBlob" omitted because they caused the program to crash
    #detector_types = ["FAST","STAR","SIFT","SURF","ORB","MSER","GFTT","HARRIS"]
    def __init__(self,detector='HARRIS'):
        self.forb = cv2.FeatureDetector_create(detector)
    def process(self,imgcv):
        gray = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
        grayGauss= cv2.GaussianBlur(imgcv,(5,5),0)
        self.kp = self.forb.detect(grayGauss)
        ret = cv2.drawKeypoints(gray, self.kp, None, color = (0, 255, 0), )
        return ret
    def getPoints(self):
        return self.kp
class DescriptionExtrator():
    def __init__(self,detector='HARRIS'):
        self.forb = cv2.DescriptorExtractor_create(detector)
    def process(self,imgcv):
        gray = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
        grayGauss= cv2.GaussianBlur(imgcv,(5,5),0)
        self.kp, self.des = self.forb.compute(grayGauss, self.kp)
class FaceDetection():
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade  = cv2.CascadeClassifier('haarcascade_eye.xml')     
    def process(self,frameI):
        frame=frameI.copy()
        #Face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                cv2.circle(roi_color,(ex+ew/2,ey+eh/2),ew/2,(0,255,0),2)
        return frame
class ColorSpace():
    def __init__(self,colorSpaceName="RGB"):
        self.colorSpace=colorSpaceName
    def process(self,image):
        color_space=self.colorSpace
        # apply color conversion if other than 'RGB'
        if color_space != 'RGB':
            if color_space == 'HSV':
                feature_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            elif color_space == 'LUV':
                feature_image = cv2.cvtColor(image, cv2.COLOR_RGB2LUV)
            elif color_space == 'HLS':
                feature_image = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
            elif color_space == 'YUV':
                feature_image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
            #elif color_space == 'YCrCb':
            #    feature_image = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
        else:
            feature_image = np.copy(image)
        return feature_image
        
class OpticalFlow():
    def draw_flow(self,im,flow,step=16):
        """ Plot optical flow at same points spaced step pixels apart."""
        h,w=im.shape[:2]
        y,x=np.mgrid[step/2:h:step,step/2:w:step].reshape(2,-1)
        fx,fy=flow[y,x].T
        #create line endpoints
        lines=np.vstack([x,y,fx,fy]).T.reshape(-1,2,2)
        lines=np.int32(lines)
        #create image and draw
        vis=cv2.cvtColor(im,cv2.COLOR_GRAY2BGR)
        for (x1,y1),(fx2,fy2) in lines:
            x2,y2=x1+fx2,y1+fy2
            if sqrt(fx2*fx2+fy2*fy2)>1.0:
                cv2.line(vis,(x1,y1),(x2,y2),(0,0,255))
                cv2.circle(vis,(x2,y2),1,(0,0,255))
            #else:    
            #    cv2.line(vis,(x1,y1),(x2,y2),(0,255,0))
            #    cv2.circle(vis,(x1,y1),1,(0,255,0))
        return vis
    def __init__(self):
        self.prvs=None
    def process(self,imgcv):
        gray = np.uint8(cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY))
        if self.prvs==None:
            self.prvs=gray.copy()
            self.hsv = np.zeros_like(imgcv)[:,:,:3]
            self.hsv[...,1] = 255
        #Optical flow
        #flow = cv2.calcOpticalFlowFarneback(self.prvs,gray, 0.5, 3, 15, 3, 5, 1.2, 0)
        flow = cv2.calcOpticalFlowFarneback(self.prvs,gray,flow=None,
                                        pyr_scale=0.5, levels=1, winsize=15,
                                        iterations=2,
                                        poly_n=5, poly_sigma=1.1, flags=0)
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        self.hsv[...,0] = ang*180/np.pi/2
        #self.hsv[...,2]=255
        #self.hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        self.hsv[...,2] = np.minimum(mag*8, 255)
        bgr = cv2.cvtColor(self.hsv,cv2.COLOR_HSV2BGR)
        self.prvs=gray
        #return self.draw_flow(gray,flow)
        #vis=cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
        return cv2.addWeighted(bgr,0.9,self.draw_flow(gray,flow),0.5,0)
    
def drawpoints(img1,img2,pts1,pts2):
    img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]
    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')
    # Place the first image to the left
    out[:rows1,:cols1,:] = img1 
    # Place the next image to the right of it
    out[:rows2,cols1:cols1+cols2,:] = img2 
    for pt1,pt2 in zip(pts1,pts2):
        color = tuple(np.random.randint(0,255,3).tolist())
        cv2.circle(out,tuple(pt1),5,color,-1)
        cv2.circle(out,(pt2[0]+cols1,pt2[1]),5,color,-1)
        cv2.line(out, tuple(pt1), (pt2[0]+cols1,pt2[1]), color,1)
    return out

class FlannMacher():
    def __init__(self):
        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)     
        self.flann = cv2.FlannBasedMatcher(index_params,search_params)
        self.detector = cv2.FastFeatureDetector()#sSIFT()     
    def process(self):
        img1 = cv2.cvtColor(self.imgcv1, cv2.COLOR_BGR2GRAY)  #queryimage # left image
        img2 = cv2.cvtColor(self.imgcv2, cv2.COLOR_BGR2GRAY)  #trainimage # right image
        # find the keypoints and descriptors with SIFT
        kp1, des1 = self.detector.detectAndCompute(img1,None)
        kp2, des2 = self.detector.detectAndCompute(img2,None)      
        matches = self.flann.knnMatch(des1,des2,k=2)       
        pts1 = []
        pts2 = []        
        # ratio test as per Lowe's paper
        for i,(m,n) in enumerate(matches):
            if m.distance < 0.8*n.distance:
                pts2.append(kp2[m.trainIdx].pt)
                pts1.append(kp1[m.queryIdx].pt)
        self.data=(pts1,pts2)
        pts1i=np.int32(pts1)
        pts2i=np.int32(pts2)
        return drawpoints(img1,img2,pts1i,pts2i)
        
class FundamentalMatrix():
    def __init__(self):
        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)     
        self.flann = cv2.FlannBasedMatcher(index_params,search_params)
        self.detector = cv2.DescriptorExtractor_create("SIFT")#ORB() #FastFeatureDetector()#SIFT()     
    def process(self):
        img1 = cv2.cvtColor(self.imgcv1, cv2.COLOR_BGR2GRAY)  #queryimage # left image
        img2 = cv2.cvtColor(self.imgcv2, cv2.COLOR_BGR2GRAY)  #trainimage # right image
        # find the keypoints and descriptors with SIFT
        kp1, des1 = self.detector.detectAndCompute(img1,None)
        kp2, des2 = self.detector.detectAndCompute(img2,None)      
        matches = self.flann.knnMatch(des1,des2,k=2)       
        pts1 = []
        pts2 = []        
        # ratio test as per Lowe's paper
        for i,(m,n) in enumerate(matches):
            if m.distance < 0.8*n.distance:
                pts2.append(kp2[m.trainIdx].pt)
                pts1.append(kp1[m.queryIdx].pt)
        pts1 = np.float32(pts1)
        pts2 = np.float32(pts2)
        F, mask = cv2.findFundamentalMat(pts1,pts2,cv2.RANSAC)     
        # We select only inlier points
        pts1 = pts1[mask.ravel()==1]
        pts2 = pts2[mask.ravel()==1]
        self.data=(F,pts1,pts2)
        pts1i=np.int32(pts1)
        pts2i=np.int32(pts2)
        return drawpoints(img1,img2,pts1i,pts2i)
class HomographyMatrix():
    def __init__(self):
        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)     
        self.flann = cv2.FlannBasedMatcher(index_params,search_params)
        self.detector = cv2.FastFeatureDetector()#.SIFT()     
    def process(self):
        img1 = cv2.cvtColor(self.imgcv1, cv2.COLOR_BGR2GRAY)  #queryimage # left image
        img2 = cv2.cvtColor(self.imgcv2, cv2.COLOR_BGR2GRAY)  #trainimage # right image
        # find the keypoints and descriptors with SIFT
        kp1, des1 = self.detector.detectAndCompute(img1,None)
        kp2, des2 = self.detector.detectAndCompute(img2,None)      
        matches = self.flann.knnMatch(des1,des2,k=2)       
        pts1 = []
        pts2 = []        
        # ratio test as per Lowe's paper
        for i,(m,n) in enumerate(matches):
            if m.distance < 0.8*n.distance:
                pts2.append(kp2[m.trainIdx].pt)
                pts1.append(kp1[m.queryIdx].pt)
        pts1 = np.float32(pts1)
        pts2 = np.float32(pts2)
        M, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC,5.0)
        h,w = img1.shape
        h/=2
        w/=2
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)
        cv2.polylines(img2,[np.int32(dst)],True,255,3)
        #We select only inlier points
        pts1 = pts1[mask.ravel()==1]
        pts2 = pts2[mask.ravel()==1]
        self.data=(M,pts1,pts2)
        pts1i=np.int32(pts1)
        pts2i=np.int32(pts2)
        return drawpoints(img1,img2,pts1i,pts2i)
class Camera():
    def __init__(self,K,dist=None,rvec=None,tvec=None):
        self.rvec=rvec
        self.tvec=tvec
        self.K=K
        self.dist=dist
    def project3DPoints(self,pts3D):
        imgPts, jacobian=cv2.projectPoints(pts3D, self.rvec, self.tvec, self.K, self.dist)
        return imgPts
    def undistort(self,imgcv):
        u=Undistor(self.k,self.dist)
        return u.process(imgcv)
class PespectiveMatrix():
    def __init__(self,src,dst):
        self.src=src
        self.dst=dst
        self.M=cv2.getPerspectiveTransform(src,dst)
        self.Minv = cv2.getPerspectiveTransform(dst, src)
    def transform(self,src):
        dst=cv2.perspectiveTransform(src, self.M)
        return dst
    def transformInv(self,src):
        dst=cv2.perspectiveTransform(src, self.Minv)
        return dst
    def warp(self,imgcv):
        img_size=(imgcv.shape[1],imgcv.shape[0])
        warped = cv2.warpPerspective(imgcv, self.M, img_size, flags=cv2.INTER_LINEAR)
        return warped
    def warpInv(self,imgcv):
        img_size=(imgcv.shape[1],imgcv.shape[0])
        warped = cv2.warpPerspective(imgcv, self.Minv, img_size, flags=cv2.INTER_LINEAR)
        return warped
class PerspectiveWarp():
    def __init__(self,perspectiveMatrix):
        self.M=perspectiveMatrix.M
        self.Minv=perspectiveMatrix.Minv
        self.inv=False
    def process(self,imgcv):
        img_size=(imgcv.shape[1],imgcv.shape[0])
        if self.inv:
            M=self.M
        else:
            M=self.minval
        warped = cv2.warpPerspective(imgcv, M, img_size, flags=cv2.INTER_LINEAR)
        return warped
                    
class HistogramColor():
    def __init__(self):
        pass
    def process(self,img):
        h = np.zeros((300,256,3))
        bins = np.arange(256).reshape(256,1)
        color = [(0,0,255),(255,0,0),(0,255,0)]
        hbgr=cv2.calcHist([img],[0,1,2],None,[256,256,256],[0,256,0,256,0,256])
        maxH=np.max(hbgr)
        for ch, col in enumerate(color):
            hist_item = cv2.calcHist([img],[ch],None,[256],[0,256])
            cv2.normalize(hist_item,hist_item,0,maxH,cv2.NORM_MINMAX)
            hist=np.int32(np.around(hist_item))
            pts = np.column_stack((bins,hist))
            cv2.polylines(h,[pts],False,col)
        h=np.uint8(np.flipud(h))
        return h
    
#Two images filter
class MixImages():
    def __init__(self):
        self.factor=0.5
        self.imgcv1=None
        self.imgcv2=None
    def process(self):
        return cv2.addWeighted(self.imgcv1,self.factor,self.imgcv2,1.0-self.factor,0)
