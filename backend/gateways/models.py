from django.db import models
from regions.models import Region

# Create your models here.

class Gateway(models.Model):
    """网关模型"""
    GATEWAY_STATUS = (
        ('online', '在线'),
        ('offline', '离线'),
        ('fault', '故障')
    )

    name = models.CharField(max_length=30, verbose_name='网关名称')
    device_id = models.CharField(max_length=50, unique=True, verbose_name='设备ID')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='gateways', verbose_name='所属园区')
    location = models.CharField(max_length=100, verbose_name='安装位置')
    status = models.CharField(max_length=10, choices=GATEWAY_STATUS, default='offline', verbose_name='状态')
    last_heartbeat = models.DateTimeField(null=True, blank=True, verbose_name='最后心跳时间')
    installed_at = models.DateTimeField(auto_now_add=True, verbose_name='安装时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['region']

    # def __str__(self):
    #     return f"{self.name} ({self.device_id})"
    

