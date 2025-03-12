from django.conf import settings
from ultralytics import YOLO
import os

from .models import YoloDetectionModel

def load_yolo_model(model_name):
    # ดึง instance ของ YoloDetectionModel
    yolo_model = YoloDetectionModel.objects.get(model_name=model_name)
    
    # รับ path ของไฟล์โมเดล
    model_path = os.path.join(settings.MEDIA_ROOT, yolo_model.model_file.name)
    print(model_path)
    # โหลดโมเดล
    model = YOLO(model_path)
    
    return model