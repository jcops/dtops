# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-20 18:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=30, unique=True, verbose_name='主机名')),
                ('inner_ip', models.GenericIPAddressField(unique=True, verbose_name='内网管理IP')),
                ('pub_ip', models.GenericIPAddressField(blank=True, null=True, unique=True, verbose_name='公网IP')),
                ('port', models.IntegerField(default=22, verbose_name='端口')),
                ('mem_total', models.CharField(blank=True, max_length=20, null=True, verbose_name='总内存')),
                ('disk_total', models.CharField(blank=True, max_length=20, null=True, verbose_name='总磁盘')),
                ('cpu_model', models.CharField(blank=True, max_length=30, null=True, verbose_name='CPU型号')),
                ('num_cpus', models.IntegerField(blank=True, null=True, verbose_name='CPU核数')),
                ('osfinger', models.CharField(blank=True, max_length=20, null=True, verbose_name='系统版本')),
                ('osrelease', models.CharField(blank=True, max_length=20, null=True, verbose_name='系统发行版本')),
                ('dns', models.GenericIPAddressField(blank=True, null=True, verbose_name='DNS')),
                ('mac_addr', models.CharField(blank=True, max_length=20, null=True, verbose_name='MAC地址')),
                ('kernelrelease', models.CharField(blank=True, max_length=30, null=True, verbose_name='内核版本')),
                ('serialnumber', models.CharField(blank=True, max_length=40, null=True, verbose_name='序列号')),
                ('virtual', models.CharField(blank=True, max_length=20, null=True, verbose_name='虚拟化')),
                ('status', models.CharField(choices=[(0, '正常'), (1, '异常'), (2, '下线'), (3, '上线')], default=0, max_length=5, verbose_name='状态')),
                ('detail', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '资产',
                'verbose_name_plural': '资产',
            },
        ),
        migrations.CreateModel(
            name='Cloud_Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='名称')),
                ('cloud', models.CharField(blank=True, max_length=20, null=True, verbose_name='云平台')),
                ('detail', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '云平台',
                'verbose_name_plural': '云平台',
            },
        ),
        migrations.CreateModel(
            name='PerforMance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_use', models.CharField(blank=True, max_length=100, null=True, verbose_name='CPU使用率')),
                ('mem_use', models.CharField(blank=True, max_length=100, null=True, verbose_name='内存使用率')),
                ('disk_use', models.CharField(blank=True, max_length=100, null=True, verbose_name='磁盘使用率')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.Asset', verbose_name='资产')),
            ],
            options={
                'verbose_name': '资产性能',
                'verbose_name_plural': '资产性能',
            },
        ),
        migrations.CreateModel(
            name='ProductLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='产品线名称')),
                ('detail', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '产品线',
                'verbose_name_plural': '产品线',
            },
        ),
        migrations.CreateModel(
            name='System_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='名称')),
                ('username', models.CharField(default='root', max_length=20, verbose_name='系统用户')),
                ('password', models.CharField(max_length=20, verbose_name='用户密码')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('detail', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '系统用户',
                'verbose_name_plural': '系统用户',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='标签')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.AddField(
            model_name='asset',
            name='cloud_platform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.Cloud_Platform', verbose_name='云平台'),
        ),
        migrations.AddField(
            model_name='asset',
            name='create_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asset', to=settings.AUTH_USER_MODEL, verbose_name='创建用户'),
        ),
        migrations.AddField(
            model_name='asset',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.ProductLine', verbose_name='产品线'),
        ),
        migrations.AddField(
            model_name='asset',
            name='system_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.System_User', verbose_name='系统用户'),
        ),
        migrations.AddField(
            model_name='asset',
            name='tag',
            field=models.ManyToManyField(blank=True, to='asset.Tag', verbose_name='标签'),
        ),
    ]