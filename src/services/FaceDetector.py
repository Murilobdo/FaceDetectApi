import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PIL import Image
from ultralytics import YOLO
import os



class FaceDetector:
    def __init__(self, image):
        self.result = False
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
            
            if(qtd == 1):
                self.result = True
            else:
                self.result = False
        
        return self.result
    
    def yoloDetect(self):
        model = YOLO('yolov8n.pt')
        results = model(self.image)
        detections = []
        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])  # Índice da classe detectada
                conf = box.conf[0].item()  # Confiança da detecção
                bbox = box.xyxy[0].tolist()  # Coordenadas do bounding box [xmin, ymin, xmax, ymax]
                
                if cls == 15:  # Exemplo: o índice 15 pode ser "sunglasses" no seu modelo
                    detections.append({
                        "class": cls,
                        "confidence": conf,
                        "bbox": bbox
                    })
                    
        if(len(detections) == 0):
            self.result = f'Foto validada com sucesso'
        else:
            self.result = 'Foto obstruida'
            
