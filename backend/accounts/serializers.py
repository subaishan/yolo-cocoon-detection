from django.contrib.auth import authenticate, get_user_model, password_validation
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed, APIException
from rest_framework import serializers
from django.db import transaction
from django.conf import settings
from utils import exc



User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'nickname', 'phone')
        extra_kwargs = {
            'nickname': {'required': False},
            'username': {'read_only': True},
        }

    def validate_empty_values(self, data):
        """判断必要字段是否为空值

        Args:
            data (any): request中的数据

        Raises:
            serializers.ValidationError: 返回字段为空的结果

        Returns: 
            (元组): 判定通过，返回数据
        """
        errors = {}

        if not data.get('email'):
            errors['email'] = {'code': 'required', 'message': '邮箱是必填项'}
        if not data.get('password1'):
            errors['password1'] = {'code': 'required', 'message': '密码是必填项'}
        if not data.get('password2'):
            errors['password2'] = {'code': 'required', 'message': '确认密码是必填项'}
        if not data.get('phone'):
            errors['phone'] = {'code': 'required', 'message': '手机号是必填项'}

        if errors:
            raise serializers.ValidationError(errors)

        return (False, data)
    
    def validate_email(self, value):
        """邮箱字段自定义校验

        Args:
            value (string): 邮箱值

        Raises:
            serializers.ValidationError: 邮箱重复抛出异常

        Returns:
            string: 没有问题, 返回数据
        """
        error = {}
        if User.objects.filter(email=value).exists():
            error['email'] = {'code': 'email_exists', 'message': '邮箱已经被注册'}
            raise exc.ConflictException(error)
            
        return value
    
    def validate_phone(self, value):
        """手机号字段自定义校验

        Args:
            value (string): 手机号值

        Raises:
            exc.ConflictException: 手机号重复抛出异常

        Returns:
            string: 没有问题, 返回数据
        """
        error = {}
        if User.objects.filter(phone=value).exists():
            error['phone'] = {'code': 'phone_exists', 'message': '手机已经被注册'}
            raise exc.ConflictException(error)
        return value

    def validate(self, attrs):
        """对象级字段验证
           没有使用
        Args:
            attrs (any): request中的数据

        Returns:
            any: 参数
        """
        return super().validate(attrs)
    
    def create(self, validated_data):
        """创建用户

        Args:
            validated_data (any): 通过验证的数据

        Returns:
            user: 返回创建完成的用户实例
        """
        try:
            # 移除 password2
            validated_data.pop('password2')
            password = validated_data['password1']

            with transaction.atomic():
                while True:
                    user = User.objects.create(
                        email = validated_data['email'],
                        nickname = validated_data.get('nickname', ''),
                        phone = validated_data.get('phone', ''),
                    )
                    user.set_password(password)
                    return user
        except Exception as e:
            raise APIException(e)


class LoginSerializer(serializers.Serializer):
    # 用户名和密码的字段
    username = serializers.CharField(
        label=('用户名或邮箱'),
        write_only=True
    )
    password = serializers.CharField(
        label=('密码'),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate_empty_values(self, data):
        """基本参数是否为空的校验

        Args:
            data (any): request中的data

        Returns:
            any: 返回原始数据data
        """
        errors = {}

        if not data.get('username'):
            errors['username'] = {'code': 'required', 'message': '用户名是必填项'}
        if not data.get('password'):
            errors['password'] = {'code': 'required', 'message': '密码是必填项'}
        
        if errors:
            raise serializers.ValidationError(errors)
            
        return (False, data)
    
    def validate(self, attrs):
        """验证账户密码

        Args:
            attrs (any): 参数

        Raises:
            serializers.ValidationError: 账号和密码错误

        Returns:
            any: 返回添加user后的参数
        """
        # 调用自定义认证后端
        errors = {}

        user = authenticate(
            request=self.context.get('request'),
            username=attrs.get('username'),
            password=attrs.get('password')
        )

        if not user:
            errors['user'] = {'code': 'not_find','message': '用户或密码错误'}
            raise AuthenticationFailed(errors)
        
        # 生成token
        refresh = RefreshToken.for_user(user)

        attrs['user'] = user
        attrs['userInfo'] = {
            'username': user.username,
            'nickname': user.nickname, 
            'avatar': f"{settings.BASE_URL}{user.avatar.url}"
            }
        attrs['token'] = {'access_token': str(refresh.access_token), 'refresh': str(refresh)}
        return attrs
