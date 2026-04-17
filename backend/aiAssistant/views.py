# aiAssistant模块的视图层

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, PermissionDenied, AuthenticationFailed
from rest_framework import status, generics, permissions

from .DeepseekService import DeepSeekClient
from .serializers import ConversationCreateSerializer, ConversationListSerializer, MessageListSerializer, ConversationUpdateSerializer, ChatSerializer
from .models import Conversation, Message

deepSeekClient = DeepSeekClient()

class ChatView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChatSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        response = deepSeekClient.get_chat_response(request)
        return Response({
            'message': response.choices[0].message.content
        })

class ChatCreateView(generics.CreateAPIView):
    """
    创建AI会话的接口
    """
    serializer_class = ConversationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """执行创建AI会话的业务逻辑

        Args:
            request (request): http请求

        Returns:
            _type_: http响应
        """
        return super().create(request, *args, **kwargs)
    

class ChatListView(generics.ListAPIView):
    """
    返回AI会话记录列表
    """
    serializer_class = ConversationListSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['created_at', 'updated_at', 'token_usage', 'user']
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """查询数据库中所属用户的AI会话记录

        Returns:
            _type_: 返回查询结果
        """
        return Conversation.objects.filter(user=self.request.user)
    

class ChatUpdateView(generics.UpdateAPIView):
    """
    更新AI会话记录的标题字段
    """
    serializer_class = ConversationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        """在数据库中查询出对应ID的AI会话记录

        Returns:
            _type_: 查询结果
        """
        conversation_id = self.kwargs.get('id')
        return Conversation.objects.filter(id=conversation_id)
    
    def perform_update(self, serializer):
        return super().perform_update(serializer)
    

class ChatDeleteView(generics.DestroyAPIView):
    """
    删除AI会话记录接口, 执行删除AI会话记录的业务逻辑
    """
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        """查询数据库中所属用户的AI会话记录

        Returns:
            _type_: 返回查询结果
        """
        return Conversation.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """删除数据库中对应ID的用户的AI会话记录

        Args:
            request (_type_): http请求

        Raises:
            PermissionDenied: 如果登陆用户和删除的会话的用户不是同一个用户,抛出权限异常

        Returns:
            Response: 返回http响应
        """
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied({'user': {'code': 'Perm-ERROR', 'message': '权限不足'}})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class MessageListView(generics.ListAPIView):
    """
    返回对应AI会话记录相关联的Message模型中的content字段
    """
    serializer_class = MessageListSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['conversation', 'created_id', 'role', 'tokens', 'created_at']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """查询数据库中对应ID的AI会话记录

        Returns:
            _type_: 返回查询结果
        """
        conversation_id = self.kwargs.get('conversation_id')
        return Message.objects.filter(conversation=conversation_id)