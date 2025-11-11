# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0026_auto_20170724_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicoconsumo',
            name='cod_anomalia',
            field=models.CharField(null=True, blank=True, max_length=10, verbose_name='cod_anomalia'),
        ),
    ]
