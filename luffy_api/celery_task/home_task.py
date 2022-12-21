import time
from .celery import app
@app.task  # app注册
def add(a, b):
    time.sleep(1)
    print('计算结果:%s' % (a + b))
    return a + b

from django.core.cache import cache
from home.models import Banner
from django.conf import settings
from home.serializer import BannerSerializer
@app.task
def update_banner():
    # 更新缓存
    # 查询出现在轮播图的数据
    queryset=Banner.objects.all().filter(is_delete=False,is_show=True).order_by('orders')[:settings.BANNER_COUNT]
    # 查出来是一个queryset对象，需要序列化
    ser=BannerSerializer(many=True,instance=queryset)
    # ser 中得图片，没有前面地址
    for item in ser.data:
        # 走定时任务不会拼接路径
        item['image'] = settings.HOST_URL + item['image']
    cache.set('banner_list',ser.data)
    return True