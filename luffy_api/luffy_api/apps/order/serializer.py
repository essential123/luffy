from .models import Order, OrderDetail
from course.models import Course
from rest_framework import serializers
from rest_framework.exceptions import APIException
from libs.alipay_common import alipay, GATEWAY
from django.conf import settings


# 不做序列化，只做反序列化，还有数据校验
class OrderSerializer(serializers.ModelSerializer):
    # courses不是表里的字段，需要重写
    # 前端传入的是 courses:[1,3,4]----->转换成课程对象[课程对象1，课程对象3，课程对象4]
    courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['courses', 'total_amount', 'subject', 'pay_type']  # 只用来做数据校验和反序列化

    def _check_price(self, attrs):
        total_amount = attrs.get('total_amount')
        real_amount = 0
        # 循环所有课程，取出价格累加得到总价格
        for course in attrs.get('courses'):
            real_amount += course.price
        if not real_amount == total_amount:  # 不正常，抛异常
            raise APIException('价格不一致')
        else:
            return total_amount

    def _get_trade_no(self):
        import uuid
        return str(uuid.uuid4())

    def _get_user(self):
        # 当前登录用户，request.user
        request = self.context.get('request')
        return request.user  # 必须通过了登录认证，才有当前登录用户

    def _get_pay_url(self, trade_no, total_amount, subject):
        res = alipay.api_alipay_trade_page_pay(
            out_trade_no=trade_no,  # 订单号
            total_amount=float(total_amount),  # 订单总价格
            subject=subject,  # 订单标题，商品名称
            return_url=settings.RETURN_URL,  # get回调地址
            notify_url=settings.NOTIFY_URL  # post回调地址
        )
        return GATEWAY + res

    def _before_create(self, pay_url, attrs, user, trade_no):
        self.context['pay_url'] = pay_url
        attrs['user'] = user
        attrs['out_trade_no'] = trade_no
        # 要不要courses剔除？不需要后面还需要用， 现在的attrs:{courses:[对象1，对象2]，total_amount：11，subject：xx,pay_type:1,user:user,out_trade_no:3333}

    def validate(self, attrs):
        # 校验价格：计算一下总价格和后端算出来的总价格是否一致
        total_amount = self._check_price(attrs)
        # 生成订单号：唯一的
        trade_no = self._get_trade_no()
        # 3）支付用户：request.user
        user = self._get_user()
        # 4）支付链接生成，放入到self.context中
        pay_url = self._get_pay_url(trade_no, total_amount, attrs.get('subject'))
        # 5）入库(两个表)的信息准备：重写create方法
        self._before_create(pay_url, attrs, user, trade_no)
        return attrs

    def create(self, validated_data):
        # {courses:[对象1，对象2]，total_amount：11，subject：xx,pay_type:1,user:user,out_trade_no:3333}
        courses=validated_data.pop('courses')
        order=Order.objects.create(**validated_data)
        # 存订单详情表
        for course in courses:
            OrderDetail.objects.create(order=order, course=course, price=course.price, real_price=course.price)
        return order
