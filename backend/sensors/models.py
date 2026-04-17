from django.db import models
from gateways.models import Gateway

# Create your models here.
class Sensor(models.Model):
    """传感器模型"""

    SENSOR_STATUS = (
        ('online', '在线'),
        ('offline', '离线'),
        ('fault', '故障')
    )

    name = models.CharField(max_length=30, verbose_name='传感器名称')
    device_id = models.CharField(max_length=50, unique=True, verbose_name='设备ID')
    gateway = models.ForeignKey(Gateway, on_delete=models.CASCADE, related_name='sensors', verbose_name='所属网关')
    status = models.CharField(max_length=10, choices=SENSOR_STATUS, default='offline', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='安装日期')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return f"{self.name} ({self.device_id}) ({self.sensor_type})"



