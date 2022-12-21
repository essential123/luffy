from .models import Banner
from .serializer import BannerSerializer

# 自动生成路由
from rest_framework.viewsets import GenericViewSet
# 获取所有
from utils.view import CommonListModelMixin
from django.conf import settings
from django.core.cache import cache
from utils.response import APIResponse
from .models import Banner


class BannerView(GenericViewSet, CommonListModelMixin):
    queryset = Banner.objects.all().filter(is_delete=False, is_show=True).order_by('orders')[:settings.BANNER_COUNT]
    serializer_class = BannerSerializer

    def list(self, request, *args, **kwargs):
        result = cache.get('banner_list')
        if result:  # 如果缓存里有
            print('走了缓存，速度很快')
            return APIResponse(result=result)  # 直接将轮播图的数据返回
        else:
            # 如果缓存里没有，去数据库拿
            print('走了数据库，速度慢')
            res = super().list(request, *args, **kwargs)  # 调用父类获取所有数据
            result = res.data.get('result')  # {code:100,msg:成功，result:[{},{}]}  取出轮播图的数据对象
            cache.set('banner_list', result)  # 将轮播图数据对象放到缓存中
            return res
