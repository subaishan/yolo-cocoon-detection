"""
URL configuration for BYwork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # 用户登陆和认证管理
    path('accounts/', include('accounts.urls')),

    # AI智能助手
    path('ai/', include('aiAssistant.urls')),

    # 图像识别模块
    path('detection/', include('imageDetection.urls')),

    # 园区管理模块
    path('regions/', include('regions.urls')),

    # 网关管理模块
    path('gateway/', include('gateways.urls')),

    # 传感器管理模块
    path('sensors/', include('sensors.urls')),

    # 环境数据管理模块
    path('envdata/', include('Environmental.urls')),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
