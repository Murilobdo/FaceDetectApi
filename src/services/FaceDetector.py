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
import imutils
from glasses_detector import GlassesClassifier, GlassesDetector

from services.Response import Response

class FaceDetector:
    def __init__(self, image):
        self.result = ''
        self.image = imutils.resize(cv2.imread(image), width=400)
        self.image_array = np.array(self.image)
        # self.image_gray = self.convert_to_grayscale(self.image_array)
        
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
            
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=self.image_array)
            detection_result = detector.detect(mp_image)
            
            qtd = len(detection_result.detections)
   
            _ = GlassesClassifier(kind='anyglasses')
            predictGlasses = _.predict(self.image_array, format='int')
                
            if(qtd != 1):
                return Response('Ajuste bem o seu rosto na camera', False)

            if(predictGlasses == 1):
                return Response('Aproxime-se da câmera e remova possíveis objetos do rosto, e fique em um lugar bem iluminado.', False)

            return Response('Foto Validada com Sucesso', True)

    def convert_to_grayscale(self, image_array):
        if len(image_array.shape) == 2:
            return image_array
        elif len(image_array.shape) == 3:
            if image_array.shape[2] == 3:
                # Imagem RGB
                return np.array(self.image.convert('L'))
            elif image_array.shape[2] == 4:
                # Imagem RGBA
                return np.array(self.image.convert('L'))
            else:
                raise ValueError("Formato de imagem desconhecido")
     

            
