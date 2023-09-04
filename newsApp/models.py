from django.db import models

# Create your models here.
from django.db import models
from DjangoUeditor.models import UEditorField   #富文本编辑器
import django.utils.timezone as timezone

# Create your models here.


class MyNew(models.Model):
    NEWS_CHOICES = (
        ('企业要闻', '企业要闻'),
        ('角色新闻', '角色新闻'),
        ('通知公告', '通知公告'),
    )    #元组， 不是字段
    title = models.CharField(max_length=50, verbose_name=' 新闻标题')
    description = UEditorField(u'内容',     #富文本编辑器，后台中的别名
                               default='',  #内容为空
                               width=1000,
                               height=300,
                               imagePath='news/images/',  #上传图像的存储位置
                               filePath='news/files/')     #上传文件的存储位置
    newType = models.CharField(choices=NEWS_CHOICES,   #上面定义的元组
                               max_length=50,
                               verbose_name='新闻类型')
    publishDate = models.DateTimeField(max_length=20,
                                       default=timezone.now,
                                       verbose_name='发布时间')
    views = models.PositiveIntegerField('浏览量', default=0)

    def __str__(self):
        return self.title  #后台中显示新闻标题字段

    class Meta:
        ordering = ['-publishDate']
        verbose_name = "新闻"
        verbose_name_plural = verbose_name

