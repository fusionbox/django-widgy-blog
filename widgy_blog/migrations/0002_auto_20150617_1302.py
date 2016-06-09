# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone


def adjust_timezone(apps, schema_editor):
    """
    Switching from date field to datetime field, the database assumes the timezone is UTC, so the times need to be
    converted to local time

    Example: date May 6 gets converted to May 6 midnight UTC, which gets rendered as May 5, 8 pm New York time, so
    the timezone (UTC) is stripped and changed to New York timezone
    """
    BlogLayout = apps.get_model('widgy_blog', 'BlogLayout')
    db_alias = schema_editor.connection.alias

    for blog_layout in BlogLayout.objects.using(db_alias).all():
        naive_date = timezone.make_naive(blog_layout.date, timezone=timezone.utc)
        blog_layout.date = timezone.make_aware(naive_date)
        blog_layout.save()


def reverse_timezone_adjustment(apps, schema_editor):
    BlogLayout = apps.get_model('widgy_blog', 'BlogLayout')
    db_alias = schema_editor.connection.alias

    for blog_layout in BlogLayout.objects.using(db_alias).all():
        naive_time = timezone.make_naive(blog_layout.date)
        blog_layout.date = timezone.make_aware(naive_time, timezone=timezone.utc)
        blog_layout.save()


class Migration(migrations.Migration):

    dependencies = [
        ('widgy_blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloglayout',
            name='date',
            field=models.DateTimeField(default=timezone.now),
        ),
        migrations.RunPython(adjust_timezone, reverse_timezone_adjustment),
    ]
