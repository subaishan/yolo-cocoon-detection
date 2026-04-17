from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import APIException
from .models import Sensor


class SensorCreateSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model=Sensor
        fields = ['id', 'name', 'device_id', 'gateway', 'status']
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate(self, attrs):
        errors = {}

        if Sensor.objects.filter(device_id=attrs['device_id']).exists():
            errors['device_id'] = {'code': 'exists', 'message': '设备ID已存在'}

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
    
    def create(self, validated_data):
        try:
            with transaction.atomic():
                sensor = Sensor.objects.create(
                    name=validated_data['name'],
                    device_id=validated_data['device_id'],
                    gateway=validated_data['gateway'],
                    status=validated_data['status']
                )
                return sensor
        except Exception as e:
            print(e)
            raise APIException(e)


class SensorListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Sensor
        fields = ['id', 'name', 'device_id', 'gateway', 'status', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


class SensorUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Sensor
        fields = ['id', 'name', 'device_id', 'gateway', 'status']
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate(self, attrs):
        errors = {}

        if 'device_id' in attrs:
            if Sensor.objects.filter(device_id=attrs['device_id']).exists():
                errors['device_id'] = {'code': 'exists', 'message': '设备ID已存在'}

        if errors: 
            raise serializers.ValidationError(errors)

        return attrs