from  __future__ import  unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserProfile(AbstractUser):
    '''扩展用户表'''
    nick_name = models.CharField(max_length=15,default='', blank=True, null=True, verbose_name='昵称')
    mobile = models.CharField(max_length=11, verbose_name='手机号')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

class UserLog(models.Model):
    LOGIN_TYPE_CHOICES = (
        ("W", "Web"),
        ("A", "App"),
    )
    username = models.CharField(max_length=20, verbose_name='登录用户')
    type = models.CharField(max_length=5, choices=LOGIN_TYPE_CHOICES, verbose_name='登录类型')
    user_agent = models.CharField(max_length=254, blank=True, null=True,  verbose_name='浏览器设备')
    ip = models.GenericIPAddressField(verbose_name='登录IP')
    city = models.CharField(max_length=254, verbose_name='登录城市')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')

    class Meta:
        verbose_name = '登录日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username