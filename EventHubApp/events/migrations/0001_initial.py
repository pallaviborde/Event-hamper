# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-14 22:48
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(max_length=50)),
                ('reason', models.CharField(max_length=50)),
                ('messsage', models.CharField(max_length=50)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('lastUpdatedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=60)),
                ('street1', models.CharField(max_length=50)),
                ('street2', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True)),
                ('verifyFlag', models.BooleanField(default=False)),
            ],
        ),
    ]
