import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PIL import Image
from ultralytics import YOLO
import matplotlib.pyplot as plt
import matplotlib.image as imgplt
import os
import cv2
import random
from glasses_detector import GlassesClassifier, GlassesDetector

class FaceDetector:
    def __init__(self, image):
        self.result = ''
        self.image = np.array(Image.open(image))
        
    def detect(self):
        BaseOptions = mp.tasks.BaseOptions
        FaceDetector = mp.tasks.vision.FaceDetector
        FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
        VisionRunningMode = mp.tasks.vision.RunningMode
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.normpath(os.path.join(current_dir, '../models/blaze_face_short_range.tflite'))

        options = FaceDetectorOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.IMAGE)

        with FaceDetector.create_from_options(options) as detector:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=self.image)
            detection_result = detector.detect(mp_image)
            
            qtd = len(detection_result.detections)
   
            _ = GlassesClassifier(kind='anyglasses')
            predictGlasses = _.predict(self.image)
                
            if(qtd == 1 and predictGlasses == 'absent'):
                self.result = 'Foto Validada com Sucesso'
            elif(qtd == 1 and predictGlasses == 'present'):
                self.result = 'Foto com Óculos'
            else:
                self.result = 'Nenhuma pessoa foi reconhecida na foto'
        
        return self.result

   
            
