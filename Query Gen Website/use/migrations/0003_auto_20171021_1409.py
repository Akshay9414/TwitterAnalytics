# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-21 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('use', '0002_auto_20160915_1825'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('hashtag', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('userid', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='customer',
            name='room',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='cus',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='obj',
        ),
        migrations.RemoveField(
            model_name='request',
            name='room_no',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='room_assigned',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='user',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Purchase',
        ),
        migrations.DeleteModel(
            name='Request',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
        migrations.DeleteModel(
            name='Staff',
        ),
        migrations.DeleteModel(
            name='Thing',
        ),
    ]