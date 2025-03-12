from django.db import models
from django.utils import timezone
# โมเดล JujubeImage สำหรับจัดเก็บข้อมูลภาพ
class JujubeImage(models.Model):
    jujube_image = models.ImageField(upload_to='images/',null=True)
    upload_date = models.DateTimeField(default=timezone.now,primary_key=True)
    detected_image = models.ImageField(upload_to='detected_image/',null=True)
    def __str__(self):
        return f"Image {self.jujube_image} uploaded on {self.upload_date}"

# โมเดล YoloDetectionModel สำหรับเก็บข้อมูลโมเดลที่ใช้ในการตรวจจับ
class YoloDetectionModel(models.Model):
    model_name = models.CharField(max_length=100, unique=True)
    model_file = models.FileField(upload_to='yolo_models/')
    def __str__(self):
        return f"Model: {self.model_name}"

# โมเดล DetectionResult สำหรับเก็บผลลัพธ์ของการตรวจจับ
class DetectionResult(models.Model):
    counter = models.PositiveIntegerField(null=True)
    width_cm = models.FloatField(null=True)
    height_cm = models.FloatField(null=True)
    width_pixel = models.PositiveIntegerField(null=True)
    height_pixel = models.PositiveIntegerField(null=True)
    ref_width_pixel = models.PositiveIntegerField(null=True)
    ref_height_pixel = models.PositiveIntegerField(null=True)
    x1 = models.PositiveIntegerField(null=True)
    y1 = models.PositiveIntegerField(null=True)
    x2 = models.PositiveIntegerField(null=True)
    y2 = models.PositiveIntegerField(null=True)
    dummy_class_name = models.PositiveIntegerField(null=True)
    jujubeimage = models.ForeignKey(JujubeImage, on_delete=models.CASCADE, to_field="upload_date", unique=False, null=False, blank=False)
   
    def __str__(self):
        return f"DetectionResult {self.id} for image {self.jujubeimage.upload_date}"

# โมเดล PredictionResult สำหรับเก็บผลลัพธ์จากการทำนาย
class PredictionResult(models.Model):
    weight_gram = models.FloatField(max_length=3, null=True)
    detectionresult = models.OneToOneField(DetectionResult, on_delete=models.CASCADE, null=False, unique=True)

    def __str__(self):
        return f"PredictionResult {self.id} for DetectionResult {self.detectionresult.id}"
