# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-31 04:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_dag'),
    ]

    operations = [
        migrations.AddField(
            model_name='dag',
            name='description',
            field=models.TextField(default='No Description provided'),
        ),
    ]
