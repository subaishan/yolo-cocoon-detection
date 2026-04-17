from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailOrUsernameModelBackend(ModelBackend):
    """
    支持邮箱或用户名登录的认证后端
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        用户名 username
        密码   password
        """
        UserModel = get_user_model()
        try:
            # 判断输入是邮箱还是用户名
            if '@' in username:
                user = UserModel.objects.get(email=username)
            else:
                user = UserModel.objects.get(username=username)
                
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
        except Exception:
            return None