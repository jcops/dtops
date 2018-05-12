from django.db import models

# Create your models here.
class KeyList(models.Model):
    STATUS_CHOICES = (
        ('1','认证'),
        ('2','未认证')
    )
    name = models.CharField(max_length=50,verbose_name='key名',unique=True)
    status = models.BooleanField(choices=STATUS_CHOICES,verbose_name='状态')

    def __str__(self):
        return  self.name

    class Meta:
        verbose_name = 'key列表'
        verbose_name_plural = verbose_name


class CmdLog(models.Model):
    host = models.CharField(max_length=30,blank=True,null=True,verbose_name="目标主机")
    cmd = models.CharField(max_length=100,blank=True,null=True,verbose_name="执行命令")
    ret_code = models.CharField(max_length=5000,blank=True,null=True,verbose_name="执行结果")
    user = models.CharField(max_length=20,blank=True,null=True,verbose_name="执行用户")
    set_time = models.DateTimeField(auto_now_add=True,verbose_name="执行时间")

    def __str__(self):
        return  self.host

    class Meta:
        verbose_name = "执行命令记录"
        verbose_name_plural = verbose_name


class Deploy_Model(models.Model):
    MODEL_NAME = (
        (1,'zookeeper'),
        (2,'nginx'),
        (3,'redis'),
        (4,'mysql'),

    )
    name = models.CharField(max_length=30,choices=MODEL_NAME,default='模块名称')
    # host = models.ForeignKey('KeyList',default='主机节点')
    detail = models.CharField(max_length=100,default='备注')

    def __str__(self):
        return  self.name

    class Meta:
        verbose_name = '模块部署'
        verbose_name_plural = verbose_name


