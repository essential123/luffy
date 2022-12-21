from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
from django.urls import path

router.register('user', views.UserView, 'user')
urlpatterns = [
    path('index/', views.index),
    # path('test/',views.test),
    path('seckill/', views.seckill),
    path('get_result/', views.get_result),
]
urlpatterns += router.urls
