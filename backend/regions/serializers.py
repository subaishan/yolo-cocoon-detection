from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import APIException
from .models import Region


class RegionCreateSerializer(serializers.ModelSerializer):
    
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'user', 'name', 'location', 'area', 'description']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
        }
    
    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        try:
            with transaction.atomic():
                while True:
                    region = Region.objects.create(
                        user = validated_data['user'],
                        name = validated_data['name'],
                        location = validated_data['location'],
                        area = validated_data['area'],
                        description = validated_data['description']
                    )

                    return region
        except Exception as e:
            raise APIException(e)
        

class RegionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ['id', 'user', 'name', 'location', 'area', 'description', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def validate(self, attrs):
        return super().validate(attrs)
    
    
class RegionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ['id', 'name', 'location', 'area', 'description']

    def validate(self, attrs):
        return super().validate(attrs)
    
