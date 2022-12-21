import time
from .celery import app
import random

@app.task  # app注册
def send_sms(mobile, code):
    # 想用django项目里面的东西需要在celery配置
    from libs.send_tx_sms import send_sms_by_phone
    from user.models import UserInfo
    send_sms_by_phone(mobile, code)
    user=UserInfo.objects.all().filter(mobile=mobile).first()
    print('给%s短信发送成功:%s,验证码是:%s' % (user.username,mobile, code))
    return True

@app.task
def seckill_task():
    time.sleep(6)  # 模拟秒杀需要3s
    res = random.choice([True, False])
    if res:
        return '秒杀成功'
    else:
        return '很遗憾，您没有秒到'
