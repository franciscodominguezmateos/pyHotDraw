#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 25/04/2015

@author: Francisco Dominguez
+03/02/2016
'''
import glob
import numpy as np
from math import sqrt
import cv2
import dlib
from pip._vendor.distlib import DistlibException
from pip._vendor import distlib
from __builtin__ import False

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
class GoodFeaturesToTrack():
    def __init__(self):
        # params for ShiTomasi corner detection
        self.feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
        # Create some random colors
        self.color = np.random.randint(0,255,(100,3))
    def process(self,imgcv):
        gray = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
        p = cv2.goodFeaturesToTrack(gray, mask = None, **self.feature_params)
        self.pts=p.reshape(-1,2)
        ret=imgcv.copy()
        for i,pt in enumerate(self.pts):
            cv2.circle(ret,tuple(pt),5,self.color[i].tolist(),-1)
        return ret
    def getPoints(self):
        return self.pts       
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
# TODO usign dlib face shape detector
class FaceShapeDetection():
    def __init__(self):
        # These files must be on the same folder of the .py source where this class is used source
        self.predictor_path="shape_predictor_68_face_landmarks.dat"
        face_rec_model_path="dlib_face_recognition_resnet_model_v1.dat"
        detector_path="mmod_human_face_detector.dat"
        #self.detector = dlib.get_frontal_face_detector()
        self.detector = dlib.cnn_face_detection_model_v1(detector_path)
        self.sp       = dlib.shape_predictor(self.predictor_path)
        self.facerec  = dlib.face_recognition_model_v1(face_rec_model_path)
        self.detections=None
        self.shapes=[]
        self.descriptors=[]
        #from https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/    
    def shape_to_np(self,shape, dtype="int"):
        # initialize the list of (x, y)-coordinates
        coords = np.zeros((68, 2), dtype=dtype)
        # loop over the 68 facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        # return the list of (x, y)-coordinates
        return coords
    
    def draw_shape(self,image,shape):
            # loop over the (x, y)-coordinates for the facial landmarks
        # and draw them on the image
        for (x, y) in shape:
            cv2.circle(image, (x, y), 3, (0, 0, 255), 2)
        for i,(x,y) in enumerate(shape[:16]):
            x1,y1=shape[i+1]
            cv2.line(image,(x,y),(x1,y1),(255,255,0),2)
        # left eyebrow
        for i,(x,y) in enumerate(shape[17:21]):
            x1,y1=shape[17+i+1]
            cv2.line(image,(x,y),(x1,y1),(255,255,0),2)
        # right eyebrow
        for i,(x,y) in enumerate(shape[22:26]):
            x1,y1=shape[22+i+1]
            cv2.line(image,(x,y),(x1,y1),(255,255,0),2)
        # nose
        for i,(x,y) in enumerate(shape[27:30]):
            x1,y1=shape[27+i+1]
            cv2.line(image,(x,y),(x1,y1),(255,255,0),2)
        for i,(x,y) in enumerate(shape[31:35]):
            x1,y1=shape[31+i+1]
            cv2.line(image,(x,y),(x1,y1),(255,255,0),2)
        # left eye
        for i,(x,y) in enumerate(shape[36:41]):
            x1,y1=shape[36+i+1]
            cv2.line(image,(x,y),(x1,y1),(255,255,0),2)
        x,y=shape[36]
        cv2.line(image,(x1,y1),(x,y),(255,255,0),2)
        # right eye
        for i,(x,y) in enumerate(shape[42:47]):
            x1,y1=shape[42+i+1]
            cv2.line(image,(x,y),(x1,y1),(255,255,0),2)
        x,y=shape[42]
        cv2.line(image,(x1,y1),(x,y),(255,255,0),2)
        # mouth
        # upper lip
        for i,(x,y) in enumerate(shape[48:59]):
            x1,y1=shape[48+i+1]
            cv2.line(image,(x,y),(x1,y1),(255,255,0),2)
        x,y=shape[48]
        cv2.line(image,(x1,y1),(x,y),(255,255,0),2)
        # lower lip
        for i,(x,y) in enumerate(shape[60:67]):
            x1,y1=shape[60+i+1]
            cv2.line(image,(x,y),(x1,y1),(255,0,255),2)
        x,y=shape[60]
        cv2.line(image,(x1,y1),(x,y),(255,0,255),2)
        return image  
    def process(self,frameI):
        img=cv2.cvtColor(frameI, cv2.COLOR_BGR2RGB)
        #Face detection
        self.detections = self.detector(img, 1)
        #print("Number of faces detected: {}".format(len(dets)))
        # Now process each face we found.
        self.shapes=[]
        self.descriptors=[]
        for k, d in enumerate(self.detections):
            dr=d.rect
            #print center_row,center_col,center_row_g,center_col_g
            #print center_row_g,center_col_g
            # Get the landmarks/parts for the face in box d.
            shape_dlib = self.sp(img, dr)
            shape=self.shape_to_np(shape_dlib)
            # Draw the face landmarks on the screen so we can see what face is currently being processed.
            #win.clear_overlay()
            face_descriptor = np.array(self.facerec.compute_face_descriptor(img, shape_dlib))
            self.descriptors.append(face_descriptor)
            self.shapes.append(shape)
            self.draw_shape(img,shape)
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    def getShapes(self):
        return self.shapes
    def getDetections(self):
        return self.detections
    def getDescriptors(self):
        return self.descriptors
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
        if self.prvs is None:
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

#01/08/2020 TO FINISH
class OpticalFlowPyrLK():
    def __init__(self):
        self.p0=np.zeros((1,2))
        self.old_gray=None
        # Parameters for lucas kanade optical flow
        self.lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        # params for ShiTomasi corner detection
        self.feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
        # Create some random colors
        self.color = np.random.randint(0,255,(100,3))
        self.gft=GoodFeaturesToTrack()
        self.minFeatures=20
        
    def process(self,imgcv):
        frame_gray = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
        frame=imgcv.copy()
        if self.p0.shape[0]<self.minFeatures:
            img=self.gft.process(imgcv)
            self.p0=self.gft.getPoints()
            self.old_gray=frame_gray
            # Create a mask image for drawing purposes
            self.mask = np.zeros_like(imgcv)
        else:
            # calculate optical flow
            p1, st, _ = cv2.calcOpticalFlowPyrLK(self.old_gray, frame_gray, self.p0, None, **self.lk_params)
            st=st.reshape(-1,)
        
            # Select good points
            good_new = p1[st==1]
            good_old = self.p0[st==1]
        
            # draw the tracks
            for i,(new,old) in enumerate(zip(good_new,good_old)):
                a,b = new.ravel()
                c,d = old.ravel()
                self.mask = cv2.line(self.mask, (a,b),(c,d), self.color[i].tolist(), 2)
                frame = cv2.circle(frame,(a,b),5,self.color[i].tolist(),-1)
                # Now update the previous frame and previous points
            self.old_gray = frame_gray.copy()
            self.p0 = good_new.reshape(-1,1,2)

            img = cv2.add(frame,self.mask)
        return img

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
    gap=32
    for i in range(out.shape[0]/gap):
        cv2.line(out,(0,i*gap), (out.shape[1],i*gap),(255,0,0),1)
    for i in range(out.shape[1]/gap*2):
        cv2.line(out,(i*gap,0), (i*gap,out.shape[0]),(255,0,0),1)
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
        #self.detector = cv2.SIFT()#cv2.FastFeatureDetector()#sSIFT()  
        minHessian = 400
        self.detector = cv2.xfeatures2d_SURF.create(hessianThreshold=minHessian)   
        self.imgcv1=None
        self.imgcv2=None
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
        minHessian = 400
        self.detector = cv2.xfeatures2d_SURF.create(hessianThreshold=minHessian)     
        self.imgcv1=None
        self.imgcv2=None
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
class FundamentalMatrixStereo():
    def __init__(self):
        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)     
        self.flann = cv2.FlannBasedMatcher(index_params,search_params)
        minHessian = 400
        self.detector = cv2.xfeatures2d_SURF.create(hessianThreshold=minHessian)     
        self.imgcv1=None
        self.imgcv2=None
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
        l=pts1.shape[0]
        mask=np.array([True]*l)
        for i in range(l):
            x1,y1=pts1[i]
            x2,y2=pts2[i]
            if abs(y2-y1)>2: # or abs(y2-y1)<3:
                mask[i]=False
        pts1=pts1[mask]
        pts2=pts2[mask]
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
        self.imgcv1=None
        self.imgcv2=None
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
class Undistorter():
    def __init__(self,mtx,dist):
        self.mtx=mtx
        self.dist=dist
        self.mtxO=mtx
    def process(self,imgcv):
        ret= cv2.undistort(imgcv, self.mtx, self.dist, None, self.mtxO)
        return ret
class Rectify():
    def __init__(self,mtxL,distL,mtxR,distR,R,T,left=True):
        self.left=left
        rectify_scale = 1 # 0=full crop, 1=no crop
        R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(mtxL, distL, mtxR, distR, (640, 480), R, T, alpha = rectify_scale)
        self.left_maps  = cv2.initUndistortRectifyMap(mtxL, distL, R1, P1, (640, 480), cv2.CV_16SC2)
        self.right_maps = cv2.initUndistortRectifyMap(mtxR, distR, R2, P2, (640, 480), cv2.CV_16SC2)
    def process(self,imgcv):
        if self.left:
            return cv2.remap(imgcv, self.left_maps[0], self.left_maps[1], cv2.INTER_LANCZOS4)
        else:
            return cv2.remap(imgcv, self.right_maps[0], self.right_maps[1], cv2.INTER_LANCZOS4)
class Camera():
    def __init__(self,K,dist=None,rvec=None,tvec=None):
        self.rvec=rvec
        self.tvec=tvec
        self.K=K
        self.dist=dist
        self.u=Undistorter(self.k,self.dist)
    def project3DPoints(self,pts3D):
        imgPts, jacobian=cv2.projectPoints(pts3D, self.rvec, self.tvec, self.K, self.dist)
        return imgPts
    def undistort(self,imgcv):
        return self.u.process(imgcv)
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
    
# Stereo Filters
# Take a picture with two images
# return the left one
class StereoSplitLeft():
    def __init__(self):
        pass
    def process(self,img):
        h,w,c=img.shape
        w2=w/2
        return img[:,0:w2]
# Take a picture with two images
# return the right one
class StereoSplitRight():
    def __init__(self):
        pass
    def process(self,img):
        h,w,c=img.shape
        w2=w/2
        return img[:,w2+1:]
# TASKS
# Calibrate
# Load / save calibrarted data
# Rectify
# 
class StereoCamera():
    def __init__(self):
        pass
    def setCalibrationData(self,KL,distL,KR,distR,R,T,E,F):
        imgSize=(640,480)
        self.KL=KL
        self.distL=distL
        self.KR=KR
        self.distR=distR
        self.R=R
        self.T=T
        self.E=E
        self.F=F
        rectify_scale = 0 # 0=full crop, 1=no crop
        self.R1, self.R2, self.P1, self.P2, self.Q, self.roi1, self.roi2 = cv2.stereoRectify(KL, distL, KR, distR, imgSize, R, T, alpha = rectify_scale)
        self.left_maps  = cv2.initUndistortRectifyMap(KL, distL, self.R1, self.P1, imgSize, cv2.CV_16SC2)
        self.right_maps = cv2.initUndistortRectifyMap(KR, distR, self.R2, self.P2, imgSize, cv2.CV_16SC2)
    def calibrate(self, cal_path):
        images_right = glob.glob(cal_path + '/right/*.jpg')
        images_left = glob.glob(cal_path + '/left/*.jpg')
        images_left.sort()
        images_right.sort()
        
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.cw=9 #9
        self.ch=6 #6
        square_size=24 #22.23 # mm
        self.objp = np.zeros((self.ch*self.cw, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:self.cw, 0:self.ch].T.reshape(-1, 2)*square_size

        # Arrays to store object points and image points from all the images.
        self.objpoints = []  # 3d point in real world space
        self.imgpoints_l = []  # 2d points in image plane.
        self.imgpoints_r = []  # 2d points in image plane.

        for i, fname in enumerate(images_right):
            img_l = cv2.imread(images_left[i])
            img_r = cv2.imread(images_right[i])

            gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
            gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret_l, corners_l = cv2.findChessboardCorners(gray_l, (self.cw, self.ch), None)
            ret_r, corners_r = cv2.findChessboardCorners(gray_r, (self.cw, self.ch), None)

            if not ret_l or not ret_r:
                print("Imagen %i no detectada en %s"%(i,fname))
                continue

            # If found, add object points, image points (after refining them)
            self.objpoints.append(self.objp)
            
            rt = cv2.cornerSubPix(gray_l, corners_l, (11, 11),
                                  (-1, -1), self.criteria)
            self.imgpoints_l.append(corners_l)

            # Draw and display the corners
            ret_l = cv2.drawChessboardCorners(img_l, (self.cw, self.ch),
                                              corners_l, ret_l)
            cv2.imshow("left", img_l)

            rt = cv2.cornerSubPix(gray_r, corners_r, (11, 11),
                                  (-1, -1), self.criteria)
            self.imgpoints_r.append(corners_r)

            # Draw and display the corners
            ret_r = cv2.drawChessboardCorners(img_r, (self.cw, self.ch),
                                              corners_r, ret_r)
            cv2.imshow("right", img_r)
            cv2.waitKey(50)

            img_shape = gray_l.shape[::-1]

        self.retL, self.M1, self.d1, self.r1, self.t1 = cv2.calibrateCamera(
            self.objpoints, self.imgpoints_l, img_shape, None, None)
        self.retR, self.M2, self.d2, self.r2, self.t2 = cv2.calibrateCamera(
            self.objpoints, self.imgpoints_r, img_shape, None, None)

        dims=img_shape
        flags = 0
        #flags |= cv2.CALIB_FIX_INTRINSIC
        # flags |= cv2.CALIB_FIX_PRINCIPAL_POINT
        #flags |= cv2.CALIB_USE_INTRINSIC_GUESS
        #flags |= cv2.CALIB_FIX_FOCAL_LENGTH
        # flags |= cv2.CALIB_FIX_ASPECT_RATIO
        flags |= cv2.CALIB_ZERO_TANGENT_DIST
        # flags |= cv2.CALIB_RATIONAL_MODEL
        flags |= cv2.CALIB_SAME_FOCAL_LENGTH
        # flags |= cv2.CALIB_FIX_K3
        # flags |= cv2.CALIB_FIX_K4
        # flags |= cv2.CALIB_FIX_K5

        stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER +
                                cv2.TERM_CRITERIA_EPS, 100, 1e-5)
        self.ret, M1, d1, M2, d2, R, T, E, F = cv2.stereoCalibrate(
            self.objpoints, self.imgpoints_l,
            self.imgpoints_r, self.M1, self.d1, self.M2,
            self.d2, dims,
            criteria=stereocalib_criteria, flags=flags)
        self.setCalibrationData(M1, d1, M2, d2, R, T, E, F)
        
        
# class Rectify():
#     def __init__(self,mtxL,distL,mtxR,distR,R,T,left=True):
#         self.left=left
#         rectify_scale = 0 # 0=full crop, 1=no crop
#         R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(mtxL, distL, mtxR, distR, (640, 480), R, T, alpha = rectify_scale)
#         self.left_maps  = cv2.initUndistortRectifyMap(mtxL, distL, R1, P1, (640, 480), cv2.CV_16SC2)
#         self.right_maps = cv2.initUndistortRectifyMap(mtxR, distR, R2, P2, (640, 480), cv2.CV_16SC2)
#     def process(self,imgcv):
#         if self.left:
#             return cv2.remap(imgcv, self.left_maps[0], self.left_maps[1], cv2.INTER_LANCZOS4)
#         else:
#             return cv2.remap(imgcv, self.right_maps[0], self.right_maps[1], cv2.INTER_LANCZOS4)
# class Camera():
#     def __init__(self,K,dist=None,rvec=None,tvec=None):
#         self.rvec=rvec
#         self.tvec=tvec
#         self.K=K
#         self.dist=dist
#     def project3DPoints(self,pts3D):
#         imgPts, jacobian=cv2.projectPoints(pts3D, self.rvec, self.tvec, self.K, self.dist)
#         return imgPts
#     def undistort(self,imgcv):
#         u=Undistorter(self.k,self.dist)
#         return u.process(imgcv)

    