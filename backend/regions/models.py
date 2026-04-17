from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Region(models.Model):
    """园区模型"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="region_manager")
    name = models.CharField(max_length=100, verbose_name='园区名称')
    location = models.CharField(max_length=100, verbose_name='位置')
    area = models.FloatField(verbose_name='面积')
    description = models.TextField(blank=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return super().__str__()
