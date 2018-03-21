from django.db import models
from users.models import UserProfile


# Create your models here.

class Asset(models.Model):
    '''资产表'''
    STATUS_CHOICES = (
        ('正常','正常'),
        ('异常','异常'),
        ('下线','下线'),
        ('上线','上线'),
    )

    hostname = models.CharField(max_length=30, unique=True, verbose_name='主机名')
    inner_ip = models.GenericIPAddressField(max_length=20, verbose_name='内网管理IP', unique=True)
    pub_ip = models.GenericIPAddressField(max_length=20, null=True, blank=True, verbose_name='公网IP', unique=True)
    port = models.IntegerField(default=22, verbose_name='端口')
    mem_total = models.CharField(max_length=20, null=True, blank=True, verbose_name='总内存')
    disk_total = models.CharField(max_length=20,null=True,blank=True,verbose_name='总磁盘')
    cpu_model = models.CharField(max_length=30,null=True,blank=True,verbose_name='CPU型号')
    num_cpus = models.IntegerField(null=True,blank=True,verbose_name='CPU核数')
    osfinger = models.CharField(max_length=20,null=True,blank=True,verbose_name='系统版本')
    osrelease = models.CharField(max_length=20,null=True,blank=True,verbose_name='系统发行版本')
    dns = models.GenericIPAddressField(max_length=20,null=True,blank=True,verbose_name='DNS')
    mac_addr = models.CharField(max_length=20,null=True,blank=True,verbose_name='MAC地址')
    kernelrelease = models.CharField(max_length=30,null=True,blank=True,verbose_name='内核版本')
    serialnumber = models.CharField(max_length=40,null=True,blank=True,verbose_name='序列号')
    virtual = models.CharField(max_length=20,null=True,blank=True,verbose_name='虚拟化')
    status = models.CharField(max_length=5,choices=STATUS_CHOICES,default='正常',verbose_name='状态')
    detail = models.CharField(max_length=100,null=True,blank=True,verbose_name='备注')
    system_user = models.ForeignKey(to='System_User', null=True, blank=True, verbose_name='系统用户')
    product = models.ForeignKey(to='ProductLine', null=True, blank=True,  verbose_name='产品线')
    tag = models.ManyToManyField(to='Tag',blank=True,verbose_name='标签')
    cloud_platform = models.ForeignKey(to='Cloud_Platform', null=True,blank=True,  verbose_name='云平台')
    create_user = models.ForeignKey(to='users.UserProfile', null=True, blank=True, related_name='asset' ,verbose_name='创建用户')
    create_time = models.DateTimeField(auto_now_add=True,null=True, blank=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,null=True, blank=True, verbose_name='更新时间')

    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name = '资产'
        verbose_name_plural = verbose_name



class System_User(models.Model):
    '''系统用户表'''
    name = models.CharField(max_length=20,unique=True,verbose_name='名称')
    username = models.CharField(max_length=20,default='root',verbose_name='系统用户')
    password = models.CharField(max_length=20,verbose_name='用户密码')


    create_time = models.DateTimeField(auto_now_add=True,null=True, blank=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,null=True, blank=True,verbose_name='更新时间')
    detail = models.CharField(max_length=100,null=True,blank=True,verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '系统用户'
        verbose_name_plural = verbose_name


class ProductLine(models.Model):
    '''产品线'''

    name = models.CharField(max_length=20, unique=True, verbose_name='产品线名称')
    detail = models.CharField(max_length=100, null=True, blank=True, verbose_name='备注')

    create_time = models.DateTimeField(auto_now_add=True,null=True, blank=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,null=True, blank=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '产品线'
        verbose_name_plural = verbose_name

class Tag(models.Model):
    '''标签'''
    name = models.CharField(max_length=20, unique=True, verbose_name='标签')

    create_time = models.DateTimeField(auto_now_add=True,null=True, blank=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True,verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

class Cloud_Platform(models.Model):
    '''云平台'''
    CLOUD_CHOICES = (
        ('阿里云','阿里云'),
        ('腾讯云', '腾讯云'),
        ('其他', '其他'),
        ('私有云', '私有云'),
    )
    name = models.CharField(max_length=20, unique=True, verbose_name='名称')
    cloud = models.CharField(max_length=20,choices=CLOUD_CHOICES,null=True,blank=True, verbose_name='云平台')
    detail = models.CharField(max_length=100, null=True, blank=True, verbose_name='备注')

    create_time = models.DateTimeField(auto_now_add=True,null=True, blank=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True,verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '云平台'
        verbose_name_plural = verbose_name


class PerforMance(models.Model):
    '''资产性能表'''

    cpu_use = models.CharField(max_length=100,null=True,blank=True,verbose_name='CPU使用率')
    mem_use = models.CharField(max_length=100,null=True,blank=True,verbose_name='内存使用率')
    disk_use = models.CharField(max_length=100,null=True,blank=True,verbose_name='磁盘使用率')
    asset = models.ForeignKey(Asset,null=True, blank=True,verbose_name='资产')

    create_time = models.DateTimeField(auto_now_add=True,null=True, blank=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True,verbose_name='更新时间')

    def __str__(self):
        return self.cpu_use

    class Meta:
        verbose_name = '资产性能'
        verbose_name_plural = verbose_name