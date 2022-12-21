# 核心代码
import random
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入对应产品模块的client models。
from tencentcloud.sms.v20210111 import sms_client, models

# 导入可选配置类
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from . import settings

# 获取n位随机数组验证码的函数
def get_code(num=4):
    code = ''
    for i in range(num):
        random_num = random.randint(0, 9)
        code += str(random_num)
    return code


# 发送短信函数
def send_sms_by_phone(mobile, code):
    try:
        # 必要步骤：
        # 实例化一个认证对象，入参需要传入腾讯云账户密钥对secretId，secretKey。
        # SecretId、SecretKey 查询: https://console.cloud.tencent.com/cam/capi
        cred = credential.Credential(settings.SECRET_ID, settings.SECRET_KEY)

        # 实例化一个http选项，可选的，没有特殊需求可以跳过。
        httpProfile = HttpProfile()
        httpProfile.reqMethod = "POST"  # post请求(默认为post请求)
        httpProfile.reqTimeout = 30    # 请求超时时间，单位为秒(默认60秒)
        httpProfile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)

        # 非必要步骤:
        # 实例化一个客户端配置对象，可以指定超时时间等配置
        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
        clientProfile.language = "en-US"
        clientProfile.httpProfile = httpProfile

        # 实例化要请求产品(以sms为例)的client对象
        # 第二个参数是地域信息，可以直接填写字符串ap-guangzhou，支持的地域列表参考 https://cloud.tencent.com/document/api/382/52071#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8
        client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)
        req = models.SendSmsRequest()

        # 短信应用ID: 短信SdkAppId在 [短信控制台] 添加应用后生成的实际SdkAppId，示例如1400006666
        # 应用 ID 可前往 [短信控制台](https://console.cloud.tencent.com/smsv2/app-manage) 查看
        # req.SmsSdkAppId = settings.APP_ID
        req.SmsSdkAppId = "1400637551"
        # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名
        # 签名信息可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-sign) 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-sign) 的签名管理查看
        # req.SignName = settings.SMS_SIGN
        req.SignName = settings.SMS_SIGN
        # 模板 ID: 必须填写已审核通过的模板 ID
        # 模板 ID 可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-template) 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-template) 的正文模板管理查看
        req.TemplateId = settings.TEMPLATE_ID
        # 模板参数: 模板参数的个数需要与 TemplateId 对应模板的变量个数保持一致，，若无模板参数，则设置为空
        req.TemplateParamSet = [code,]
        # 下发手机号码，采用 E.164 标准，+[国家或地区码][手机号]
        # 示例如：+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不要超过200个手机号
        req.PhoneNumberSet = ["+86" + mobile, ]
        # 用户的 session 内容（无需要可忽略）: 可以携带用户侧 ID 等上下文信息，server 会原样返回
        req.SessionContext = ""
        # 短信码号扩展号（无需要可忽略）: 默认未开通，如需开通请联系 [腾讯云短信小助手]
        req.ExtendCode = ""
        # 国际/港澳台短信 senderid（无需要可忽略）: 国内短信填空，默认未开通，如需开通请联系 [腾讯云短信小助手]
        req.SenderId = ""
        resp = client.SendSms(req)
        # 输出json格式的字符串回包
        print(resp.to_json_string(indent=2))   # 字符串
        return True
    except TencentCloudSDKException as err:
        return False
