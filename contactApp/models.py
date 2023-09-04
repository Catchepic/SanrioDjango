# Create your models here.
from django.http import HttpResponse
from django.utils import timezone
from django.db import models
from datetime import datetime
from django.db.models.signals import post_init, post_save  # 管理员单击“保存”前、后触发信号
from django.dispatch import receiver  # 信号接收的装饰器
from django.core.mail import send_mail  # 发送邮件
import os
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docx.shared import Mm, Inches, Pt


class Ad(models.Model):
    """
    招聘广告
    """
    title = models.CharField(max_length=50, verbose_name='招聘岗位')
    description = models.TextField(verbose_name='岗位要求')
    publishDate = models.DateTimeField(max_length=20,
                                       default=timezone.now,
                                       verbose_name='发布时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '招聘广告'
        verbose_name_plural = '招聘广告'
        ordering = ('-publishDate',)


class Resume(models.Model):
    """
    简历
    """
    name = models.CharField(max_length=20, verbose_name='姓名')
    character = models.CharField(max_length=30, verbose_name='合作肖像')
    storeName = models.CharField(max_length=20, verbose_name='公司名称')
    storeInfo = models.CharField(max_length=20, verbose_name='公司简介')
    bossName = models.CharField(max_length=20, verbose_name='联系人姓名')
    bossNum = models.CharField(max_length=20, verbose_name='联系人电话')
    email = models.EmailField(max_length=30, verbose_name='邮箱')
    position = models.CharField(max_length=40, verbose_name='联系地址')
    experience = models.TextField(blank=True,
                                  null=True,
                                  verbose_name='合作内容描述')
    grade_list = (
        (1, '未审'),
        (2, '通过'),
        (3, '未通过'),
    )
    status = models.IntegerField(choices=grade_list,
                                 default=1,
                                 verbose_name='面试成绩')
    publishDate = models.DateTimeField(max_length=20,
                                       default=timezone.now,
                                       verbose_name='提交时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '简历'
        verbose_name_plural = '简历'
        ordering = ('-status', '-publishDate')


@receiver(post_init, sender=Resume)  # “保存”前触发信号，简历模型
def before_save_resume(sender, instance, **kwargs):
    """
    :
    :param sender:
    :param instance:
    :param kwargs:
    """
    instance.__original_status = instance.status  # instance为传入的模型变量，一条记录

@receiver(post_save, sender=Resume)
def post_save_resume(sender, instance, **kwargs):
    """
    :
    :param sender:
    :param instance:
    :param kwargs:
    """
    email = instance.email  # 应聘者邮箱
    EMAIL_FROM = 'konsexyu@foxmail.com'  # 企业QQ邮箱

    if instance.__original_status == 1 and instance.status == 2:
        email_title = '通知：Sanrio合作初审核结果'
        email_body = instance.name + ':你好，恭喜您通过本企业初试'
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        template_path = os.getcwd() + '\\media\\recruit.docx'  # os.getcwd() 方法用于返回当前工作目录+模板文件
        template = DocxTemplate(template_path)  # 建立模板文件
        # 从instance实例中获取当前简历字段信息
        name = instance.name
        character = instance.character
        storeName = instance.storeName
        email = instance.email
        storeInfo = instance.storeInfo
        bossName = instance.bossName
        bossNum = instance.bossNum
        position = instance.position
        experience = instance.experience


        context = {
            'name': name,
            'character': character,
            'storeName': storeName,
            'email': email,
            'storeInfo': storeInfo,
            'bossName': bossName,
            'bossNum': bossNum,
            'position': position,
            'experience': experience,
        }
        template.render(context)  # 模板文件字段替换
        filename = '%s\\media\\contact\\recruit\\%s_%d.docx' % (os.getcwd(), instance.name, instance.id)  # 姓名_id号命名
        template.save(filename)  # 模板文件保存

    elif instance.__original_status == 1 and instance.status == 3:
        email_title = '通知：sanrio招聘初试结果'
        email_body = '很遗憾，您未能通过本企业初试，感谢您的关注'
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
