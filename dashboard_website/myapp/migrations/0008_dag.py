# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-30 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alertspecification_jar_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.TextField()),
                ('dag_name', models.CharField(max_length=100)),
                ('dag_div', models.TextField()),
            ],
        ),
    ]
