# aiAssistant模块的服务层

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.core.cache import cache
from django.db import transaction
from django.db.models import F
import logging

from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
from .models import Conversation, Message

logger = logging.getLogger(__name__)

class DeepSeekClient:
    
    def __init__(self, API_KEY=settings.DEEPSEEK_API_KEY, BASE_URL=settings.DEEPSEEK_BASE_URL):
        self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

        self.max_context_messages = 10  # 缓存中最大上下文消息数
        self.cache_timeout = 3600   # redis缓存时间
        self.cache_key = "ctx:{conversation_id}"    # redis中的KEY

    def make_cache_key(self, conversation_id):
        return self.cache_key.format(conversation_id=conversation_id)
    
    def get_context(self, conversation_id):
        
        key = self.make_cache_key(conversation_id=conversation_id)
        
        # 从缓存中获取对话信息
        if cached := cache.get(key):
            return cached
        
        # 缓存不存在时从数据库加载
        context = Message.objects.filter(
            conversation_id=conversation_id
        ).order_by('-created_at')[:self.max_context_messages].values_list('content', flat=True)

        # 反转顺序
        context = list(reversed(context)) 

        cache.set(key=key, value=context, timeout=self.cache_timeout)

        return context
    
    def update_context(self, Response, conversation_id, new_message):
        
        with transaction.atomic():
            while True:
                key = self.make_cache_key(conversation_id=conversation_id)
                reply = Response.choices[0].message.model_dump()
                total_tokens = Response.usage.total_tokens
                prompt_tokens = Response.usage.total_tokens
                completion_tokens = Response.usage.completion_tokens

                # 获取消息
                context = self.get_context(conversation_id=conversation_id) or []

                # 追加新消息
                context.append(new_message)
                context.append(reply)
                context = context[-self.max_context_messages:]
                cache.set(key=key, value=context, timeout=self.cache_timeout)

                Message.objects.create(conversation_id=conversation_id, role='user', content=new_message, tokens=prompt_tokens)
                Message.objects.create(conversation_id=conversation_id, role='user', content=reply,         tokens=completion_tokens)
                Conversation.objects.filter(id=conversation_id).update(token_usage=F('token_usage') +total_tokens)

                return context

    def get_chat_response(self, request, created_conversation_id=None, model="deepseek-chat"):
        
        if created_conversation_id:
            conversation_id = created_conversation_id
        else:
            conversation_id = request.data.get('conversation_id')

        new_message = request.data.get('message')[0]
        context = self.get_context(conversation_id) or []

        context.append(new_message)
    
        response = self.client.chat.completions.create(
            model=model,
            messages=context,
            stream=False
        )
        self.update_context(Response=response, conversation_id=conversation_id, new_message=new_message)
        return response
        
    def create_conversation(self,user, title):
        try:
            conversation = Conversation.objects.create(user=user, title=title)
            return conversation
        except Exception as e:
            return None
        

