from .models import PestDetectionRecord
from rest_framework import serializers

class PestDetectionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PestDetectionRecord
        fields = ['original_image']
    
    def validate(self, attrs):

        errors = {}

        original_image = attrs['original_image']

        # 验证图片格式
        allowed_content_types = ['image/jpeg', 'image/png', 'image/jpg']
        if original_image.content_type not in allowed_content_types:
            errors['original_image'] = {'code': 'type_errors', 'messages': '只支持JPEG和PNG格式的图片'}
        
        # 验证文件大小 (10MB)
        if original_image.size > 10 * 1024 * 1024:
            errors['original_image'] = {'code': 'size_errors', 'messages': '图片大小不能超过10MB'}
        
        # 如果有错误，抛出异常
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs
    

class PestDetectionListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PestDetectionRecord
        fields = ['id', 'created_at', 'status', 'detection_count', 'processing_time']


class PestDetectionRetrieveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PestDetectionRecord
        fields = ['original_image', 'processed_image', 'detection_data']