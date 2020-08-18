'''
Created on 16 Aug 2020

@author: Francisco Dominguez Mateos
'''
import cv2
#python 3
#import xmlrpc.client
#python 2.7
import xmlrpclib

class DetectorRemote():
    def __init__(self,url="http://localhost:9000/"):
        #python 3
        #self.proxy = xmlrpc.client.ServerProxy(url)
        #python 2.7
        self.proxy = xmlrpclib.ServerProxy(url)
        self.labels=self.proxy.getLabels()
    def detect(self,cvImage):
        detection=[]
        cv2.imwrite("detector_remote_temp.jpg",cvImage)
        with open("detector_remote_temp.jpg", "rb") as handle:
            #print(proxy.detect(xmlrpc.client.Binary(handle.read())))
            #Binary Image (this is python 2.7)
            bi=xmlrpclib.Binary(handle.read())
            try:
                detection=self.proxy.detect(bi)
            except Exception() as rnr:
                print("error xml:",rnr)
                #detection=self.proxy.detect(bi)                
            return detection
