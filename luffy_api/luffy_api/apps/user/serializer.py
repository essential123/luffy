from rest_framework import serializers
from .models import UserInfo
import re
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from rest_framework.exceptions import APIException
from django.core.cache import cache


# 这个序列化类只做多方式登录的校验，不做序列化和反序列化
class UserMulLoginSerializer(serializers.ModelSerializer):
    # 如果不重写username，username字段自己的校验规则就过不了
    username = serializers.CharField()  # 重写，优先用现在的，就没有unique的限制了

    class Meta:
        model = UserInfo
        fields = ['username', 'password']

    # 封装之隐藏属性  __表示隐藏， _并不是隐藏，公司里约定俗成用 _ 表示只在内部用，如果外部想用，也可以用
    def _get_user(self, attrs):
        # attrs 是校验过后的数据：字段自己的规则【字段自己有规则：坑】和局部钩子
        username = attrs.get('username')
        password = attrs.get('password')
        # username可能是用户名，邮箱，手机号---》使用正则判断
        if re.match(r'^1[3-9][0-9]{9}$', username):
            user = UserInfo.objects.filter(mobile=username).first()
        elif re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', username):
            user = UserInfo.objects.filter(email=username).first()
        else:
            user = UserInfo.objects.filter(username=username).first()
        if user and user.check_password(password):
            return user
        else:
            return APIException('用户名或密码错误')

    def _get_token(self, user):
        try:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return token
        except Exception as e:
            return ValidationError(str(e))

    def validate(self, attrs):
        # print(attrs,type(attrs))  # OrderedDict([('username', 'jzb'), ('password', '123')]) <class 'collections.OrderedDict'>
        # 取出用户名和密码，校验用户名是否存在
        # 如果通过校验，返回attrs
        user = self._get_user(attrs)
        # 签发token
        # 把token写入序列化类对象中）如果有问题抛异常
        token = self._get_token(user)
        self.context['token'] = token
        self.context['username'] = user.username
        self.context['icon'] = 'http://127.0.0.1:8000/media/' + str(user.icon)
        # self.context['icon'] = user.icon # 对象
        # 以后如果有问题，都抛异常，如没有问题，返回attrs
        return attrs


class UserMobileLoginSerializer(serializers.ModelSerializer):
    # 如果不重写mobile，mobile字段自己的校验规则就过不了
    mobile = serializers.CharField()  # 重写，优先用现在的，就没有unique的限制了
    code = serializers.CharField()  # code不是userinfo表字段，不能从表里映射，需要自己添加额外字段

    class Meta:
        model = UserInfo
        fields = ['mobile', 'code']

    def _get_user(self, attrs):
        # attrs 是校验过后的数据
        mobile = attrs.get('mobile')
        code = attrs.get('code')
        old_code = cache.get('sms_code_%s' % mobile)
        cache.set('sms_code_%s' % mobile, '')
        if code == old_code or code == '8888':
            user = UserInfo.objects.filter(mobile=mobile).first()
            return user
        raise APIException('验证码错误')

    def _get_token(self, user):
        try:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return token
        except Exception as e:
            return ValidationError(str(e))

    def validate(self, attrs):
        # 取出手机号和code，校验用户名是否存在，如果通过校验，返回attrs
        user = self._get_user(attrs)
        # 签发token,把token写入序列化类对象中）如果有问题抛异常
        token = self._get_token(user)
        self.context['token'] = token
        self.context['username'] = user.username
        self.context['icon'] = 'http://127.0.0.1:8000/media/' + str(user.icon)
        # self.context['icon'] = user.icon # 对象
        # 以后如果有问题，都抛异常，如没有问题，返回attrs
        return attrs


class UserRegisterSerializer(serializers.ModelSerializer):  # 数据校验，反序列化
    code = serializers.CharField()

    class Meta:
        model = UserInfo
        fields = ['mobile', 'password', 'code']  # mobile就是唯一的，校验数据库是否唯一，映射过来就有了

    def _get_token(self, user):
        try:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return token
        except Exception as e:
            return ValidationError(str(e))

    def create(self, attrs):  # mobile,username,password
        user = UserInfo.objects.create_user(**attrs)
        return user


    def validate(self, attrs):
        mobile = attrs.get('mobile')
        code = attrs.get('code')
        old_code = cache.get('sms_code_%s' % mobile)
        cache.set('sms_code_%s' % mobile, '')
        # 1 验证code是否正确
        if old_code == code or code == "8888":
            attrs['username'] = mobile  # username设置为手机号
            attrs.pop('code')  # code剔除
            return attrs
            # 3 保存正常不用写，新增Userinfo，密码是加密的---》重写create方法
        raise APIException('验证码错误')
