#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 18/08/2020

@author: Francisco Dominguez
'''
import sys
from threading import Timer

from pyHotDraw.Figures.pyHImageFigure import pyHImageSourceFigure
from pyHotDraw.Figures.pyHTextFigure import pyHTextFigure

import roslib
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class pyHROSCameraFigure(pyHImageSourceFigure):
    def __init__(self,x,y,w=80,h=40,topic="/camera/rgb/image_color",text=" ROS Camera ",width=640,hight=480):
        super(pyHROSCameraFigure,self).__init__(x,y,w,h)
        #pyHImageSourceFigure.__init__(self, x, y, w, h)
        """Initialize camera."""
        self.textFigure=pyHTextFigure(x,y,w,h,text,border=False)
        self.inputConnectionFigure=None
        self.flip=False
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber(topic,Image,self.callback,None,1)
        rospy.init_node('pyHROSCameraFigure', anonymous=True)
        #self.timer = Timer(0.2,self.rosSpin)
        #self.timer.start()

    def draw(self,g):
        super(pyHROSCameraFigure,self).draw(g)
        self.textFigure.setDisplayBox(self.getDisplayBox())
        self.textFigure.draw(g)

    def callback(self,data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
    
#         (rows,cols,channels) = cv_image.shape
#         if cols > 60 and rows > 60 :
#             cv2.line(cv_image, (0,480/4),(640,480/4),(255,0,0), 1)
    
        #cv2.imshow("pyHROSCameraFigure", cv_image)
        #cv2.waitKey(1)

        frame=cv_image
        if(self.flip):
            frame=cv2.flip(frame,0)
        img=self.getImage().getData()
        self.getImagePrev().setData(img)
        self.getImage().setData(frame)
        self.notifyImageChanged()
        
#     def rosSpin(self):
#         """
#         Call rospy.spin() in order to get events from ROS
#         """
#         self.timer = Timer(0.2,self.rosSpin)
#         self.timer.start()
#         rospy.spin()
