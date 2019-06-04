from django.db import models

from luffy.utils.base_model import BaseModel
# Create your models here.


class BannerInfo(BaseModel):
    name = models.CharField(max_length=150, verbose_name='轮播图名称')
    link = models.CharField(max_length=150, verbose_name='轮播图链接地址')
    image = models.ImageField(upload_to='banner', verbose_name='轮播图')
    order = models.IntegerField(verbose_name='显示顺序')
    is_show = models.BooleanField(default=False, verbose_name='是否上架')

    class Meta:
        db_table = 'lf_banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.name