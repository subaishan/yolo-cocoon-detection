# 使用部署了CDet-YOLO的API进行判定

from datetime import datetime
from django.conf import settings
from django.core.cache import cache

import requests
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework.exceptions import APIException
from django.conf import settings
from rest_framework import status
from django.core.files.uploadedfile import UploadedFile
from pathlib import Path
from .models import PestDetectionRecord
import json
import base64
from io import BytesIO
from PIL import Image

class CDetYoloClient:

    def __init__(self, BASE_URL=settings.IMAGEDETECTION_BASE_URL):
        self.BASE_URL = BASE_URL

        self.detect_url  = f"{self.BASE_URL}/detect/"
        self.detect_raw_url = f"{self.BASE_URL}/detect/detect-raw/"
        self.health_url = f"{self.BASE_URL}/health/"
        self.model_info = f"{self.BASE_URL}/model-info/"
        self.gpu_status = f"{self.BASE_URL}/gpu-status/"

    def check_health(self):
        """检查API服务健康状态"""
        try:
            response = requests.get(self.health_url, timeout=10)
            return response.status_code == status.HTTP_200_OK
        except requests.exceptions.RequestException:
            return False
        
    def get_gpu_status(self):
        """获取GUP状态信息

        Returns:
            response: http响应
        """
        try:
            response = requests.get(self.gpu_status, timeout=10)
            if response.status_code == status.HTTP_200_OK:
                return response.json()
        except requests.exceptions.RequestException as e:
            return Exception(f"获取GPU信息失败: {str(e)}")
    
    def get_model_info(self):
        """获取模型信息"""
        try:
            response = requests.get(self.model_info_url, timeout=10)
            if response.status_code == status.HTTP_200_OK:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            raise Exception(f"获取模型信息失败: {str(e)}")

    def get_detect_response(self, request):
        """
        获取检测响应 - 处理前端上传的图片
        
        Args:
            request: Django request对象,包含上传的图片
            
        Returns:
            dict: 包含检测结果或错误信息
        """
        # 检查服务是否可用
        if not self.check_health():
            raise APIException({'errors': '检测服务不可用，请稍后重试'})
        
        # 检查是否有上传的图片
        if 'original_image' not in request.FILES:
            return {
                'success': False,
                'error': '请上传图片文件',
                'status_code': status.HTTP_400_BAD_REQUEST
            }
        
        original_image = request.FILES['original_image']
        
        # 验证文件类型
        if not original_image.content_type.startswith('image/'):
            return {
                'success': False,
                'error': '请上传图片文件(JPEG、PNG等)',
                'status_code': status.HTTP_400_BAD_REQUEST
            }
        
        # 验证文件大小
        if original_image.size > 10 * 1024 * 1024:
            return {
                'success': False,
                'error': '图片大小不能超过10MB',
                'status_code': status.HTTP_400_BAD_REQUEST
            }
        
        try:
            # 调用YOLO检测API
            files = {'original_image': original_image}

            response = requests.post(self.detect_url, files=files, timeout=30)
            
            if response.status_code == status.HTTP_200_OK:
                
                result = response.json()

                with transaction.atomic():
                    while True:
                        original_image_filename = f"original_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                        processed_image_filename = f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                        original_image.seek(0)
                        original_image_io = original_image.read()
                        processed_image_io = self.decode_processed_image(result['processed_image'])
                        pestDetectionRecord = PestDetectionRecord.objects.create(
                            user=request.user,
                            status='已处理',
                            original_image=ContentFile(original_image_io, name=original_image_filename),
                            processed_image=ContentFile(processed_image_io.getvalue(), name=processed_image_filename),
                            detection_data=result['detections'],
                            detection_count=result['detection_count'],
                            processing_time=result['processing_time'],
                        )

                        result = {
                            'detection_data': result['detections'],
                            'detection_count': result['detection_count'],
                            'processing_time': result['processing_time'],
                        }

                        return {
                            'success': True,
                            'data': result,
                            'image': settings.BASE_URL + pestDetectionRecord.processed_image.url,
                        }
            else:
                raise APIException(e)
                
        except requests.exceptions.Timeout:
            raise requests.exceptions.Timeout(e)
        
        except Exception as e:
            raise APIException(e)

    def decode_processed_image(self, base64_str):
        """
        解码Base64格式的处理后图像
        
        Args:
            base64_str: Base64编码的图像字符串
            
        Returns:
            PIL.Image: 解码后的图像对象
        """
        try:
            if base64_str.startswith('data:image'):
                # 移除data URL前缀
                base64_str = base64_str.split(',', 1)[1]
            
            image_data = base64.b64decode(base64_str)
            return BytesIO(image_data)
        except Exception as e:
            raise ValueError(f"图像解码失败: {str(e)}")
        