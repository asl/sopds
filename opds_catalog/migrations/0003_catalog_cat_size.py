# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opds_catalog', '0002_auto_20161102_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='cat_size',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
