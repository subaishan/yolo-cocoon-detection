from django.db import models
from sensors.models import Sensor

# Create your models here.
class EnvironmentData(models.Model):
    """环境数据模型"""

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='environment_data', verbose_name='传感器')
    temperature = models.FloatField(null=True, blank=True, verbose_name='温度')
    humidity = models.FloatField(null=True, blank=True, verbose_name='湿度')
    light_intensity = models.FloatField(null=True, blank=True, verbose_name='光照强度')
    co2_concentration = models.FloatField(null=True, blank=True, verbose_name='二氧化碳浓度')
    recorded_at = models.DateTimeField(verbose_name='记录时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['recorded_at']

    def __str__(self):
        return self.id