# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 列表页显示字段
    list_display = ('username', 'email', 'nickname', 'last_active')
    
    # 只读字段（包含自动生成的username）
    readonly_fields = ('username', 'last_active')
    
    # 字段分组配置
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('email', 'nickname', 'phone', 'avatar')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('时间记录', {'fields': ('last_active', 'date_joined', 'last_login')}),
    )
    
    # 添加用户时的字段配置（重要！）
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2'),
        }),
    )
    
    # 按邮箱排序
    ordering = ('email',)