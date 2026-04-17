# aiAssistant模块的模型层

from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Conversation(models.Model):
    """会话管理"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    title = models.CharField(max_length=40, default="新对话")  # 自动生成标题
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    token_usage = models.IntegerField(default=0)  # 累计Token消耗

class Message(models.Model):
    """消息记录（支持上下文记忆）"""

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    created_id = models.CharField(max_length=50, default=uuid.uuid4, editable=False) 
    role = models.CharField(max_length=10)
    content = models.JSONField()
    tokens = models.IntegerField()  # 单条消息Token数
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]  # 确保消息按顺序排列