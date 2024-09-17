import os
import cv2
import imutils
from PIL import Image
import mediapipe as mp
import numpy as np
from glasses_detector import GlassesClassifier
import io

from services.Response import Response

class FaceDetector:
    def __init__(self, image):
        self.result = ''
        self.image = self.loadImage(image)
        self.image_array = np.array(self.image)

    def loadImage(self, image):
        image_bytes = image.read()
        image = Image.open(io.BytesIO(image_bytes))
        image = np.array(image)
        return imutils.resize(image, width=500)
    
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