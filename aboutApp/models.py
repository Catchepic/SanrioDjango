# Create your models here.
from django.utils import timezone
from django.db import models


class Store(models.Model):

    title = models.CharField(max_length=50, verbose_name=' 店铺名')
    description = models.TextField(verbose_name='店铺详情描述')
    publishDate = models.DateTimeField(max_length=20, default=timezone.now, verbose_name='发布时间')
    views = models.PositiveIntegerField('浏览量', default=0)

    def __str__(self):
        return self.title  # 在后台显示每条数据的title字段

    class Meta:
        verbose_name = '店铺'
        verbose_name_plural = '店铺'
        ordering = ('-publishDate',)


class StoreImg(models.Model):
    """
    产品图片
    """
    store = models.ForeignKey(Store,  # 该外键从属于Product类
                                related_name='storeImgs',  # 在Product类中利用该名称调用产品图片
                                verbose_name='店铺',
                                on_delete=models.CASCADE)  # 当产品删掉，产品的图片也会被删掉
    photo = models.ImageField(upload_to='Store/',
                              blank=True,
                              verbose_name='店铺图片')

    class Meta:
        verbose_name = '店铺图片'
        verbose_name_plural = '店铺图片'
