# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-04 02:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='finance.Category'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='categories',
            field=models.ManyToManyField(blank=True, to='finance.Category'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True),
        ),
    ]
