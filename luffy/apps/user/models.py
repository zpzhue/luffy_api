from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    '''用户模型类'''
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号码')

    class Meta:
        db_table = 'lf_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name