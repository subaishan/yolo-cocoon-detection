from django.contrib import admin
from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogOutAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', RegisterAPIView.as_view()),   # 注册接口
    path('login/', LoginAPIView.as_view()),     # 登陆接口
    path('logout/', LogOutAPIView.as_view()),   # 登出接口

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),    # 获取token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   # 刷新token
]
