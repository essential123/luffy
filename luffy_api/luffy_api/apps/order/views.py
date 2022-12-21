from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import GenericViewSet, ViewSet
# from rest_framework.mixins import CreateModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.response import APIResponse
from .serializer import OrderSerializer
from .models import Order
from rest_framework.exceptions import APIException


# class OrderView(GenericViewSet,CreateModelMixin):
class OrderView(GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 这个新增接口既要新增，又要返回支付链接地址，需要重写create方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        # raise_exception=True标记，意味着你可以在你的API中全局复写校验错误响应的格式。如果你要这么做，建议你使用一个自定义的异常
        # 默认情况下，该异常返回400 Bad Request
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        serializer.save()
        pay_url = serializer.context.get('pay_url')
        return APIResponse(pay_url=pay_url)


from rest_framework.response import Response
from utils.common_logger import logger


class PaySuccessView(ViewSet):
    def list(self, request):
        try:
            out_trade_no = request.query_params.get('out_trade_no')
            Order.objects.get(out_trade_no=out_trade_no, order_status=1)
            return APIResponse()
        except Exception as e:
            raise APIException('没查到')

    def create(self, request):  # 给支付宝用的，写完后无法测试-----》
        try:
            # from django.http.request import QueryDict
            # print(type(request.data))
            result_data = request.data.dict()  # 回调回来编码格式是urlencoded，QueryDic对象---》.dict--->转成真正的字典对象
            out_trade_no = result_data.get('out_trade_no')
            signature = result_data.pop('sign')  # 如果是QueryDic对象不允许pop
            from libs import alipay_common
            # 验证签名，result_data和signature验证签名，sdk帮咱们写好了，一定要验证签名
            result = alipay_common.alipay.verify(result_data, signature)
            if result and result_data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
                # 完成订单修改：订单状态、流水号、支付时间
                Order.objects.filter(out_trade_no=out_trade_no).update(order_status=1,
                                                                       pay_time=result_data.get('timestamp'),
                                                                       trade_no=result_data.get('trade_no'))
                # 完成日志记录
                logger.warning('%s订单支付成功' % out_trade_no)
                return Response('success')  # 支付宝要求的格式
            else:
                logger.error('%s订单支付失败' % out_trade_no)
                return Response('failed')
        except:
            return Response('failed')
