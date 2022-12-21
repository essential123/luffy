from alipay import AliPay
from alipay.utils import AliPayConfig
from . import settings

# 实例化对象，传入一堆参数
alipay = AliPay(
    appid=settings.APPID,
    app_notify_url=None,  # 默认回调 url
    app_private_key_string=settings.APP_PRIVATE_KEY_STRING,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY_STRING,
    sign_type=settings.SIGN,  # RSA 或者 RSA2
    debug=settings.DEBUG,  # 默认 False
    verbose=False,  # 输出调试数据
    config=AliPayConfig(timeout=15)  # 可选，请求超时时间
)
