# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0017_auto_20170629_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procesoimpexp',
            name='estado_proceso',
            field=models.IntegerField(verbose_name='estado del proceso', default=0),
        ),
    ]
