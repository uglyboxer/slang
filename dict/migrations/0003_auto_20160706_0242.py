# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-06 02:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0002_auto_20160702_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='definition',
            field=models.CharField(default=None, max_length=1000),
        ),
        migrations.AlterField(
            model_name='entry',
            name='translation',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True),
        ),
    ]