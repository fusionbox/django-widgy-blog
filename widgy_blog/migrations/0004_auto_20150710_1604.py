# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('widgy_blog', '0003_auto_20150701_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloglayout',
            name='defaultlayout_ptr',
        ),
        migrations.AddField(
            model_name='bloglayout',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
