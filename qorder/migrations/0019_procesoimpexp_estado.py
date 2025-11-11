# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0018_auto_20170629_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='procesoimpexp',
            name='estado',
            field=models.CharField(null=True, max_length=20, verbose_name='estado', blank=True),
        ),
    ]
