from celery import Celery
import os

# 在django中集成celery需要加入以下django配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffy_api.settings.dev')  # 项目上线用上线环境的settings.py
import django

django.setup()

broker = 'redis://127.0.0.1:6379/0'
backend = 'redis://127.0.0.1:6379/1'
app = Celery(__name__, backend=backend, broker=broker, include=['celery_task.home_task', 'celery_task.user_task'])

# 写定时任务
# app的配置项
# 时区  app.conf  所有的配置字典，默认的
app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
app.conf.enable_utc = False
## 编写定时任务
from datetime import timedelta
from celery.schedules import crontab

app.conf.beat_schedule = {
    # 'send_sms_task': {
    #     'task': 'celery_task.user_task.send_sms',  # 指定哪一个任务
    #     'schedule': timedelta(hours=5),  # 事件对象，
    #     # 'schedule': crontab(hour=8, day_of_week=1),  # 每周一早八点
    #     'args': ('1897334444', '7777'),  # 参数
    # },
    # 'add_task': {
    #     'task': 'celery_task.home_task.add',
    #     'schedule': crontab(hour=12, minute=10, day_of_week=3),  # 每周三早12.10
    #     'args': (10, 20),
    # },
    'update_banner': {
        'task': 'celery_task.home_task.update_banner',
        'schedule': timedelta(seconds=50),
        'args': (),
}

}
