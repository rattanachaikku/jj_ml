from django.contrib import admin

# Register your models here.
from .models import JujubeImage, PredictionResult, DetectionResult, YoloDetectionModel 
# from .models import DetectedImage

admin.site.register(JujubeImage)

admin.site.register(PredictionResult)


admin.site.register(DetectionResult)
# admin.site.register(DetectedImage)

admin.site.register(YoloDetectionModel)