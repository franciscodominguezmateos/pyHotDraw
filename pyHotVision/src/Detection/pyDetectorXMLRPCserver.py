'''
Created on 8 Jul 2018

@author: Francisco Dominguez
'''
import random
import colorsys
import cv2
from pyDetector import DetectorSSD

#python 3
#import xmlrpc.client
#from xmlrpc.server import SimpleXMLRPCServer
#from xmlrpc.server import SimpleXMLRPCRequestHandler

#python 2.7
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer


ssd=DetectorSSD()

def detect(binaryJPEG):
    with open("fetched_python_logo.jpg", "wb") as handle:
        handle.write(binaryJPEG.data)
    img=img=cv2.imread("fetched_python_logo.jpg")
    detections=ssd.detect(img)
    return detections
def getLabels():
    return ssd.labels

server=SimpleXMLRPCServer(('localhost',9000))
server.register_function(detect)
server.register_function(getLabels)
print("Waiting images to detect")
server.serve_forever()

