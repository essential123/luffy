from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

router.register('banner', views.BannerView, 'banner')
urlpatterns = [
]
urlpatterns += router.urls
