# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('widgy_blog', '0002_auto_20150617_1302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'name', blank=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='bloglayout',
            name='tags',
            field=models.ManyToManyField(to='widgy_blog.Tag', blank=True),
        ),
    ]
