from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import time
import random

def avatar_upload_path(instance, filename):
    """头像上传路径，按用户ID分目录存储"""
    return f'users/{instance.id}/avatar/{filename}'

def generate_username():
        """生成用户名
        规则：
        1. 前2位:固定为'10'
        2. 中间6位:时间戳基值(年月日时分混合)
        3. 最后3位:随机数 + 校验位(避免连续重复)

        Returns:
            string: 用户名
        """
        # 时间戳部分（混合年月日时分）
        current_time = time.localtime()
        time_part = (
            f"{current_time.tm_year % 100:02d}"  # 年后2位
            f"{current_time.tm_mon:02d}"
            f"{current_time.tm_mday:02d}"
            f"{current_time.tm_min:02d}"
        )[:6]  # 取6位

        # 随机部分（3位，避免连续重复数字）
        rand_part = ""
        for _ in range(3):
            while True:
                digit = str(random.randint(0, 9))
                if not rand_part or digit != rand_part[-1]:  # 避免连续相同
                    rand_part += digit
                    break
                
        # 组合：10 + 时间部分 + 随机部分 = 11位
        return f"10{time_part}{rand_part}"

class User(AbstractUser):
    """
    用户核心模型
    特性：
    - 系统生成的唯一用户名（数字ID）
    - 邮箱必填且唯一
    - 支持手机号绑定（可选）
    - 自动维护最后活动时间
    """
    
    # ---- 覆盖AbstractUser字段 ----
    username = models.CharField(
        _('用户名'),
        max_length=15,
        unique=True,
        editable=False,  # 禁止手动编辑
        default=generate_username,
        help_text=_('系统生成的唯一ID')
    )
    email = models.EmailField(
        _('邮箱'),
        unique=True,
        error_messages={
            'unique': "该邮箱已被注册"
        }
    )
    
    # ---- 扩展字段 ----
    nickname = models.CharField(
        _('显示名称'),
        max_length=100,
        blank=True,
        default='',
        help_text=_('前端展示的名称（默认为用户名）')
    )
    phone = models.CharField(
        _('手机号'),
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        error_messages={
            'unique': _("该手机号已被绑定")
        }
    )
    avatar = models.ImageField(
        _('头像'),
        upload_to=avatar_upload_path,
        default='users/default/avatar.png',
        blank=True
    )
    last_active = models.DateTimeField(
        _('最后活跃时间'),
        auto_now=True
    )

    # ---- 认证配置 ----
    USERNAME_FIELD = 'username'  # 唯一标识字段
    REQUIRED_FIELDS = ['email']  # 创建超级用户时的必填字段

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return self.nickname or self.username

    def save(self, *args, **kwargs):
        """自动处理显示名称"""
        if not self.nickname:
            self.nickname = self.username
        super().save(*args, **kwargs)