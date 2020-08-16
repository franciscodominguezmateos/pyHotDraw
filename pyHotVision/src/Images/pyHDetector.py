'''
Created on 16 Aug 2020

@author: Francisco Dominguez Mateos
'''
import cv2
import colorsys
#this doesn't seem to work for kind of cuda context problem
#from Detection.pyDetector import DetectorSSD
from Detection.pyDetectorRemote import DetectorRemote

class pyHDetector():
    def __init__(self,detector=DetectorRemote()):
        self.detector=detector
        self.colors=self.getDistinctColors(len(self.detector.labels))
    
    def HSVToRGB(self,h, s, v):
        (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
        return (int(255*r), int(255*g), int(255*b))
     
    def getDistinctColors(self,n):
        huePartition = 1.0 / (n + 1)
        return [self.HSVToRGB(huePartition * value, 1.0, 1.0) for value in range(0, n)]
    
    def process(self,img):
        img=img.copy()
        self.data=self.detector.detect(img)
        for label,score,xmin,ymin,xmax,ymax in self.data:
            label_name = self.detector.labels[label - 1]
            display_txt = '{:0.2f}, {}'.format(score, label_name)
            color = self.colors[label-1]
            cv2.putText(img,display_txt,(xmin,ymin-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,color)
            cv2.rectangle(img,(xmin,ymin),(xmax,ymax),color,1)
            return img
