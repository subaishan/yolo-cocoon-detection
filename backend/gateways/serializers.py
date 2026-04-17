from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import APIException
from regions.models import Region
from .models import Gateway


class GatewayCreateSerializer(serializers.ModelSerializer):
    
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Gateway
        fields = ['id', 'name', 'device_id', 'region', 'location', 'status', 'last_heartbeat']
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate(self, attrs):

        errors = {}

        if Gateway.objects.filter(device_id=attrs['device_id']).exists():
            errors['device_id'] = {'code': 'exists', 'message': '设备ID已存在'}

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
    

    def create(self, validated_data):
        try:
            with transaction.atomic():
                gateway = Gateway.objects.create(
                    name=validated_data['name'],
                    device_id=validated_data['device_id'],
                    region=validated_data['region'],
                    location=validated_data['location'],
                    status=validated_data['status'],
                    last_heartbeat=validated_data['last_heartbeat']
                )
                return gateway
        except Exception as e:
            raise APIException(e)
        

class GatewayListSerializer(serializers.ModelSerializer):
    
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Gateway
        fields = ['id', 'name', 'device_id', 'region', 'location', 'status', 'last_heartbeat', 'installed_at', 'updated_at']
        extra_kwargs = {
            'id': {'read_only': True},
        }


class GatewayUpdateSerializer(serializers.ModelSerializer):
    
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Gateway
        fields = ['id', 'name', 'device_id', 'region', 'location', 'status', 'last_heartbeat']
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate(self, attrs):

        errors = {}
        if 'device_id' in attrs:
            if Gateway.objects.filter(device_id=attrs['device_id']).exists():
                errors['device_id'] = {'code': 'exists', 'message': '设备ID已存在'}

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
