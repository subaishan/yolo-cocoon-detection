from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PestDetectionRecord(models.Model):
    """病虫害检测记录"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pestdetectionrecord")
    created_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='待处理')
    original_image = models.ImageField(
        upload_to='pest_detection/original/'
    )
    processed_image = models.ImageField(
        upload_to='pest_detection/processed_image',
        null=True, blank=True
    )
    detection_data = models.JSONField(default=dict)
    detection_count = models.IntegerField(default=0)
    processing_time = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']
