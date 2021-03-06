# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-15 15:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('age', models.IntegerField(default=20)),
                ('in_hotel', models.BooleanField(default=False)),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quant', models.IntegerField(default=1)),
                ('paid', models.BooleanField(default=False)),
                ('cus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='use.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('extra_points', models.CharField(max_length=200)),
                ('done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=200)),
                ('orientation', models.CharField(choices=[('North facing', 'North facing'), ('East facing', 'East facing'), ('South facing', 'South facing'), ('West facing', 'West facing')], max_length=200)),
                ('occupied', models.BooleanField(default=False)),
                ('rent', models.IntegerField(default=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=200)),
                ('designation', models.CharField(choices=[('Manager', 'Manager'), ('Assistant manager', 'Assistant manager'), ('Sweeper', 'Sweeper'), ('Waiter', 'Waiter'), ('Laundary', 'Laundary'), ('Cook', 'Cook')], max_length=200)),
                ('management', models.BooleanField(default=False)),
                ('room_assigned', models.ManyToManyField(to='use.Room')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obj_name', models.CharField(max_length=200)),
                ('price', models.IntegerField(default=0)),
                ('object_type', models.CharField(choices=[('Book', 'Book'), ("Men's Grooming", "Men's Grooming"), ('Womens Grooming', 'Womens Grooming'), ('Packed Edibles', 'Packed Edibles'), ('Hotel souvenier', 'Hotel souvenier'), ('Food', 'Food')], max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='room_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='use.Room'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='use.Thing'),
        ),
        migrations.AddField(
            model_name='customer',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='use.Room'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
