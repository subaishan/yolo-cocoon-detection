### 统一错误结构工厂
from django.http import Http404
from rest_framework.exceptions import APIException, AuthenticationFailed, PermissionDenied,NotFound,Throttled
from requests.exceptions import Timeout, RequestException
from rest_framework import serializers, status

class ConflictException(APIException):
    """409业务逻辑错误类

    Args:
        APIException (APIException): 父类
    """
    status_code = status.HTTP_409_CONFLICT
    default_code = 'conflict_error'

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        

from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # 调用DRF默认的异常处理器
    response = exception_handler(exc, context)
    
    if isinstance(exc, serializers.ValidationError):
        # 自定义验证错误的格式 400
        response.data = {
            'success': False,
            'code': 'validation_error',
            'message': '参数验证失败',
            'errors': response.data
        }
        return response
    
    if isinstance(exc, AuthenticationFailed):
        # 自定义认证失败错误格式 401
        response.data = {
            'success': False,
            'code': 'AuthenticationFailed',
            'message': '认证失败',
            'errors': response.data
        }
        return response
        
    if isinstance(exc, PermissionDenied):
        # 自定义权限不足错误格式 403
        response.data = {
            'success': False,
            'code': 'PermissionDenied',
            'message': '权限不足',
            'errors': response.data
        }
        return response

    if isinstance(exc, Http404):
        # 自定义资源不存在错误格式 404
        response.data = {
            'success': False,
            'code': 'NotFound',
            'message': '资源不存在',
            'errors': response.data
        }
        return response

    if isinstance(exc, NotFound):
        # 自定义资源不存在错误格式 404
        response.data = {
            'success': False,
            'code': 'NotFound',
            'message': '资源不存在',
            'errors': response.data
        }
        return response
    
    if isinstance(exc, ConflictException):
        # 自定义业务逻辑错误格式 409
        response.data = {
            'success': False,
            'code': 'conflict_error',
            'message': '业务逻辑错误',
            'errors': response.data
        }
        return response

    if isinstance(exc, Throttled):
        # 自定义频率过高错误格式 429
        response.data = {
            'success': False,
            'code': 'Throttled',
            'message': '访问频率过高',
            'errors': response.data
        }
        return response

    if isinstance(exc, APIException):
        # 自定义服务器错误格式 500
        response.data = {
            'success': False,
            'code': 'server_error',
            'message': '服务器错误',
            'errors': response.data
        }
        return response
    
    if isinstance(exc, Timeout):
        # 自定义request库中Timeout错误
        response.data = {
            'success': False,
            'code': 'Timeout',
            'message': '请求超时',
            'errors': response.data
        }
        response.status_code = status.HTTP_504_GATEWAY_TIMEOUT
        return response

    return response