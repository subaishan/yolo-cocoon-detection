from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import APIException
from .models import EnvironmentData


class EnvironmentDataCreateSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model=EnvironmentData
        fields = ['id', 'sensor', 'temperature', 'humidity', 'light_intensity', 'co2_concentration', 'recorded_at', 'created_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        try:
            with transaction.atomic():
                environmentdata = EnvironmentData.objects.create(
                    sensor=validated_data['sensor'],
                    temperature=validated_data['temperature'],
                    humidity=validated_data['humidity'],
                    light_intensity=validated_data['light_intensity'],
                    co2_concentration=validated_data['co2_concentration'],
                    recorded_at=validated_data['recorded_at'],
                )
                return environmentdata
        except Exception as e:
            print(e)
            raise APIException(e)
        

class EnvironmentDataListSerializer(serializers.ModelSerializer):
    
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model=EnvironmentData
        fields = ['id', 'sensor', 'temperature', 'humidity', 'light_intensity', 'co2_concentration', 'recorded_at', 'created_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
        }


