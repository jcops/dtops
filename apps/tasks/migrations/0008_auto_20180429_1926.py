# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-29 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20180429_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='salt_returns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fun', models.CharField(max_length=50)),
                ('jid', models.CharField(max_length=255)),
                ('return_field', models.TextField(db_column='return')),
                ('success', models.CharField(max_length=10)),
                ('full_ret', models.TextField()),
                ('alter_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'salt_returns',
            },
        ),
        migrations.DeleteModel(
            name='SaltReturns',
        ),
    ]