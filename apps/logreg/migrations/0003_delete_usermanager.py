# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 18:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logreg', '0002_usermanager'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserManager',
        ),
    ]