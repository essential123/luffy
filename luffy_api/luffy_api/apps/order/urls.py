from rest_framework.routers import SimpleRouter
from . import views
router = SimpleRouter()
# 127.0.0.1:8000/api/v1/order/alipay/---->post 请求
router.register('alipay',views.OrderView,'alipay')
# 127.0.0.1:8000/api/v1/order/success/---->get请求  post请求
router.register('success',views.PaySuccessView,'success')
urlpatterns = [
]
urlpatterns += router.urls
