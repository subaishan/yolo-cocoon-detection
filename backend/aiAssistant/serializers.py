# aiAssistant模块的序列化器

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import APIException, AuthenticationFailed
from .models import Conversation, Message

class ChatSerializer(serializers.Serializer):
    conversation_id = serializers.IntegerField()

    def validate_empty_values(self, data):
        errors = {}
        
        if not data.get('conversation_id'):
            errors['conversation_id'] = {'code': 'required', 'messages': 'conversation_id不存在'}
            raise serializers.ValidationError(errors)
        return (False, data)
    
    def validate(self, attrs):
        errors = {}
        conversation = Conversation.objects.filter(id=attrs['conversation_id'])
        
        if not conversation:
            errors['conversation_id'] = {'code': 'not_find', 'messages': '没找到conversation_id对应对象'}
            raise serializers.ValidationError(errors)
        
        return super().validate(attrs)

class ConversationCreateSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField()

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'title']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
        }

    def validate_empty_values(self, data):
        errors = {}
        if not data.get('title'):
            errors['title'] = {'code': 'required', 'messages': 'title不存在'}
            raise serializers.ValidationError(errors)
        return (False, data)

    def validate(self, attrs):
        errors = {}

        if not attrs['user']:
            errors['user'] = {'code': 'AUTH-ERROR', 'message': '认证错误'}
            return AuthenticationFailed(errors)
        return attrs
    
    def create(self, validated_data):
        try:
            with transaction.atomic():
                conversation = Conversation.objects.create(
                    user=validated_data['user'],
                    title=validated_data['title']
                )
                return conversation
        except Exception as e:
            raise APIException(e)
        

class ConversationListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'title']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'title': {'read_only': True},
        }

    def validate(self, attrs):
        errors = {}

        if not attrs['user']:
            errors['user'] = {'code': 'AUTH-ERROR', 'message': '认证错误'}
            return AuthenticationFailed(errors)
        return attrs
    

class ConversationUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    
    class Meta:
        model = Conversation
        fields = ['title'] 
        extra_kwargs = {
            'title': {
                'required': True,
                'allow_blank': False,
                'max_length': 15
            }
        }
    

class MessageListSerializer(serializers.ModelSerializer):
    content = serializers.JSONField(read_only=True)

    class Meta:
        model = Message
        fields = ['content']
        extra_kwargs={
            'content': {'read_only': True},
        }
        
        