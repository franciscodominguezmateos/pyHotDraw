'''
Created on 14 Mar 2018

@author: Francisco Dominguez
'''
import cv2
import keras
from keras.applications.imagenet_utils import preprocess_input
from keras.backend.tensorflow_backend import set_session
from keras.models import Model
from keras.preprocessing import image
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import imread
import tensorflow as tf

from ssd import SSD300
from ssd_utils import BBoxUtility

class Detector(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.labels=[]
    def detect(self,cvImage):
        pass
        
'''
from: https://github.com/rykov8/ssd_keras
dependences: `Keras` v1.2.2, `Tensorflow` v1.0.0, `OpenCV` v3.1.0-dev
'''
class DetectorSSD(Detector):
    def __init__(self,path_weights="/home/francisco/git/ssd_keras/weights_SSD300.hdf5"):
        config = tf.ConfigProto()
        config.gpu_options.per_process_gpu_memory_fraction = 0.45
        set_session(tf.Session(config=config))
        
        self.labels = ['Aeroplane', 'Bicycle', 'Bird', 'Boat', 'Bottle',
                       'Bus', 'Car', 'Cat', 'Chair', 'Cow', 'Diningtable',
                       'Dog', 'Horse','Motorbike', 'Person', 'Pottedplant',
                       'Sheep', 'Sofa', 'Train', 'Tvmonitor']
        NUM_CLASSES = len(self.labels) + 1
        
        input_shape=(300, 300, 3)
        # Get detections with confidence higher than 0.6.
        self.detection_confidence=0.6
        self.model = SSD300(input_shape, num_classes=NUM_CLASSES)
        self.model.load_weights(path_weights, by_name=True)
        self.bbox_util = BBoxUtility(NUM_CLASSES)
        self.detections=[]
        
    def detect(self,cvImage):
        inputs = []
        images = []
        cvImage=cv2.cvtColor(cvImage,cv2.COLOR_BGR2RGB)
        img=cv2.resize(cvImage, (300,300))
        images.append(cvImage)
        inputs.append(img.copy().astype(np.float))
        inputs = preprocess_input(np.array(inputs))
        preds = self.model.predict(inputs, batch_size=1, verbose=0)
        results = self.bbox_util.detection_out(preds)

        for i, img in enumerate(images):
            # Parse the outputs.
            det_label = results[i][:, 0]
            det_conf = results[i][:, 1]
            det_xmin = results[i][:, 2]
            det_ymin = results[i][:, 3]
            det_xmax = results[i][:, 4]
            det_ymax = results[i][:, 5]
        
            # Get detections with confidence higher than 0.6.
            top_indices = [i for i, conf in enumerate(det_conf) if conf >= self.detection_confidence]
        
            top_conf = det_conf[top_indices]
            top_label_indices = det_label[top_indices].tolist()
            top_xmin = det_xmin[top_indices]
            top_ymin = det_ymin[top_indices]
            top_xmax = det_xmax[top_indices]
            top_ymax = det_ymax[top_indices]
                
            self.detections=[]
            for i in range(top_conf.shape[0]):
                xmin = int(round(top_xmin[i] * img.shape[1]))
                ymin = int(round(top_ymin[i] * img.shape[0]))
                xmax = int(round(top_xmax[i] * img.shape[1]))
                ymax = int(round(top_ymax[i] * img.shape[0]))
                score = float(top_conf[i])
                label = int(top_label_indices[i])
                self.detections.append([label,score,xmin,ymin,xmax,ymax])         
        return self.detections
    

        