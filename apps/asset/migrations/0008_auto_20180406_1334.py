# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-06 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0007_auto_20180406_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='dns',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='DNS'),
        ),
    ]