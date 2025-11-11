# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0006_auto_20170411_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicoconsumo',
            name='anio',
            field=models.CharField(max_length=10, verbose_name='anio', null=True, blank=True),
        ),
    ]
