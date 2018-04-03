# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-01 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0002_auto_20180320_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='cpu_model',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='CPU型号'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='kernelrelease',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='内核版本'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='mac_addr',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='MAC地址'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='osfinger',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='系统版本'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='osrelease',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='系统发行版本'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='serialnumber',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='序列号'),
        ),
    ]