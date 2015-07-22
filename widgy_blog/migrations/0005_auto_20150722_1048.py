# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import widgy.db.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('widgy_blog', '0004_auto_20150710_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloglayout',
            name='page_title',
            field=models.CharField(max_length=255, help_text='Will default to the blog title', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bloglayout',
            name='slug',
            field=models.CharField(max_length=255, help_text='Will default to the blog title', blank=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(editable=False, unique=True, populate_from='name', blank=True),
        ),
    ]
