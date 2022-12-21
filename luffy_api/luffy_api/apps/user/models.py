from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


# user 的app的models.py中扩写用户表
class UserInfo(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)
    # 需要pillow包的支持 ImageField继承了 FileField只存储图片
    icon = models.ImageField(upload_to='icon', default='icon/default.png')

    class Meta:
        db_table = 'luffy_user'  # 指定表名
        verbose_name = '用户表'  # 后台管理显示中文
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
