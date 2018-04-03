# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-01 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0004_auto_20180401_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='inner_ip',
            field=models.GenericIPAddressField(unique=True, verbose_name='内网管理IP'),
        ),
    ]
