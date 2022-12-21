from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from utils.common_logger import logger

# 原来的异常处理
def exception_handler(exc, context):
    # 程序出了异常，会走到这,我们都要记录日志
    # 请求地址，请求方式，请求时间，请求哪个视图函数，如果登录了，记录一下用户id
    request=context.get('request')
    try:
        user_id = request.user.pk
        if not user_id:
            user_id = '匿名用户'
    except:
        user_id = '匿名用户'
    view = context.get('view')
    logger.error('用户：【%s】，使用：【%s】 请求，请求：【%s】 地址，视图函数是：【%s】，出错了，错误是：【%s】' % (
        user_id, request.method, request.get_full_path(), str(view), str(exc)
    ))
    # 第一步：执行一下原来的异常处理:它只处理drf的异常，django的异常没有处理
    # res如果有值是Response的对象，说明是drf的异常
    # res如果是None，说明是django的异常
    res = drf_exception_handler(exc, context)
    # 在这里，可以通过状态码，把异常分的更细一些：比如有数据的异常，除以0的异常，列表越界异常。。。。
    if res:
        # drf异常
        # res=Response(data={'code':999,'msg':'服务器出错，请联系系统管理员'})
        res = Response(data={'code': 999, 'msg': res.data.get('detail', '服务器出错，请联系系统管理员')})
    else:
        # django的异常，状态码是888，错误信息是  exc异常对象转成字符串
        res = Response(data={'code': 888, 'msg': str(exc)})

    return res
