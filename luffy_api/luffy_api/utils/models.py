from django.db import models


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')   # 只在创建数据的那一刻自动获取当前时间 之后如果不人为更改则不变
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')   # 每次操作数据并保存都会自动更新当前时间
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    is_show = models.BooleanField(default=True, verbose_name='是否显示')
    orders = models.IntegerField(verbose_name='优先级')

    class Meta:
        abstract = True
