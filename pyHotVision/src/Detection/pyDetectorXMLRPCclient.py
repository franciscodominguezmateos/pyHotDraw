'''
Created on 8 Jul 2018

@author: francisco
'''
import xmlrpc.client
import time
import colorsys
import cv2

class DetectorRemote():
    def __init__(self,url="http://localhost:9000/"):
        self.proxy = xmlrpc.client.ServerProxy(url)
        self.labels=self.proxy.getLabels()
    def detect(self,cvImage):
        cv2.imwrite("detector_remote_temp.jpg",cvImage)
        with open("detector_remote_temp.jpg", "rb") as handle:
            #print(proxy.detect(xmlrpc.client.Binary(handle.read())))
            detection=self.proxy.detect(handle.read())
            return detection

def HSVToRGB(h, s, v):
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
    return (int(255*r), int(255*g), int(255*b))
 
def getDistinctColors(n):
    huePartition = 1.0 / (n + 1)
    return [HSVToRGB(huePartition * value, 1.0, 1.0) for value in range(0, n)]

ssd=DetectorRemote()
colors=getDistinctColors(len(ssd.labels))

#img=cv2.imread("/home/francisco/git/ssd_keras/pics/car_cat2.jpg")
capture = cv2.VideoCapture(0)
#capture = cv2.VideoCapture("http://192.168.100.15:8080/video")
while True:
    rc,img = capture.read()
    if not rc:
        continue
    for label,score,xmin,ymin,xmax,ymax in ssd.detect(img):
        label_name = ssd.labels[label - 1]
        display_txt = '{:0.2f}, {}'.format(score, label_name)
        color = colors[label-1]
        cv2.putText(img,display_txt,(xmin,ymin-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,color)
        cv2.rectangle(img,(xmin,ymin),(xmax,ymax),color,1)
    cv2.imshow("DetectorSSD",img)
    if cv2.waitKey(1)==27:
        break

