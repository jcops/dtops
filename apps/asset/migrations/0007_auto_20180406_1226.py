# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-06 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0006_auto_20180401_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloud_platform',
            name='cloud',
            field=models.CharField(blank=True, choices=[('阿里云', '阿里云'), ('腾讯云', '腾讯云'), ('其他', '其他'), ('私有云', '私有云')], max_length=50, null=True, verbose_name='云平台'),
        ),
        migrations.AlterField(
            model_name='cloud_platform',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='productline',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='产品线名称'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='标签'),
        ),
    ]
