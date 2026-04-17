import os
from pathlib import Path
from datetime import timedelta

# 基础路径配置
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL = 'http://localhost:8000'

DEEPSEEK_API_KEY  = "sk-8d137a901b174a9caae264ea489842f4"   # Deepseek的API_KEY
DEEPSEEK_BASE_URL = "https://api.deepseek.com"  # Deepseek的BASE_URL

IMAGEDETECTION_BASE_URL = 'http://localhost:6006'

# =====================
# 安全相关配置
# =====================
SECRET_KEY = 'django-insecure-your-secret-key-here'  # 生产环境从环境变量读取
DEBUG = True
ALLOWED_HOSTS = ['*'] # 生产环境指定域名

# =====================
# 应用定义
# =====================
INSTALLED_APPS = [
    # Django 核心应用
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 第三方应用
    'corsheaders',      # 跨域支持
    'rest_framework',   # DRF核心
    'rest_framework_simplejwt',  # JWT认证
    
    # 本地应用
    'accounts',         # 用户管理
    'regions',          # 园区管理
    'gateways',         # 网关管理
    'sensors',          # 传感器管理
    'Environmental',    # 环境数据管理
    'pestDetection',    # 病虫害数据管理
    'imageDetection',   # YOLO模型图片识别
    'aiAssistant',      # deepseek模型

    'django_cleanup.apps.CleanupConfig',    # 自动删除模型关联的文件
]

# =====================
# 中间件
# =====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =====================
# 数据库配置 (生产环境建议使用环境变量)
# =====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'bywork1'),
        'USER': os.getenv('DB_USER', 'testUser'),
        'PASSWORD': os.getenv('DB_PASSWORD', '260417BYWork.'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",  # 启用严格模式
        }
    }
}

# =====================
# 配置redis缓存 
# =====================

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# =====================
# 路由配置 
# =====================
ROOT_URLCONF = 'BYwork.urls'

# =====================
# 模板配置
# =====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'BYwork.wsgi.application'

# =====================
# 密码验证器设置
# =====================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =====================
# 认证配置
# =====================
AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# =====================
# DRF + JWT 配置
# =====================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # 仅保留JWT
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # 默认需要认证
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer' if DEBUG else None,
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'EXCEPTION_HANDLER': 'utils.exc.custom_exception_handler',
}

# JWT 详细配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,  # 刷新时返回新refresh_token
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,  # 更新last_login字段
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# =====================
# 跨域配置 (CORS)
# =====================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Disposition']  # 允许前端访问的文件下载头

# =====================
# 安全增强配置
# =====================
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1年HSTS
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

CSRF_COOKIE_HTTPONLY = False  # 允许JS读取
CSRF_COOKIE_SAMESITE = 'Lax'  # 平衡安全与第三方集成
SESSION_COOKIE_HTTPONLY = True  # 防止XSS读取Session

# =====================
# 文件与静态资源
# =====================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# FILE_UPLOAD_PERMISSIONS = 0o644  # 文件权限设置

# =====================
# 国际化
# =====================
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True  # 使用时区感知

# =====================
# 其他配置
# =====================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
PASSWORD_RESET_TIMEOUT = 180  # 密码重置有效期(秒)
SILENCED_SYSTEM_CHECKS = ['admin.E410'] # 忽视E410警告