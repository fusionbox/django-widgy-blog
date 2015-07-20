# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('widgy_blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloglayout',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
