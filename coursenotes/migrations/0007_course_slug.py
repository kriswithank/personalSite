# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-05 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursenotes', '0006_remove_chapter_parent_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
