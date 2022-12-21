#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # 第一行就在加载配置文件，如果配置文件不对，django项目肯定起不来
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffy_api.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # print(sys.argv) # ['D:/djangoProject/luffy_api/manage.py', 'runserver', '8000']
    execute_from_command_line(sys.argv)

# 执行python manage.py runserver 本质就是执行main函数，传了一个参数runserver
if __name__ == '__main__':
    main()
