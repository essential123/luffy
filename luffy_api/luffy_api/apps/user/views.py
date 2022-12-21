# post ----> 查询 --->使用ViewSetMixin自动生成路由，action装饰器可以在视图类中写多个函数
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from .models import UserInfo

from .serializer import UserMulLoginSerializer, UserMobileLoginSerializer, UserRegisterSerializer
from utils.response import APIResponse
from rest_framework.exceptions import APIException
from libs.send_tx_sms import get_code, send_sms_by_phone
import re
from django.core.cache import cache
from django.http import HttpResponse
from utils.view import CommonListModelMixin


# from rest_framework_jwt.views import obtain_jwt_token

class UserView(ViewSet):
    # 不写action不会生成路由
    def get_serializer(self, data):
        # 两种写法
        # 如果 （请求地址/action） 是mul_login，返回UserMulLoginSerializer
        # 如果 （请求地址/action） 是mobile_login，返回UserMobileLoginSerializer
        # if self.request=='mul_login':
        if self.action == 'mul_login':
            return UserMulLoginSerializer(data=data)
        else:
            return UserMobileLoginSerializer(data=data)

    def common_login(self, request):
        ser = self.get_serializer(data=request.data)
        # 如果校验通过继续往下走，校验不通过直接抛异常，捕获全局异常，drf的异常
        ser.is_valid(raise_exception=True)
        token = ser.context.get('token')
        username = ser.context.get('username')
        icon = ser.context.get('icon')
        return APIResponse(token=token,username=username, icon=icon)

    @action(methods=['POST'], detail=False, url_path='mul_login')
    def mul_login(self, request):
        return self.common_login(request)

    @action(methods=['POST'], detail=False, url_path='mobile_login')
    def mobile_login(self, request):
        return self.common_login(request)

    @action(methods=['POST'], detail=False)
    def mobile_register(self, request):
        ser = UserRegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return APIResponse(msg='注册成功')
        # 后期可以写注册并且登录的接口

    @action(methods=['GET'], detail=False)
    def mobile(self, request):
        try:
            mobile = request.query_params.get('mobile')
            UserInfo.objects.get(mobile=mobile)
            return APIResponse(msg='手机号存在')
        except Exception as e:
            raise APIException('手机号不存在')

    @action(methods=['GET'], detail=False)
    def send_sms(self, request):
        mobile = request.query_params.get('mobile')
        if re.match(r'^1[3-9][0-9]{9}$', mobile):
            code = get_code()  # 需要保存验证码（能存能取不能丢）---》缓存
            # 放在内存当中，项目重启就没了---》后期放在redis中，重启项目还在
            cache.set('sms_code_%s' % mobile, code)
            res = send_sms_by_phone(mobile, code)
            if res:
                return APIResponse(msg='发送短信成功')
            else:
                # raise APIException('发送短信失败')
                return APIResponse(code=101, msg='发送失败，请稍后再试')
        else:
            return APIResponse(code=102, msg='手机号不合法')


# from django.shortcuts import HttpResponse
# class Person:
#     pass
#
# from django.core.cache import cache
#
# def index(request):
#     # cache.set('pv', '10', 3)  # 之前缓存在内存中，现在缓存在redis中
#     # 缓存强大在，可以缓存任意的python数据类型
#     p = Person()
#     p.name = 'xxx'
#     cache.set('p', p)
#     return HttpResponse('把p缓存起来了')
#
# def test(request):
#     p=cache.get('p')
#     print(p.name)
#     return HttpResponse('把p取出来了')

from celery_task.user_task import send_sms


def index(request):
    mobile = request.GET.get('mobile')
    # 异步
    res = send_sms.delay(mobile, '8888')
    print(res)
    return HttpResponse('已经发送了')


from celery_task.user_task import seckill_task
from celery_task.celery import app
from celery.result import AsyncResult
from django.http import JsonResponse


def seckill(request):
    # 提交秒杀任务
    res = seckill_task.delay()
    return JsonResponse({'code': 100, 'msg': '正在排队', 'id': str(res)})


def get_result(request):
    task_id = request.GET.get('id')
    res = AsyncResult(id=task_id, app=app)
    if res.successful():
        result = res.get()  # 7
        return JsonResponse({'code': 100, 'msg': str(result)})
    elif res.failed():
        print('任务失败')
        return JsonResponse({'code': 101, 'msg': '秒杀失败'})
    elif res.status == 'PENDING':
        print('任务等待中被执行')
        return JsonResponse({'code': 102, 'msg': '还在排队'})
