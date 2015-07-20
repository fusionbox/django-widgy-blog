# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import widgy.db.fields
import django.utils.timezone
import widgy.contrib.page_builder.db.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('page_builder', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('widgy', '0001_initial'),
        ('filer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', widgy.db.fields.VersionedWidgyField(to='widgy.VersionTracker', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'blog post',
                'verbose_name_plural': 'blog posts',
            },
        ),
        migrations.CreateModel(
            name='BlogLayout',
            fields=[
                ('defaultlayout_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='page_builder.DefaultLayout')),
                ('title', models.CharField(max_length=1023)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('summary', models.TextField(null=True, blank=True)),
                ('slug', models.CharField(help_text=b'Will default to the blog title', max_length=255, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('keywords', models.CharField(max_length=255, null=True, blank=True)),
                ('page_title', models.CharField(help_text=b'Will default to the blog title', max_length=255, null=True, blank=True)),
                ('author', models.ForeignKey(related_name='blog_bloglayout_set', to=settings.AUTH_USER_MODEL)),
                ('image', widgy.contrib.page_builder.db.fields.ImageField(related_name='+', on_delete=django.db.models.deletion.PROTECT, blank=True, to='filer.File', null=True)),
            ],
            options={
                'ordering': ['-date'],
                'abstract': False,
            },
        ),
    ]
