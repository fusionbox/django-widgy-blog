# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('widgy_blog', '0003_auto_20150701_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloglayout',
            name='defaultlayout_ptr',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='bloglayout',
            old_name='defaultlayout_ptr',
            new_name='id',
        ),
    ]
