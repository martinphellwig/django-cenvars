# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-21 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_cenvars', '0002_auto_multiple_inheritance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inheritance',
            options={'ordering': ['offspring', 'sortorder']},
        ),
        migrations.AddField(
            model_name='inheritance',
            name='sortorder',
            field=models.FloatField(default=0.0),
        ),
    ]
