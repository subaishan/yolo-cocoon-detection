from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout
from rest_framework.response import Response
from utils import exc
from .serializers import RegisterSerializer, LoginSerializer

# Create your views here.
class RegisterAPIView(generics.CreateAPIView):
    """
    处理用户注册的接口
    """

    permission_classes = [AllowAny]  # 允许未认证用户访问
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        responst = super().create(request, *args, **kwargs)
        user = responst.data
        print(user)
        return Response({
            'success': True,
            'message': '注册成功',
            'userInfo': user
        }, status=status.HTTP_200_OK)
    

class LoginAPIView(APIView):
    """登陆视图类

    """

    permission_classes = [AllowAny]  # 允许未认证用户访问

    def post(self, request):
        """post请求

        Args:
            request (request): request

        Returns:
            Response: 请求结果
        """
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        userInfo = serializer.validated_data['userInfo']
        token = serializer.validated_data['token']

        return Response({
            'success': True,
            'message': '登陆成功',
            'userInfo': userInfo,
            'token': token
        }, status=status.HTTP_200_OK)
    

class LogOutAPIView(APIView):
    """登出试图类
    
    后期可以设置, 配合redis实现token黑名单, 可以提高安全性
    """

    def post(self, request):
        try:
            logout(request)
            return Response({
                'success': True,
                'message': '登出成功',
            }, status=status.HTTP_200_OK)
        except Exception as e:
            exc.make_server_error(e)
            
