#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BYwork.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()



# 必要依赖 djang、 mysqlclient、 django-cors-headers、 djangorestframework

# 开发模式 运行命令 python manage.py runserver --settings=myproject.settings.development.py

# 生产模式 运行命令 python manage.py runserver --settings=myproject.settings.production.py

# 检查数据库格式是否标准 python manage.py check --database default

# 数据库连接测试 进入数据库交互界面 python manage.py dbshell

# 生成迁移文件命令 python manage.py makemigrations APPNAME

# 执行迁移 python manage.py migrate

# 收集静态文件 python manage.py collectstatic

# 创建测试用的超级用户 python manage.py createsuperuser

# 重置迁移
# python manage.py makemigrations --empty appname  # 生成空迁移文件（可选）
# python manage.py migrate --fake appname zero     # 重置迁移记录
# python manage.py makemigrations                        # 重新生成迁移
# python manage.py migrate --fake-initial                # 同步数据库

# 模块
# accounts 用户模块
# regions 园区管理模块
# gateways 网关模块
# sensors 传感器模块
# pestDetection 病虫害模块
# imageDetection 病虫害识别模块
# aiAssistant AI智能助手模块



