# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-04 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursenotes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='dept_num',
            field=models.CharField(default='fooo', max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='course_num',
            field=models.CharField(max_length=50),
        ),
    ]
